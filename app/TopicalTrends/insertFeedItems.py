import feedparser 
import MySQLdb as mdb
import datetime
import autotagger
from TopicalTrends.DBConf import DBConf as dbc

#This function inserts items into the feed item table
def insert_feeditems(feed_id, url):
    feed = feedparser.parse(url)
    
    #print "Feed title :" + feed.feed.title + "\n"
    #print "Feed description: " + feed.feed.description + "\n"
    #print "Feed link: " + feed.feed.link + "\n"
    #print "Language: " + feed.feed.language + "\n"
    
    for f in  feed.entries:
        print f
        #@Todo: Not sure how to convert the date into a datetime object properly. Using default values right now
        #pub_date = datetime.datetime.strptime(f.updated, "%a, %d %b %Y %H:%M:%S ")
        #sql =  "INSERT INTO feed_item(title, \
        #description, link, guid,  pub_date, date, feed_id) \
        #VALUES ('%s', '%s', '%s', '%s' , '%s', '%s',  '%d')" %\
        #(MySQLdb.escape_string(f.title), MySQLdb.escape_string(f.description), MySQLdb.escape_string(f.link), MySQLdb.escape_string(f.guid), datetime.datetime.now(), datetime.datetime.now(), feed_id)
        conn = mdb.connect(dbc.host, dbc.user, dbc.passwrd, dbc.db, charset="utf8")
        cursor = conn.cursor()
        #print("sql>>>>"+MySQLdb.escape_string(sql))
        #cursor.execute(sql)
        
        if 'guid' in f and 'title' in f and 'description'in f:        
            cursor.executemany(
                  """INSERT INTO feed_item (title,
                                            description,
                                            link,
                                            guid,
                                            pub_date,
                                            date,
                                            feed_id)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                          [(f.title,
                                            f.description,
                                            f.link,
                                            f.guid,
                                            datetime.datetime.now(),
                                            datetime.datetime.now(),
                                            feed_id) #soheilTODO replace datetime.now (not sure which one) with pub_date 
                                           ])
            
            #get the id of the feed item just inserted to pass it to insert_feeditem_tags function
            cursor.executemany(
                  """SELECT * FROM feed_item WHERE guid = %s""", (f.guid,))
            feeditem = cursor.fetchone()
            feeditem_id = feeditem[0]
            
            conn.commit()
            conn.close()
    
            #autotag this feed item and update database
            autotagger.insert_feeditem_tags(feeditem_id)
        
sql = "Select * from source WHERE checked = '0' "

try:
    con = mdb.connect(dbc.host, dbc.user, dbc.passwrd, dbc.db, charset="utf8")
    cursor = con.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for r in rows:
        insert_feeditems(r[0], r[3])
except RuntimeError as error:
    print error
    cursor.close()
    con.close()

#This function inserts the items in the feed
