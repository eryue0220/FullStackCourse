#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
    return render_template('restaurants.html', restaurants = restaurants)


@app.route('/new/', methods=['GET', 'POST'])
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def addNewRestaurant():
    if request.method == 'POST':
        pass

    return render_template('add_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        pass

    return render_template('edit_restaurant.html', restaurant = {'name': 'The CRUDdy Crab', 'id': 1})


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        pass

    return render_template('delete_restaurant.html', restaurant = {'name': 'The CRUDdy Crab', 'id': 1})


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    menu = [{'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'}]
    restaurant = {'name':'Cheese Pizza', 'id': 1}
    return render_template('menu.html', restaurant = restaurant, items = menu)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def addMenu(restaurant_id):
    return 'This page will add a new menu for the restaurant.'


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenu(restaurant_id, menu_id):
    return 'This page will update menu for the restaurant'


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',
    methods=['GET', 'POST'])
def deleteMenu(restaurant_id, menu_id):
    return 'delete menu'


@app.route('/restaurants/json')
def restaurantJSONData():
    restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
    
    return jsonify(restaruants = restaurants)
    

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 8080)
