#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

db = sqlite3.connect('database_name')
cursor = db.cursor()
cursor.execute("insert into database_table_name vales(value1, value2)")
db.commit()
