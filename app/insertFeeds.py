#! /usr/bin/python

#This file includes methods for inserting feeds into the database
#Feeds are inserted manually, but may be processed from a form or another input source in the future

import MySQLdb as mdb
import sys
import datetime

#Settings for the mysql connection
#soheilTODO put mysql conn config stuff in a config file so it could be different for each of us
mysql_conn = {
    'host' : 'localhost',
    'username' : 'root',
    'password': '',
    'db' : 'TopicalTrending'
}

#soheilTODO we shuold only get the link, the title and description can be gotten from rss itself
#feeds = {
#"link" : "http://www.sciencenews.org/view/feed/type/news/name/articles.rss",
#"title" : "Science News",
#"description" : "News about science"
#}

feed_links = (
["http://www.sciencenews.org/view/feed/type/news/name/articles.rss"],
["http://www.physorg.com/rss-feed/"],
["http://feeds.feedburner.com/TechCrunch/"]
)



#sql =  "INSERT INTO source(title, \
#       description, link, date) \
#       VALUES ('%s', '%s', '%s', '%s' )" % \
#       (feeds['title'], feeds['description'], feeds['link'], datetime.datetime.now())
try:    
    con = mdb.connect(mysql_conn['host'], mysql_conn['username'], mysql_conn['password'],           mysql_conn['db'], charset = "utf8")
    cursor = con.cursor()

    #insert the feed links and into source table #soheilTODO: have to add link title, description and some date later on when we are actually reading the feed
    for link in feed_links:
        print(link)
        cursor.executemany("""INSERT INTO source (link) VALUES (%s)""",[( link)])

    con.commit()
    con.close()
    print "Feeds inserted into database source table..."
except RuntimeError as error:
    print error


