'''
Created on Mar 31, 2012

@author: houman
'''


from Analysis import Analysis
from datetime import datetime
#from pyparsing import Combine soheil: not seeing this getting used anywhere, and giving error that module doesn't exist so commenting out to see if it works -- and it Did work fine with this commented out

if __name__ == '__main__':
    pass

#print report
query = 'Internet'
time1 = '2012-04-20 00:00:00'
time2 = '2013-04-21 08:00:00'
time11 = '2012-04-21 08:00:00'
time22 = '2013-04-22 00:00:00'

print 'getFreqTopics:'
print Analysis.getFreqTopics(time1, time2, minFreq=10, k=0)

print '\ngetFreqTopicSets:'
print Analysis.getFreqTopicSets(query)

print '\ngetTopicFrequency:'
print Analysis.getTopicFrequency(query, time1, time2)

print '\ngetHotTopics:'
topics = Analysis.getHotTopics(10, time1, time2)
print topics

print '\ngetTopicsFrequencyChanges:'
print Analysis.getTopicsFrequencyChanges(topics, time11, time22)


#print strt(datetime.combine(datetime.now(),, - datetime.now()))
