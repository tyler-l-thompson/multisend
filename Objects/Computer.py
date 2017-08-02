'''
Created on Aug 2, 2017

@author: Tyler Thompson
'''

class Computer(object):
    '''
    classdocs
    '''


    def __init__(self, id, hostname, mac, ip, assettag):
        '''
        Constructor
        '''
        self.id = id
        self.hostname = hostname
        self.mac = mac
        self.ip = ip
        self.assettag = assettag