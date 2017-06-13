#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppies

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

def query_puppies_by_name():
    return session.query(Puppies.name).order_by(Puppies.name.asc()).all()


def query_puppies_by_age_desc():
    today = datetime.date.today()
    if passes_leap_day(today):
        six_months_ago = today - datetime.timedelta(days = 183)
    else:
        six_months_ago = today - datetime.timedelta(days = 182)

    return session.query(Puppies.name, Puppies.birth)\
        .filter(Puppies.birth >= six_months_ago)\
        .order_by(Puppies.birth.desc())


def passes_leap_day(today):
    """
    Returns true if most recent February 29th occured after or exactly 183 days ago (366 / 2)
    """
    this_year = today.timetuple()[0]
    if is_leap_year(this_year):
        six_months_ago = today - datetime.timedelta(days = 183)
        leap_day = datetime.date(this_year, 2, 29)
        return leap_day >= six_months_ago
    else:
        return False

def is_leap_year(this_year):
    """
    Returns true iff the current year is a leap year.
    Implemented according to logic at https://en.wikipedia.org/wiki/Leap_year#Algorithm
    """
    if this_year % 4 != 0:
        return False
    elif this_year % 100 != 0:
        return True
    elif this_year % 400 != 0:
        return False
    else:
        return True


def query_puppies_by_weight_asc():
    return session.query(Puppies.name, Puppies.weight)\
        .order_by(Puppies.weight.asc())\
        .all()


def query_puppies_by_position():
    return session.query(Shelter, func.count(Puppies.id))\
        .join(Puppies)\
        .groub_by(Shelter.id)\
        .all()

