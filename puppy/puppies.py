#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    
    id = Column(Integer,  primary_key=True)
    name = Column(Integer, nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zip = Column(String(10))
    website = Column(String)


class Puppies(Base):
    __tablename__ = 'puppy'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(80), nullable=False)
    birth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship('shelter')
    weight = Column(Numeric(10))
    
engine = create_engine('sqlite:///puppies.db')

Base.metadata.create_all(engine)
