'''
Created on Mar 31, 2012

@author: houman
'''

class MyUtilities(object):
    '''
        contains all general functions which could be called by any class
        
        NOTE: all functions of this class are static
    '''

    @staticmethod
    def sortDicByVal(dic):
        ''' Returns input dictionary dic sorted by their values in ascending order '''
        return sorted(dic.items(), key=lambda (k, v): (v, k))

    @staticmethod
    def sortTupleListByVal(l):
        ''' Returns input list of tuples l sorted by their values
            input: like [(k1, v1), ...]
            input: similar to input but sorted in ascending order by keys
        '''
        return sorted(l, key=lambda (k, v): (v, k))
    
    @staticmethod
    def sortDicByKeyLen(dic):
        ''' Returns input dictionary dic sorted by length of the keys in ascending order '''
        return sorted(dic.items(), key=lambda (k, v): len(k))
    
