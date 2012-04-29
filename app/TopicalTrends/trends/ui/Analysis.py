'''
Created on Mar 31, 2012

@author: houman
'''
import MySQLdb as mdb
import itemmining
from DBConf import DBConf as dbc
from MyUtilities import MyUtilities
from MyConf import MyConf as params

class Analysis(object):
    ''' Handles analysis of our data
        
        NOTE: All functions of this class are static.
    '''
    
    @staticmethod
    def getFreqTopics(time1, time2, minFreq=0, k=0):
        ''' Returns top k frequent topics among feeditems stored from time1 to time2
            with a minimum frequency of minFreq.
            k = 0 means return all
            
            output:
            A list like [[topic1, freq1], [topic2, freq2], ...] in which
            most frequent topic is at the beginning 
        '''
            
        try:
            db = mdb.Connect(dbc.host,
                                 dbc.user,
                                 dbc.passwrd,
                                 dbc.db)
            c = db.cursor()
            query = '''SELECT t.title, count( fit.feeditem_id ) count
                       FROM `tag` t INNER JOIN `feeditem_tag` fit ON t.id = fit.tag_id
                       WHERE fit.`date` >=  '%s' AND fit.`date` <= '%s' 
                       GROUP BY t.id''' % (time1, time2)
            if minFreq > 0:
                query += ' HAVING count > %s' % str(minFreq)
            query += ' ORDER BY `count` DESC'
            if k > 0:
                query += ' LIMIT ' + str(k)
            c.execute(query)
            rows = c.fetchall()
            out = []    # output
            for r in rows:
                out.append([r[0], str(r[1])])          
        finally:        
            if db:
                db.commit()
                c.close()
                db.close()
        return out    
        
    @staticmethod
    def getMaximalFreqItemSets(freqTopicSets):
        ''' filters out non-maximal frequent topics in freqTopicSets
            
            output: list of tuples: [([topic1, topic2, ... ], Freq), ...]
        '''
        
        out = []
        for i in range(len(freqTopicSets)):
            maximal = True
            for j in range(i + 1, len(freqTopicSets)):  # compare each set with it's proceeding sets to see if it should be considered or not 
                if set(freqTopicSets[i][0]).issubset(set(freqTopicSets[j][0])): #and freqTopicSets[i][1] == freqTopicSets[j][1]:
                    maximal = False
            if maximal:
                out.append(freqTopicSets[i])
        return out
    
    @staticmethod
    def convetFrozensetToList(frozenSetList):
        ''' convert the input list to another list friendlier for processing
            by converting frozen sets to sets
            
            input: like [(frozenset([topic1, topic2, ...]), freq), ...]
            output: like [([topic1, topic2, ...], freq), ...]
        '''
        out = []
        for topicSets in frozenSetList:
            topicList = []
            for topicSet in topicSets[0]:
                topicList.append(topicSet)
            out.append((topicList, topicSets[1]))
        return out
            
    @staticmethod
    def getFreqTopicSets(query, time1, time2,  minSup=params.maxAllowedSupport, maximal=True): # len is ignored for now
        ''' Returns frequent topic sets containing the query and having a length of len
            and a support value of greater than minSup3
            
            output: list of tuples: [([topic1, topic2, ... ],Freq), ...]
        '''
        sup = minSup
        
        freqTopicSets = []
        while (len(freqTopicSets) < params.minFreqTopicSetsCount and params.minAllowedSupport <= sup): 
            freqTopicSets = []
            try:
                db = mdb.Connect(dbc.host,
                                     dbc.user,
                                     dbc.passwrd,
                                     dbc.db)
                c = db.cursor()
                #Question By Soheil (for Houman): does this query return the set of all tags that co-occur with the query tag but not the query tag itself, along with the id of the feed item that contains that tag?( if so then let's leave the comment cuz i might not remember in the future :) april.24
                c.execute('''SELECT fit.feeditem_id, t.title 
                           FROM `feeditem_tag` fit 
                           INNER JOIN `tag` t ON fit.tag_id = t.id 
                           WHERE t.title != %s AND fit.feeditem_id 
                           IN (SELECT fit.feeditem_id 
                               FROM `feeditem_tag` fit 
                               INNER JOIN `tag` t ON fit.tag_id = t.id
                               WHERE fit.`date` >=  %s AND fit.`date` <= %s AND 
                               t.title = %s) 
                           ORDER BY feeditem_id ASC''', (query, time1, time2, query))
                rows = c.fetchall()
                feeditemTopics = ()
                topicSet = ()
                feeditemID = ''				
                #soheil:making sets of tags that represent a feed item? (note: if this ever becomes an efficiency bottleneck, consider replacing this loop with a GROUP BY feeditem_id in the above sql query)
                for r in rows:
                    if feeditemID == r[0]:
                        topicSet += (r[1],)
                    else:
                        if topicSet:
                            feeditemTopics += ((topicSet),)
                            topicSet = ()
                        feeditemID = r[0]
                        topicSet += (r[1],)
            finally:
                if db:
                    db.commit()
                    c.close()
                    db.close()
            relimInput = itemmining.get_fptree(feeditemTopics)
            freqTopicSets = itemmining.fpgrowth(relimInput, sup)    # find freq topic sets
            freqTopicSets = MyUtilities.sortDicByKeyLen(freqTopicSets) # sort the freq topic sets by frequency and change the data structure
            freqTopicSets = Analysis.convetFrozensetToList(freqTopicSets) # convert the data structure of freq topic sets so they become process friendly
            if maximal:  # ignore non-maximal freq topic sets and return only maximal ones
                freqTopicSets = Analysis.getMaximalFreqItemSets(freqTopicSets)
            freqTopicSets = MyUtilities.sortTupleListByVal(freqTopicSets) # sort the freq topic sets by frequency
            sup -= 1          
        
        return freqTopicSets
    
    @staticmethod
    def getHotTopics(k, time1, time2):
        '''
            Returns k most frequent topics (no topic sets)
            using feeditems stored from time1 to time2 ordered by frequency
            
            output: (('topic1', freq1), ('topic2', freq2), ...)
        '''
        try:
            db = mdb.Connect(dbc.host,
                                 dbc.user,
                                 dbc.passwrd,
                                 dbc.db)
            c = db.cursor()
            c.execute('''SELECT title, count( fit.feeditem_id )
                        FROM `feeditem_tag` fit
                        INNER JOIN `tag` t ON fit.tag_id = t.id
                        WHERE fit.`date` >=  %s AND fit.`date` <= %s
                        GROUP BY t.id
                        ORDER BY count( fit.feeditem_id ) DESC
                        LIMIT %s''', (time1, time2, k))
            rows = c.fetchall()            
        finally:
            db.commit()
            c.close()
            db.close()
        return rows   
    
    @staticmethod
    def getTopicFrequency(topic, time1, time2):
        '''
            Returns the number of occurrences (frequency) of topic
            using feeditems stored from time1 to time2
            
            output: Topic's frequency as an integer
        '''
        try:
            db = mdb.Connect(dbc.host,
                                 dbc.user,
                                 dbc.passwrd,
                                 dbc.db)
            c = db.cursor()
            c.execute(""" SELECT COUNT( fit.feeditem_id ) count 
                        FROM `feeditem_tag` fit
                        INNER JOIN  `tag` t ON fit.tag_id = t.id
                        WHERE fit.`date` >=  %s AND fit.`date` <= %s AND TITLE = %s 
                        ORDER BY COUNT( fit.feeditem_id ) DESC """, (time1, time2, topic))
            rows = c.fetchall()            
        finally:
            if db:
                db.commit()
                c.close()
                db.close()
        freq = rows[0][0]
        return freq
    @staticmethod 
    def getTopicsFrequencyChanges(topics, time1, time2):
        '''
            Returns the changes of frequencies for input topics
            
            input: output of getHotTopics() function
            
            output: [('topic1', <changes on frequency 1>), ('topic2', <changes on frequency 2>), ...]
        '''
        results = []
        for t in topics:
            topic = t[0]
            oldFreq = t[1]
            newFreq = Analysis.getTopicFrequency(topic, time1, time2)
            results.append((topic,str(newFreq-oldFreq)))
        return results