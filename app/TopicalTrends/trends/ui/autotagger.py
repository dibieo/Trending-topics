# -*- coding: utf-8 -*-
import urllib
from xml.dom import minidom #got the idea from http://developer.yahoo.com/python/python-xml.html
import MySQLdb as mdb #using mysqldb according to http://mysql-python.sourceforge.net/MySQLdb.html
import datetime
from DBConf import DBConf as dbc
from MyConf import MyConf as params
from MLStripper import strip_tags
from TimeoutException import timeout
import re
import pdb


#the stop regex pattern list works like this:
# [(<'the rss feed1's base url'>),('stopPattern1 | stopPattern2 | ... '),
# (<'the rss feed2's base url'>),('stopPattern2),
# put more rss feeds and stop words here]
#what it does is when tagging feed items from a feed, it ignores certain words that occur in that feed a lot and might throw off our frequent items and itemsets
#note: for a more general filter see filterTitleDescription below
stopLists = [
(('news.cnet.com'),('(c|C)net')),
(('feeds.reuters.com'),('(r|R)euters')),
(('feeds.technologyreview.com'),('(t|T)r35')),
(('bbc.co'),('bbc|BBC'))]

@timeout(params.timeout, None)  # timeout this function if it takes more than params.timeout
def wikify(url):
    return minidom.parse(urllib.urlopen (url))

#uses the services described here: http://wdm.cs.waikato.ac.nz:8080/services/?suggest

#uses the wikify service to autotag a feeditem and update the database accordingly
def insert_feeditem_tags(feeditem_id):
    #get feed_item from our db, get title and description of item and use it as text to be wikified
    conn = mdb.connect(dbc.host, dbc.user, dbc.passwrd, dbc.db, charset="utf8")
    c = conn.cursor()
    c.execute("""SELECT title, description, link FROM feeditem
                      WHERE id = %s """, int(feeditem_id),)
    row = c.fetchone()
    item_title = strip_tags(row[0])
    item_desc = strip_tags(row[1])
    item_url = row[2]
    textToWikify = filterTitleDescription(item_title, item_desc)
    textToWikify = urllib.quote_plus(textToWikify.encode('utf-8'))  # replace special chars in string using %xx escape

    #remove stop words for this feed from text to be wikfied, usually feed specific stopwords are those that are repeated a lot in some feed, like the name of a news agency in its own articles
    for stopList in stopLists:
        if(item_url.lower() in stopList[0].lower()): #if the base url of feed is in feed item url, ie ths item belongs to that feed
            print('textToWikify before:')
            print(textToWikify)
            textToWikify = re.sub(stopList[1], '', textToWikify)
            
            print('textToWikify after:')
            print(textToWikify)

            
            
    #call wikify
    url = params.baseUrl + 'wikify?minProbability=' + params.minProbability + '&repeatMode=' + params.repeatMode + '&source=' + textToWikify
    
    #if not isinstance(url,unicode):
    url = url.encode('utf8')

    dom = None
    try:
        dom = wikify(url)
    except:
        pass

    if dom: # if wikifier successfully wikified the source and no timeout occurred
        topics = dom.getElementsByTagName('DetectedTopic')
        
        for topic in topics:
            topic_title = topic.getAttribute('title')
            topic_id_miner = topic.getAttribute('id') #the id that wikipediaminer associates with each wikipedia topic
            topic_weight = topic.getAttribute('weight')
            
            #store this tag(ie topic) in the tags table if not already there
            #first check to see if tag already exists in tag table
            try: 
                c.execute("""SELECT * FROM tag WHERE title = %s""", (topic_title,))
                tag = c.fetchone()
                # if this tag doesn't exist already insert it
                if(tag == None):
                    c.execute('SELECT id FROM tag WHERE title = %s', (topic_title,))
                    if len(c.fetchall()) == 0:
                        c.execute(
                              """INSERT INTO tag (title, 
                                                  url,
                                                  count, 
                                                  date, 
                                                  id_miner)
                                 VALUES (%s, %s, %s, %s, %s)""",
                                                (topic_title,
                                                  "http://en.wikipedia.org/wiki/" + topic_title, #url is null for now since wikifier doesn't return a url but it can be inferred from title
                                                  1,
                                                  datetime.datetime.now(),
                                                  topic_id_miner,) 
                                                )
                else:
                    print("tag already exists: " + topic_title)
                    #soheilTODO increment count indicating this tag has been seen again
        
                #do another select to get the tag_id to be associated with the feed_item
                c.execute("""SELECT * FROM tag WHERE title = %s""", (topic_title,))
                tag = c.fetchone()
                tag_id = tag[0] 
                        
                #associate the tag with the feeditem
                c.execute(
                      """INSERT INTO feeditem_tag (feeditem_id,
                                                   tag_id,
                                                   date,
                                                   weight_miner)
                         VALUES (%s, %s, %s, %s)""",
                                                 (feeditem_id,
                                                   tag_id,
                                                   datetime.datetime.now(),
                                                   topic_weight,) 
                                                 )
            except RuntimeError as error:
                print error
                conn.commit()
                c.close()                
                conn.close()
    
        
        conn.commit()
        c.close()
        conn.close() 
        return topics
    else:
        print "WARNING: Wikifier timed out on feeditem with id %s. Feeditem was deleted." % feeditem_id
        conn = mdb.connect(dbc.host, dbc.user, dbc.passwrd, dbc.db, charset="utf8")
        c = conn.cursor()
        try:
            c.execute('DELETE FROM feeditem WHERE id = %s', (feeditem_id,))
            conn.commit()
            c.close()
            conn.close()
        except RuntimeError as error:
            print error
            conn.commit()
            c.close()                
            conn.close()   
    
def getAllTopics(textToWikify):
    #call wikify
    url = params.baseUrl + 'wikify?source='
    dom = minidom.parse(urllib.urlopen (url + textToWikify))
    print(dom)
    print(url + textToWikify)
    topics = dom.getElementsByTagName('detectedTopic')

    #print tsgs to console
    for topic in topics:
        topic_string = topic.getAttribute('title')
        print(topic_string)

    return topics
    
def getSortedPairwiseRelatednesses(text):    
    url = 'compare?ids1='
    #topicDifferences = []
    allTopics = getAllTopics(text)
    
    for topic in allTopics:
        url = url + topic.getAttribute('id') + ','
    
    #get rid of the extra comma at the end
    url = url[:-1]
    url = url + '&ids2='
    for topic in allTopics:
        url = url + topic.getAttribute('id') + ','
    url = url[:-1]
    url = url + '&titles'
    
    #soheilTodo delete later
    print(params.baseUrl + url)
    #use the compare service, with many to many topic comparison
    dom = minidom.parse(urllib.urlopen(params.baseUrl + url))
    
    topicRelatednesses = dom.getElementsByTagName("Measure")
    
    sortedRelatednesses = sorted(topicRelatednesses, key=lambda measure:measure.firstChild.nodeValue)
    printComparisonResults(sortedRelatednesses)
    return sortedRelatednesses
    
def printComparisonResults(comparisons):
    for c in comparisons:       
        print("t1:" + c.getAttribute('highTitle') + " t2:" + c.getAttribute('lowTitle') + " relatedness measure:" + c.firstChild.nodeValue)
        
def getFileTopics(filePath):
    f = open(filePath)
    text = ""
    for line in f:
        text = text + line
        
    getSortedPairwiseRelatednesses(text)


#a rule based filter, for example if the frist 5 words of the description contian 'Reuters'

#note: this general filter applies to things that the feed specific stopWordList (look above) doesn't catch. for example reuter is mentioned the beginning of descriptions of items in yahoo news and other feeds (not just reuter itself, when reuter is mentioned in the descriptions of reuter's rss feeds the stop word list catches those)
 
# give it title and description, it will filter, concatenate and return them
def filterTitleDescription(title, description):
    
    #filtering the description
    count = 1;
    filteredDesc = ' '  
    for word in description.split():        
        #eliminate reuter as source mentions at the beginning of descriptions
        if(count <= 10):
            word = re.sub('(R|r)euters | (C|c)net | bbc | BBC', '', word)
        
        filteredDesc = filteredDesc + word +' '
        count+=1
    
    count = 1;
    filteredTitle = ''
    for word in title.split():        
        #eliminate reuter as source mentions at the beginning of descriptions
        if(count <= 10):
            word = re.sub('(R|r)euters | (C|c)net | bbc | BBC', '', word)
        
        filteredTitle = filteredTitle + word +' '
        count+=1
        
    return filteredTitle + ' ' + filteredDesc #no filtering on title right now
        
    



    
#here's how this method works:
#what's passed in is a list of topics compared pairwise and sorted based on the relatedness of the topic pairs
#the topic pairs with the highest levels of relatedness are considered to be the cores or seeds from which the topic set will be grown
# for each topic not already inside the selected topics set
# sum relatedness to all topics already selected
# the topic with the greatest sum is our candidate for inclusion in the set
# we can divide this by some function of the number of topics already in the set to punish for size increase  
#def growTopicSet(sortedPairwiseRelatednesses, topics):
    #alreadySelectedTopics = []
    #alreadySelectedTopics[0] =  sortedPairwiseRelatednesses[]  #note development has stopped right here, uncommenting this will give you a bug due to empty []
    
    
    
    
    
    
#   <WikipediaMiner service="/services/compare">
#   <Request ids1="17362" ids2="711147,89074,89073" titles="true"/>
#   <Response>
#   <Measures>
#   <Measure highId="89073" highTitle="Kea" lowId="17362" lowTitle="Kiwi">0.721</Measure>
#   <Measure highId="89074" highTitle="Kakapo" lowId="17362" lowTitle="Kiwi">0.789</Measure>
#   <Measure highId="711147" highTitle="Takahē" lowId="17362" lowTitle="Kiwi">0</Measure>
#   </Measures>
#   </Response>
#   </WikipediaMiner>

     
        
    
        
    
            
            
        
    

            
        
        
        
        
        
