from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import SeriesCategories, Base, SeriesItems, User

engine = create_engine('sqlite:///Series.db')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Admin", email="admin12345@gmail.com")
session.add(User1)
session.commit()

# Series Categories
category1 = SeriesCategories(user_id = 1, name = "Action")

session.add(category1)
session.commit()

category2 = SeriesCategories(user_id = 1, name = "Comedy")

session.add(category2)
session.commit()

category3 = SeriesCategories(user_id = 1, name = "Crime")

session.add(category3)
session.commit()

category4 = SeriesCategories(user_id = 1, name = "Biography")

session.add(category4)
session.commit()

category5 = SeriesCategories(user_id = 1, name = "Drama")

session.add(category5)
session.commit()

# Series Items

seriesItem1 = SeriesItems(user_id = 1, name = "Breaking Bad", description = "Breaking Bad is an American neo-western crime drama television series created and produced by Vince Gilligan, the series tells the story of Walter White (Bryan Cranston), a struggling and depressed high school chemistry teacher who is diagnosed with lung cancer. Together with his former student Jesse Pinkman (Aaron Paul), White turns to a life of crime by producing and selling crystallized methamphetamine to secure his family's financial future before he dies, while navigating the dangers of the criminal world.", director = "Vince Gilligan", picture = 'https://upload.wikimedia.org/wikipedia/en/6/61/Breaking_Bad_title_card.png', category = category3)

session.add(seriesItem1)
session.commit()

seriesItem2 = SeriesItems(user_id = 1, name = "House M.D.", description = "House is an American television medical drama. The series main character is Dr. Gregory House (Hugh Laurie), an unconventional, misanthropic medical genius who, despite his dependence on pain medication, leads a team of diagnosticians at the fictional Princeton Plainsboro Teaching Hospital (PPTH) in New Jersey.", director = "David Shore", picture = 'https://art-s.nflximg.net/af523/97fc0b9faf2f4a2728a10b716fb2ab622a4af523.jpg', category = category5)

session.add(seriesItem2)
session.commit()

seriesItem3 = SeriesItems(user_id = 1, name = "Narcos", description = "Narcos is an American crime drama web television series that is set and filmed in Colombia, seasons one and two are based on the story of drug kingpin Pablo Escobar, who became a billionaire through the production and distribution of cocaine. The series also focuses on Escobar's interactions with drug lords, Drug Enforcement Administration (DEA) agents, and various opposition entities. Season three picks up after the fall of Escobar and continues to follow the DEA as they try to shutdown the rise of the infamous Cali Cartel.", director = "Chris Brancato", picture = 'https://upload.wikimedia.org/wikipedia/en/0/0a/Narcos_title_card.jpg', category = category4)

session.add(seriesItem3)
session.commit()

seriesItem4 = SeriesItems(user_id = 1, name = "Friends", description = "Friends is an American television sitcom. The show revolves around six 20 to 30 years old friends living in Manhattan, New York City.", director = "David Crane", picture = 'https://cdn.24.co.za/files/Cms/General/d/4320/28d1220097b54f79907f2d810b51ad0b.jpg', category = category2)

session.add(seriesItem4)
session.commit()

seriesItem5 = SeriesItems(user_id = 1, name = "Prison Break", description = "Prison Break is an American television serial drama. The series revolves around two brothers, one of whom has been sentenced to death for a crime he did not commit, and the other who devises an elaborate plan to help his brother escape prison and clear his name.", director = "Paul Scheuring", picture = 'https://upload.wikimedia.org/wikipedia/en/d/d3/Prison-break-s1-intro.jpg', category = category1)

session.add(seriesItem5)
session.commit()

seriesItem6 = SeriesItems(user_id = 1, name = "La casa de papel", description = "La casa de papel is a Spanish heist television series. It revolves about a long-prepared, multiple day assault on the Royal Mint of Spain.", director = "Alex Pina", picture = 'https://upload.wikimedia.org/wikipedia/en/1/12/La_casa_de_papel_intertitle.png', category = category1)

session.add(seriesItem6)
session.commit()

seriesItem7 = SeriesItems(user_id = 1, name = "The Simpsons", description = "The Simpsons is an American animated sitcom. The series is a satirical depiction of working-class life, epitomized by the Simpson family, which consists of Homer, Marge, Bart, Lisa, and Maggie. The show is set in the fictional town of Springfield and parodies American culture and society, television, and the human condition.", director = "Matt Groening", picture = 'https://upload.wikimedia.org/wikipedia/en/0/0d/Simpsons_FamilyPicture.png', category = category2)

session.add(seriesItem7)
session.commit()

seriesItem8 = SeriesItems(user_id = 1, name = "Game of Thrones", description = "Game of Thrones is an American fantasy drama television series. It is filmed in Belfast and elsewhere in Northern Ireland, Canada, Croatia, Iceland, Malta, Morocco, Scotland, Spain, and the United States. Set on the fictional continents of Westeros and Essos, Game of Thrones has several plot lines and a large ensemble cast but centers on three primary story arcs. The first story arc centers on the Iron Throne of the Seven Kingdoms and follows a web of alliances and conflicts among the dynastic noble families either vying to claim the throne or fighting for independence from the throne. The second story arc focuses on the last descendant of the realm's deposed ruling dynasty, exiled and plotting a return to the throne. The third story arc centers on the longstanding brotherhood charged with defending the realm against the ancient threats of the fierce peoples and legendary creatures that lie far north, and an impending winter that threatens the realm.", director = "David Benioff", picture = 'https://upload.wikimedia.org/wikipedia/en/d/d8/Game_of_Thrones_title_card.jpg', category = category1)

session.add(seriesItem8)
session.commit()

seriesItem9 = SeriesItems(user_id = 1, name = "Sherlock", description = "Sherlock is a British crime drama television series based on Sir Arthur Conan Doyle's Sherlock Holmes detective stories. Sherlock depicts consulting detective Sherlock Holmes (Benedict Cumberbatch) solving various mysteries in modern-day London. Holmes is assisted by his flatmate and friend, Dr John Watson (Martin Freeman), who has returned from military service in Afghanistan with the Royal Army Medical Corps. Although Metropolitan Police Service Detective Inspector Greg Lestrade (Rupert Graves) and others are suspicious of Holmes at first, over time, his exceptional intellect and bold powers of observation persuade them of his value. In part through Watson's blog documenting their adventures, Holmes becomes a reluctant celebrity with the press reporting on his cases and eccentric personal life. Both ordinary people and the British government ask for his help.", director = "Mark Gatiss", picture = 'https://upload.wikimedia.org/wikipedia/en/4/4d/Sherlock_titlecard.jpg', category = category3)

session.add(seriesItem9)
session.commit()

seriesItem10 = SeriesItems(user_id = 1, name = "Spartacus", description = "Spartacus is a British television series produced in New Zealand. The fiction series was inspired by the historical figure of Spartacus, a Thracian gladiator who from 73 to 71 BCE led a major slave uprising against the Roman Republic departing from Capua.", director = "Steven S. DeKnight", picture = 'https://images-na.ssl-images-amazon.com/images/I/61FXwFfGPLL._SS500.jpg', category = category4)

session.add(seriesItem10)
session.commit()


seriesItem11 = SeriesItems(user_id = 1, name = "Dexter", description = "Dexter is an American television crime drama mystery series that centers on Dexter Morgan (Michael C. Hall), a forensic technician specializing in blood spatter pattern analysis for the fictional Miami Metro Police Department, who leads a secret parallel life as a vigilante serial killer, hunting down murderers who have slipped through the cracks of the justice system.", director = "James Manos, Jr.", picture = 'https://upload.wikimedia.org/wikipedia/en/c/c0/Dexter_TV_Series_Title_Card.jpg', category = category3)

session.add(seriesItem11)
session.commit()

seriesItem12 = SeriesItems(user_id = 1, name = "Buffy the Vampire Slayer", description = "Buffy the Vampire Slayer is an American supernatural drama television series based on the 1992 film of the same name. he series narrative follows Buffy Summers (played by Sarah Michelle Gellar), the latest in a line of young women known as Vampire Slayers, or simply Slayers. In the story, Slayers are called (chosen by fate) to battle against vampires, demons, and other forces of darkness. Being a young woman, Buffy wants to live a normal life, but as the series progresses, she learns to embrace her destiny. Like previous Slayers, Buffy is aided by a Watcher, who guides, teaches, and trains her. Unlike her predecessors, Buffy surrounds herself with a circle of loyal friends who become known as the Scooby Gang.", director = "Joss Whedon", picture = 'https://upload.wikimedia.org/wikipedia/en/2/29/Buffy_the_Vampire_Slayer_title_card.jpg', category = category1)

session.add(seriesItem12)
session.commit()

seriesItem13 = SeriesItems(user_id = 1, name = "Fargo", description = "Fargo is an American black comedy crime drama anthology television series. The show is inspired by the eponymous 1996 film written and directed by the Coen brothers. The series follows an anthology format, with each season set in a different era, and with a different story and mostly new characters and cast, although there is minor overlap. Each season shares a common chronology with the original film.", director = "Noah Hawley", picture = 'https://upload.wikimedia.org/wikipedia/commons/1/1e/Fargo_%28TV_logo%29.png', category = category1)

session.add(seriesItem13)
session.commit()



print "added series categories and items!"