'''
Created on Apr 6, 2012

@author: houman
'''

class MyConf:
    '''
        contains all program specific configuration parameters
        this parameters are machine independent (unlike DBConf's parameters)
        and control how system works
        
    '''

    #baseUrl = "http://wikipedia-miner.cms.waikato.ac.nz/services/"
    # Wikiminer parameters
    baseUrl = 'http://ec2-50-112-73-48.us-west-2.compute.amazonaws.com:8080/wikiminer/services/'
    minProbability = '0.1'
    repeatMode = 'FIRST_IN_REGION' # 'ALL'
    
    timeout = 20 # the maximum period of time a feed's url is allowed to take to load

    maxAllowedSupport = 10 # start with this support and reduce it until it is lees than minSupport or # of frequent topic sets found is less than minFreqTopicSetsCount
    minAllowedSupport = 3 # min support used in finding frequent topic sets
    minFreqTopicSetsCount = 100
    days = 1 # the number of past days over which frequent topic sets are discovered
    maxFreqTopics = 100 # the number of freq topics to be shown on the left bar of the page    
    
    output = True   # enable/disable terminal output