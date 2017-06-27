#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Restaurant, Menu

engine = create_engine()
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home'


if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1', port = 8080)
