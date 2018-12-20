import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       	   'id': self.id,
           'name': self.name,
		   'email': self.email,
}
 
class SeriesCategories(Base):
    __tablename__ = 'series_categories'
	
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
	
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       	   'id': self.id,
           'name': self.name,
}
 
class SeriesItems(Base):
    __tablename__ = 'series_item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    director = Column(String(80), nullable = False)
    description = Column(String(1000))
    picture = Column(String(250))
    category_id = Column(Integer,ForeignKey('series_categories.id'))
    category = relationship(SeriesCategories)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       	   'id': self.id,
           'name': self.name,
		   'picture': self.picture,
           'director': self.director,
           'description': self.description,
}
 

engine = create_engine('sqlite:///Series.db')
Base.metadata.create_all(engine)