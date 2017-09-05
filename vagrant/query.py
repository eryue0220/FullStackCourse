#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import psycopg2

DATABASE_NAME = 'news'
QUESTION_1 = '1.What are the most popular three articles of all time? \n'
QUESTION_2 = '2.Who are the most popular article authors of all time? \n'
QUESTION_3 = '3.Which days did more than 1% of requests lead to errors? \n'


def cget_query_results(query):
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


# get top 3 popular articles
def get_top_3_articles():
  return cget_query_results('''
    select title, count(path) as views
    from articles, log
    where log.status like '%200 OK%'
    and log.path = concat('/article/', articles.slug)
    group by title
    order by views desc
    limit 3;
  ''')


def get_most_popular_author():
  '''get the most popular author'''
  return cget_query_results('''
    select authors.name, count(log.path) as views
    from authors
    left join articles on articles.author = authors.id
    left join log on log.path = concat('/article/', articles.slug)
    where log.status like '%200 OK%'
    group by authors.name
    order by views desc;
  ''')


# Question 3 solved by SQL View 
# See README.md for more details
def calc_error_percent():
  '''calculate the error percentage'''
  return cget_query_results('''
    select error_per_day.time::date, (100.0 * error_count / total_count) as error_percent
    from error_per_day, total_per_day
    where error_per_day.time::date = total_per_day.time::date
    and (100.0 * error_count / total_count) > 1
    group by error_per_day.time::date, error_percent;
  ''')


def write_files(filename, question, answer, need=False):
  file_path = os.path.abspath(os.path.join(os.getcwd(), filename))
  mode = os.path.exists(file_path) and 'a' or 'w'
  breakLine = need and '\n' or ''

  with open(filename, mode) as f:
    f.write(question)
    for key in answer:
      if question == QUESTION_3: 
        val = '{:.2f}%'.format(key[1])
      else:  
        val = key[1]
      con = ' ' * 4 + str(key[0]) + ' - ' + str(val) + breakLine
      f.write(con)


def main():
  top3_articles = get_top_3_articles()
  popular_authors = get_most_popular_author()
  error_percent = calc_error_percent()
  
  write_files('result.txt', QUESTION_1, top3_articles, True)
  write_files('result.txt', QUESTION_2, popular_authors, True)
  write_files('result.txt', QUESTION_3, error_percent)


if __name__ == '__main__':
  main()
