# import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Company(Base):
    __tablename__ = 'company'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
            'name': self.name,
            'id': self.id
        }


class Cars(Base):
    __tablename__ = 'cars'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    Specifications = Column(String(250))
    price = Column(String(16))
    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship(Company)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
            'name': self.name,
            'Specifications': self.Specifications,
            'id': self.id,
            'price': self.price,
        }


engine = create_engine('sqlite:///cars.db')
Base.metadata.create_all(engine)
