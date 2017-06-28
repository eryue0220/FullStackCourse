#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Restaurant, Menu
import random, string

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)


@app.route('/restaurant/<int:restaurant_id>/menu/json/')
def restaurant_menu_json(restaurant_id):
    menu = session.query(Menu).filter_by(restaurant_id = restaurant_id).all()

    return jsonify(Menus=[i.serialize for i in menu])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/json/')
def menu_json(restaurant_id, menu_id):
    menu = session.query(Menu).filter_by(id = menu_id).one()
    return jsonify(Menu = menu.serialize)


if __name__ == '__main__':
    app.secret_key = 'Super Secret Key'
    app.debug = True
    app.run(host = '127.0.0.1', port = 8080)
