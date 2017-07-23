#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Author: Kun Liu
# @Date: 2017-07-05 19:21:22
# @Last modified by: Kun Liu
# @Last modified date: 2017-07-10 20:31:22

import psycopg2
import sys

"""
    This file can connect to database for selecting
    the most popular articles, authors and
    the date with over 1% requests error.
"""

DBNAME = "news"

# Try to connect to database
try:
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
except:
    print "error when connecting to the database %s" % DBNAME
    sys.exit()

# open the out.txt for output the answer
with open('out.txt', 'w') as f:

    # select the most popular there articles
    c.execute("SELECT title, count(*) as reviews "
              "FROM articles,log "
              "WHERE '/article/'||articles.slug=log.path "
              "GROUP BY title "
              "ORDER BY reviews desc;")
    popular_article = c.fetchall()
    f.write('Most popular three artiles are: \n')
    for i in range(0, 3):
        f.write('     ' + str(i + 1) + '. "' + popular_article[i][0]
                + '"' + '--' + str(popular_article[i][1]) + ' reviews\n')

    # select the most popular authors sorted by list
    # c.execute("drop view if exists popular_article")
    c.execute("CREATE view popular_article as "
              "SELECT title, count(*) as reviews, author "
              "FROM articles, log "
              "WHERE ('/article/')||slug=path "
              "GROUP BY title,author "
              "ORDER BY reviews desc;")
    c.execute("SELECT name, sum(reviews) as views "
              "FROM authors join popular_article "
              "ON author=id "
              "GROUP BY name "
              "ORDER BY views desc;")
    popular_author = c.fetchall()
    f.write('\n\nMost popular authors are : \n')
    for i in range(0, len(popular_author)):
        f.write('     ' + str(i + 1) + '. "' + popular_author[i][0]
                + '"' + '--' + str(popular_author[i][1]) + ' reviews\n')

    # select the date more than 1% requests lead to errors
    # c.execute("drop view if exists error_date")
    # c.execute("drop view if exists total_date")
    c.execute("CREATE view error_date as "
              "SELECT time::date, count(*) as error_nums "
              "FROM log where status<>'200 OK' "
              "GROUP BY time::date;")
    c.execute("CREATE view total_date as "
              "SELECT time::date, count(*) as total_nums "
              "FROM log "
              "GROUP BY time::date;")
    c.execute("SELECT error_date.time, "
              "round(error_nums::numeric/total_nums::numeric,4) "
              "AS result from total_date "
              "JOIN error_date ON total_date.time=error_date.time "
              "WHERE round(error_nums::numeric/total_nums::numeric,4)>0.01;")
    error_date = c.fetchall()
    f.write('\n\nThis day had more than 1% requests lead to errors: \n')
    f.write('     ' + str(error_date[0][0]) + '--' +
            str(round(error_date[0][1] * 100, 2)) + '% errors')

# close database
db.close()
