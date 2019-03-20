from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import *

engine = create_engine('sqlite:///cars.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# delete old data
session.query(User).delete()
session.query(Company).delete()
session.query(Cars).delete()

# dummy user....
User1 = User(name="Dummy Deno", email="deno@gmail.com",
             picture='https://d3iw72m71ie81c.cloudfront.net/caesar.jpg')
session.add(User1)
session.commit()

# kia brand and autos
Company1 = Company(user_id=1, name="Kia")

session.add(Company1)
session.commit()

Car1 = Cars(
    user_id=1, name="Soul",
    Specifications="The Soul concept was styled in 2005",
    price="$20000", company=Company1)

session.add(Car1)
session.commit()

Car2 = Cars(
    user_id=1, name="Sportage",
    Specifications="Was developed with a Mazda base platform.",
    price="$32000", company=Company1)

session.add(Car2)
session.commit()

# skoda brand and autos
Company2 = Company(user_id=1, name="Skoda")

session.add(Company2)
session.commit()

Car3 = Cars(
    user_id=1, name="Octavia",
    Specifications="The Skoda Octavia produced since 1996.",
    price="$27000", company=Company2)

session.add(Car3)
session.commit()

Car4 = Cars(
    user_id=1, name="Fabia",
    Specifications="Fabia produced since 1999.",
    price="$17000", company=Company2)

session.add(Car4)
session.commit()
print "added autos!"
