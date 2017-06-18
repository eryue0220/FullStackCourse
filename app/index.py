#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Restaurant


app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/index')
def restaurant_list():
    restaurants = session.query(Restaurant).all()

    if restaurants:
        return render_template('restaurant.html', items=restaurants)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    output = ''

    if restaurant:
        output += restaurant.name
        output += '<br />'

    return output


@app.route('/restaurants/add/', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST' and request.form['name']:
        new_item = Restaurant(name = request.form['name'])
        session.add(new_item)
        session.commit()
        flash("new menu item created!")

        return redirect(url_for('restaurant_list'))

    return render_template('add.html')


@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def edit(restaurant_id):
    name = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST' and request.form['name']:
        name.name = request.form['name']
        session.add(name)
        session.commit()

        return redirect(url_for('restaurant_list'))

    return render_template('edit.html', name = name.name, restaurant_id = restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def delete(restaurant_id):
    deleteItem = session.query(Restaurant).filter_by(id = restaurant_id).one()    
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()

        return redirect(url_for('restaurant_list'))

    return render_template('delete.html', name = deleteItem.name, id = deleteItem.id)


@app.route('/restaurants/JSON')
def restaurantJSON():
    all = session.query(Restaurant).all()
    restaurant_json = []
    for item in all:
        restaurant_json.append(item.name)
    
    return jsonify(RestaurantItems=restaurant_json)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
