from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify
)
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, SeriesCategories, SeriesItems, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///Series.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token

# Login and Logout methods are mainly obtained
# from the udacity tutorials github link.
# https://github.com/udacity/ud330/blob/master/Lesson3/step3/project.py

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response
        (json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style = "width: 300px; height: 300px;border-radius: 150px; \
                -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'],
	               email=login_session['email'],)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/logout')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showCategories'))
    else:
        response = make_response(
                   json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/categories')
def showCategories():
    """ Shows home page which displays all the categories
    and latest added series

    Returns:
        Home page
    """
    series = session.query(SeriesCategories)
    latest_series = session.query(SeriesItems).order_by(
                    SeriesItems.id.desc()).limit(5)
    if 'username' not in login_session:
        return render_template('publicCategoriesHome.html', series=series,
                               latest_series=latest_series)
    else:
        return render_template('categoriesHome.html',
                               series=series, latest_series=latest_series)


@app.route('/categories/<path:category_name>')
@app.route('/categories/<path:category_name>/items')
def showItems(category_name):
    """ Shows series of specific category

    Args:
        category_name:
            Name of the category to show series that belong to it
    Returns:
        Home page
    """
    itemCategory = session.query(SeriesCategories).filter_by(
                   name=category_name).one()
    series = session.query(SeriesCategories)
    all_series = session.query(SeriesCategories)
    items = session.query(SeriesItems).filter_by(category=itemCategory).all()
    if 'username' not in login_session:
        return render_template('publicCategoryItems.html',
                               itemCategory=itemCategory, series=series,
                               items=items, all_series=all_series)
    else:
        return render_template('categoryItems.html',
                               itemCategory=itemCategory, series=series,
                               items=items, all_series=all_series)


@app.route('/categories/<path:category_name>/items/new',
           methods=['GET', 'POST'])
def newItem(category_name):
    """ Adds a new series in specific category

    Args:
        category_name:
            Name of the category of the added series
    Returns:
        on GET: Page to add new series
        on POST: Reditect to showItems page that shows the category
                 in which the series was added
    """
    if 'username' not in login_session:
        return redirect('/login')

    allCategories = session.query(SeriesCategories).all()

    if request.method == 'POST':
        itemCategory = session.query(SeriesCategories).filter_by(
                       name=request.form['categoriesList']).one()
        newItem = SeriesItems(name=request.form['name'],
                              description=request.form['description'],
                              picture=request.form['picture'],
                              director=request.form['director'],
                              category=itemCategory,
                              user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('%s series successfully added' % (newItem.name))
        return redirect(url_for('showItems', category_name=itemCategory.name))
    else:
        return render_template('addItem.html', category_name=category_name,
                               allCategories=allCategories)


@app.route('/categories/<string:category_name>/<string:series_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, series_name):
    """ Edits existing series

    Args:
        category_name:
            Name of the category of the edited series
        series_name:
            Name of the edited series
    Returns:
        on GET: Page to edit existing series
        on POST: Reditect to showItems page that shows the category
                 in which the series was added
    """
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(SeriesItems).filter_by(name=series_name).one()
    categories = session.query(SeriesCategories).all()

    creator = getUserInfo(editedItem.user_id)

    if creator.id != login_session['user_id']:
        flash("You are not authorized to edit this series.\
               You can edit series you added only.\
               Only %s can edit this series" % creator.name)
        return redirect('/categories')

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['director']:
            editedItem.director = request.form['director']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['picture']:
            editedItem.picture = request.form['picture']
        if request.form['categories']:
            category = session.query(SeriesCategories).filter_by(
                       name=request.form['categories']).one()
            editedItem.category = category
        session.add(editedItem)
        flash('%s series edited successfully' % editedItem.name)
        session.commit()
        return redirect(url_for('showItems', category_name=category_name))
    else:
        return render_template('editItem.html',
                               category_name=category_name,
                               series_name=series_name, series=editedItem,
                               categories=categories)


@app.route('/categories/<string:category_name>/<string:series_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, series_name):
    """ Deletes existing series

    Args:
        category_name:
            Name of the category of the deleted series
        series_name:
            Name of the deleted series
    Returns:
        on GET: Page to delete existing series
        on POST: Reditect to showItems page that shows the category
                 from which the series was deleted
    """
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(SeriesItems).filter_by(
                  name=series_name).one()
    category = session.query(SeriesCategories).filter_by(
               name=category_name).one()

    creator = getUserInfo(deletedItem.user_id)

    if creator.id != login_session['user_id']:
        flash("You are not authorized to delete %s.\
               You can delete series you added only.\
               Only %s can delete this series" % (series_name, creator.name))
        return redirect('/categories')

    if request.method == 'POST':
        session.delete(deletedItem)
        flash('%s series successfully deleted' % deletedItem.name)
        session.commit()
        return redirect(url_for('showItems', category_name=category.name))
    else:
        return render_template('deleteItem.html',
                               category_name=category_name,
                               series_name=series_name,
                               item=deletedItem)


@app.route('/categories/<string:category_name>/<string:series_name>')
def showItem(category_name, series_name):
    """ Show description of a series

    Args:
        category_name:
            Name of the category of the shown series
        series_name:
            Name of the shown series
    Returns:
        page to show description of the selected series
    """
    series = session.query(SeriesItems).filter_by(name=series_name).one()
    if 'username' not in login_session:
        return render_template('publicItemDescription.html',
                               category_name=category_name, item=series)
    else:
        return render_template('itemDescription.html',
                               category_name=category_name, item=series)


# JSON

@app.route('/JSON')
@app.route('/categories/JSON')
def showCategoriesJSON():
    """ Shows all categories in JSON format

    Returns:
        returns all categories in JSON format
    """
    series = session.query(SeriesCategories)
    return jsonify(Series=[i.serialize for i in series])


@app.route('/categories/<string:category_name>/JSON')
@app.route('/categories/<string:category_name>/items/JSON')
def showItemsJSON(category_name):
    """ Show series of specific category in JSON format

    Args:
        category_name:
            Name of the category of the shown series
    Returns:
        returns all series in specific cateory in JSON format
    """
    series = session.query(SeriesCategories).filter_by(
             name=category_name).one()
    items = session.query(SeriesItems).filter_by(category=series).all()
    return jsonify(Items=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
