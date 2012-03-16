#! /usr/bin/python

#This file includes methods for inserting feeds into the database
#Feeds are inserted manually, but may be processed from a form or another input source in the future

import MySQLdb as mdb
import sys
import datetime

#Settings for the mysql connection
mysql_conn = {
    'host' : 'localhost',
    'username' : 'root',
    'password': 'password',
    'db' : 'trendingTopics'
}
feeds = {

"link" : "http://www.sciencenews.org/view/feed/type/news/name/articles.rss",
"title" : "Science News",
"description" : "News about science"
}
sql =  "INSERT INTO source(title, \
       description, link, date) \
       VALUES ('%s', '%s', '%s', '%s' )" % \
       (feeds['title'], feeds['description'], feeds['link'], datetime.datetime.now())
try:
    con = mdb.connect(mysql_conn['host'], mysql_conn['username'], mysql_conn['password'], mysql_conn['db'])
    cur = con.cursor()
    feedTitle = feeds['title']
    cur.execute(sql)
    con.commit()
    con.close()
    print "Record inserted into database..."
except RuntimeError as error:
    print error


