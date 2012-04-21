import feedparser 
import MySQLdb as mdb
import autotagger
from TopicalTrends.DBConf import DBConf as dbc
import hashlib
from TopicalTrends.MyConf import MyConf as params
from TopicalTrends.TimeoutException import  timeout

@timeout(params.timeout, None) # timeout this function if it takes more than params.timeout
def parseUrl(url):
    return feedparser.parse(url)

#This function inserts items into the feed item table
def insert_feeditems(feed_id, url):   
    
    if params.output:
        print 'Loading %s' % url
    feed = parseUrl(url)
    if feed.feed: # feed was available and timeout did not occur
    
        #print "Feed title :" + feed.feed.title + "\n"
        #print "Feed description: " + feed.feed.description + "\n"
        #print "Feed link: " + feed.feed.link + "\n"
        #print "Language: " + feed.feed.language + "\n"
        
        for f in feed.entries:
            conn = mdb.connect(dbc.host, dbc.user, dbc.passwrd, dbc.db, charset="utf8")
            c = conn.cursor()
            link = ''
            guid = ''
            hash = ''
            if 'link' in f:
                if len(f.link) > 0:
                    link = f.link
                    h = hashlib.sha512()
                    h.update(str(link))
                    hash = h.hexdigest()
            if 'guid' in f:
                if len(f.guid) > 0:
                    guid = f.guid
                    h = hashlib.sha512()
                    h.update(str(guid))
                    hash = h.hexdigest()                
            if len(hash) > 0:
                if 'title' in f and 'description'in f:
                    pubDate = ''
                    if 'pubDate' in f:
                        pubDate = f.pubDate
                    try:
                        c.execute('SELECT id FROM feeditem WHERE hash = %s', (hash))
                        if len(c.fetchall()) == 0:
                            c.execute("""INSERT feeditem (title,
                                                            description,
                                                            link,
                                                            guid,
                                                            hash,
                                                            pub_date,                                            
                                                            feed_id)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                                           (f.title,
                                                            f.description,
                                                            link,
                                                            guid,
                                                            hash,
                                                            pubDate,
                                                            feed_id,) #soheilTODO replace datetime.now (not sure which one) with pub_date 
                                                           )
                            #print 'new feeditem!'
                        feeditem_id = c.lastrowid  # get the id of last inserted row              
                    except RuntimeError as error:
                        print error
                        conn.commit()
                        c.close()                
                        conn.close()
                    conn.commit()
                    c.close()
                    conn.close()
                    #autotag this feed item and update database if it's not already in there
                    #print feeditem_id
                    if feeditem_id > 0:
                        autotagger.insert_feeditem_tags(feeditem_id)
            else:
                print 'feeditem ignored: no guid, no link!'        
    else:
        print 'WARNING feed url timed out %s ' % (url,)

sql = "Select id, link from feed "

try:
    conn = mdb.connect(dbc.host, dbc.user, dbc.passwrd, dbc.db, charset="utf8")
    c = conn.cursor()
    c.execute(sql) 
    rows = c.fetchall()
    
except RuntimeError as error:
    print error
    c.close()
    conn.close()
c.close()
conn.close()

index = 0.
for r in rows:
    insert_feeditems(r[0], r[1])       
    index += 1
    if params.output:
        print str(round((index / len(rows)) * 100.0, 1)) + '% completed ...' 

#This function inserts the items in the feed


    
