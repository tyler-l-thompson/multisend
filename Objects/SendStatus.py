'''
Created on Aug 2, 2017

@author: Tyler Thompson
'''

class SendStatus(object):
    '''
    classdocs
    '''


    def __init__(self, id, ip, user, ping, functionReturn=None):
        '''
        Constructor
        '''
        self.id = id
        self.ip = ip
        self.user = user
        self.ping = ping
        self.functionReturn = functionReturn
