'''
Created on Aug 2, 2017

@author: Tyler Thompson
'''

class SendStatus(object):
    '''
    classdocs
    '''


    def __init__(self, id, ip, user, ping, idfile=None, cmd=None, functionReturn=None, dfstatus=False):
        '''
        Constructor
        '''
        self.id = id
        self.ip = ip
        self.user = user
        self.ping = ping
        self.cmd = cmd
        self.idfile = idfile
        self.functionReturn = functionReturn
        self.dfstatus = dfstatus
