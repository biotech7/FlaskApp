import sys
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.username,
            'email': self.email
        }



class Catalog(Base):
    __tablename__ = 'catalog'
    
    cname = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    user = relationship(User)
    user_id = Column(Integer, ForeignKey("user.id"))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.cname,
            'id': self.id
        }


class CatalogsItem(Base):
    __tablename__ = 'catalogsitem'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    catalogs_id = Column(Integer, ForeignKey("catalog.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    catalogs = relationship(Catalog)
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price
        }


engine = create_engine('sqlite:///site.db')


Base.metadata.create_all(engine)
