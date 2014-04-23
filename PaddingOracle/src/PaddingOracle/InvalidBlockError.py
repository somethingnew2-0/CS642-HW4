'''
Created on Jul 4, 2010

@author: eloi
'''

class InvalidBlockError(Exception):
    '''
    classdocs
    '''

    

    def __init__(self, expectedSize, receivedSize):
        self.expected = expectedSize
        self.received = receivedSize
    def __str__(self):
        return "Invalid block size: "+self.received+" bytes. Block must be "+self.expected+" bytes long."