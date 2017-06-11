#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('db')
cursor = conn.cursor()
cursor.execute('select * from table_name')
result = cursor.fetchall()
print(result)
conn.close()
