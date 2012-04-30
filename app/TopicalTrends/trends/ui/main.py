'''
Created on Mar 31, 2012

@author: houman
'''


from Analysis import Analysis
import datetime
from datetime import timedelta
#from pyparsing import Combine soheil: not seeing this getting used anywhere, and giving error that module doesn't exist so commenting out to see if it works -- and it Did work fine with this commented out

if __name__ == '__main__':
    pass

#print report
query = 'Reuters'
#time1 = '2012-04-20 00:00:00'
#time2 = '2013-04-25 08:00:00'
#time11 = '2012-04-25 08:00:00'
#time22 = '2013-04-30 00:00:00'

time2 = datetime.datetime.now() 
time1 = time2 - timedelta(days=20)
time22 = time1
time11 = time22 - timedelta(days=20)

print 'getFreqTopics:'
print Analysis.getFreqTopics(time1, time2, minFreq=10, k=0)

print '\ngetFreqTopicSets:'
print Analysis.getFreqTopicSets(query, time1, time2)

print '\ngetTopicFrequency:'
print Analysis.getTopicFrequency(query, time1, time2)

print '\ngetHotTopics:'
topics = Analysis.getHotTopics(10, time1, time2)
print topics

print '\ngetTopicsFrequencyChanges:'
print Analysis.getTopicsFrequencyChanges(topics, time11, time22)


#print strt(datetime.combine(datetime.now(),, - datetime.now()))
