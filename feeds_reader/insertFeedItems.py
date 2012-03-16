import feedparser
import MySQLdb
import MySQLdb as mdb
import datetime
import time



#This function inserts items into the feed item table
def insert_feeditems(feed_id, url, con):
    feed = feedparser.parse(url)

    print "Feed title :" + feed.feed.title
    print  "Feed description: " + feed.feed.description
    print  "Feed link: " + feed.feed.link
    print  "Language: " + feed.feed.language
    for f in  feed.entries:
        print f
        #@Todo: Not sure how to convert the date into a datetime object properly. Using default values right now
        #pub_date = datetime.datetime.strptime(f.updated, "%a, %d %b %Y %H:%M:%S ")
        sql =  "INSERT INTO feed_item(title, \
       description, link, guid,  pub_date, date, feed_id) \
       VALUES ('%s', '%s', '%s', '%s' , '%s', '%s',  '%d')" % \
       (f.title, f.description, f.link, f.guid, datetime.datetime.now(), datetime.datetime.now(), feed_id)
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
        con.close()
        print "Feed Item inserted"
        print "Item title: " + f.title
        print "Item description: " + f.description
        print "Item author: " + f.author
        print "Item Guid: " + f.guid
        print "Item link: " + f.link
        print "pub Date:  " + f.updated
 
sql =  "Select * from source"
mysql_conn = {
    'host' : 'localhost',
    'username' : 'root',
    'password': 'password',
    'db' : 'trendingTopics'
}

try:
    con = mdb.connect(mysql_conn['host'], mysql_conn['username'], mysql_conn['password'], mysql_conn['db'])
    cursor = con.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for r in rows:
        insert_feeditems(r[0], r[3], con)
except RuntimeError as error:
    print error




#This function inserts the items in the feed
