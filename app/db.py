#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)

    @property
    def serialize(self):
        '''Return object data in easily serializable format'''
        return {
            'id': self.id,
            'name': self.name
        }


class Menu(Base):
    __tablename__ = 'Menu'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'course': self.course
        }

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
