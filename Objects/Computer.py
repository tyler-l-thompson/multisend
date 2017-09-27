'''
Created on Aug 2, 2017

@author: Tyler Thompson
'''

class Computer(object):
    '''
    classdocs
    '''


    def __init__(self, id, hostname, mac, ip, assettag, cmd=None, idFile=None, functionReturn=None, dfstatus=False, ping=True, src=None, dest=None):
        '''
        Constructor
        '''
        self.id = id
        self.hostname = hostname
        self.mac = mac
        self.ip = ip
        self.ping = ping
        self.assettag = assettag
        self.cmd = cmd
        self.idFile = idFile
        self.functionReturn = functionReturn
        self.dfstatus = dfstatus
        self.src = src
        self.dest = dest