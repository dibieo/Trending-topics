'''
Created on Mar 31, 2012

@author: houman
'''
import MySQLdb as mdb
import itemmining
from DBConf import DBConf as dbc
from MyUtilities import MyUtilities

class Analysis(object):
    ''' Handles analysis of our data
        
        NOTE: All functions of this class are static.
    '''
    
    @staticmethod
    def getFreqTopics(minFreq, k):
        ''' Returns top k frequent topics with a minimum frequency of minFreq.
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
                       GROUP BY t.id'''
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
    def getClosedFreqItemSets(freqTopicSets):
        ''' filters out non-closed frequent topics in freqTopicSets
            
            output: list of tuples: [([topic1, topic2, ... ], Freq), ...]
        '''
        
        out = []
        for i in range(len(freqTopicSets)):
            closed = True
            for j in range(i + 1, len(freqTopicSets)):  # compare each set with it's proceeding sets to see if it should be considered or not 
                if set(freqTopicSets[i][0]).issubset(set(freqTopicSets[j][0])) and freqTopicSets[i][1] == freqTopicSets[j][1]:
                    closed = False
            if closed:
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
    def getFreqfeeditemTopics(len, minSup, query, closed=True): # len is ignored for now
        ''' Returns frequent topic sets containing the query and having a length of len
            and a support value of greater than minSup
            
            output: list of tuples: [([topic1, topic2, ... ],Freq), ...]
        '''
        
        try:
            db = mdb.Connect(dbc.host,
                                 dbc.user,
                                 dbc.passwrd,
                                 dbc.db)
            c = db.cursor()
            query = '''SELECT fit.feeditem_id, t.title 
                       FROM `feeditem_tag` fit 
                       INNER JOIN `tag` t ON fit.tag_id = t.id 
                       WHERE t.title != '%s' AND fit.feeditem_id 
                       IN (SELECT fit.feeditem_id 
                           FROM `feeditem_tag` fit 
                           INNER JOIN `tag` t ON fit.tag_id = t.id 
                           WHERE t.title = '%s') 
                       ORDER BY feeditem_id ASC''' % (query, query)
            c.execute(query)
            rows = c.fetchall()
            feeditemTopics = ()
            topicSet = ()
            feeditemID = ''
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
        relimInput = itemmining.get_relim_input(feeditemTopics)
        freqTopicSets = itemmining.relim(relimInput, minSup)    # fined freq topic sets        
        freqTopicSets = MyUtilities.sortDicByKeyLen(freqTopicSets) # sort the freq topic sets by frequency and change the data structure
        freqTopicSets = Analysis.convetFrozensetToList(freqTopicSets) # convert the data structure of freq topic sets so they become process friendly
        if closed:  # ignore non-closed freq topic sets and return only closed ones
            freqTopicSets = Analysis.getClosedFreqItemSets(freqTopicSets)
        freqTopicSets = MyUtilities.sortTuplesListByVal(freqTopicSets) # sort the freq topic sets by frequency
        return freqTopicSets