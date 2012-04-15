'''
Created on Mar 31, 2012

@author: houman
'''

from Analysis import Analysis


if __name__ == '__main__':
    pass


#print report

results = Analysis.getFreqTopics(3, 0)
print Analysis.getFreqfeeditemTopics(2, 1, 'mathematics')
