'''
Created on Aug 2, 2017

@author: Tyler Thompson
'''

class SshSendStatus(object):
    '''
    classdocs
    '''


    def __init__(self, id, ip, user, ping, sshReturn=None):
        '''
        Constructor
        '''
        self.id = id
        self.ip = ip
        self.user = user
        self.ping = ping
        self.sshReturn = sshReturn
