#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import psycopg2

DATABASE_NAME = 'news'
QUESTION_1 = '1.What are the most popular three articles of all time? \n'
QUESTION_2 = '2.Who are the most popular article authors of all time? \n'
QUESTION_3 = '3.Which days did more than 1% of requests lead to errors? \n'


def connect_database(database=DATABASE_NAME):
  return psycopg2.connect(database=database)


# get top 3 popular articles
def get_top_3_articles():
  db = connect_database()
  cursor = db.cursor()
  cursor.execute('''
    select title, count(path) as views
    from articles, log
    where log.status like '%200 OK%'
    and log.path like '%' || articles.slug || '%' 
    group by title
    order by views desc
    limit 3;
  ''')
  result = cursor.fetchall()
  db.close()

  return result


def get_most_popular_author():
  '''get the most popular author'''
  db = connect_database()
  cursor = db.cursor()

  # join query
  # cursor.execute('''
  #   select authors.name, count(log.path) as views
  #   from authors
  #   left join articles on articles.author = authors.id
  #   left join log on log.path like '%' || articles.slug || '%'
  #   group by authors.NameError
  #   order by views desc;
  # ''')

  cursor.execute('''
    select name, count(path) as views
    from articles, log, authors
    where articles.author = authors.id 
    and log.path like '%' || articles.slug || '%'
    group by name
    order by views desc;
  ''')
  result = cursor.fetchall()
  db.close()
  return result


def get_data_from_db():
  '''get the request count from database'''
  db = connect_database()
  cursor = db.cursor()
  cursor.execute('''
    select count(status) as err_num, date(time)
    from log where status like '4%' or status like '5%'
    group by date(time)
    order by err_num desc;
  ''')
  error = cursor.fetchall()

  cursor.execute('''
    select count(status) as total_num, date(time)
    from log
    group by date(time)
    order by total_num desc;
  ''')
  total = cursor.fetchall()
  db.close()
  return [error, total]


def sum_request_error():
  '''sum up the request error which more than 1%'''
  error, total = get_data_from_db()
  result = [(float(err_count) / total_count, str(date)) for (err_count, date) in error for (total_count, total_date) in total if str(date) == str(total_date)]
  data = []

  return [(str(round(percent * 100, 2)) + '%', date) for (percent, date) in result if percent * 100 > 1]
  

def write_files():
  top3_articles = get_top_3_articles()
  popular_authors = get_most_popular_author()
  err_percent = sum_request_error()

  with open('result.txt', 'wt') as f:
    for index, content in enumerate([top3_articles, popular_authors, err_percent]):
      if (index == 0): f.write(QUESTION_1)
      if (index == 1): f.write(QUESTION_2)
      if (index == 2): f.write(QUESTION_3)

      for (key, value) in content:
        con = ' ' + str(key) + ' - ' + str(value) + '\n'
        f.write(con)

if __name__ == '__main__':
  write_files()
