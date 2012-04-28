#! /usr/bin/python

#This file includes methods for inserting feeds into the database
#Feeds are inserted manually, but may be processed from a form or another input source in the future

import MySQLdb as mdb
from DBConf import DBConf as dbc
import hashlib

#soheilTODO we shuold only get the link, the title and description can be gotten from rss itself
#feeds = {
#"link" : "http://www.sciencenews.org/view/feed/type/news/name/articles.rss",
#"title" : "Science News",
#"description" : "News about science"
#}

# duplicates will be ignored at database insertion time (unique index is in use) 
feed_links = ()
f = open('rss_feeds', 'r')
for line in f:
	feed_links.append(line)

#sql =  "INSERT INTO source(title, \
#       description, link, date) \
#       VALUES ('%s', '%s', '%s', '%s' )" % \
#       (feeds['title'], feeds['description'], feeds['link'], datetime.datetime.now())
try:    
    con = mdb.connect(dbc.host, dbc.user, dbc.passwrd, dbc.db, charset="utf8")
    cursor = con.cursor()
    
    linkCount = 0
    #insert the feed links and into source table #soheilTODO: have to add link title, description and some date later on when we are actually reading the feed
    for link in feed_links:
        print str(link)
        h = hashlib.sha512()
        h.update(str(link))
        linkHash = h.hexdigest()
        cursor.executemany("""INSERT IGNORE INTO feed (link, link_hash) VALUES (%s, %s)""", [(link, linkHash)])
        linkCount += 1

    con.commit()
    con.close()
    print "\nNew feeds inserted into database source table (repeated links were ignored) ..."
    print "Total: %s" % linkCount
except RuntimeError as error:
    print error


