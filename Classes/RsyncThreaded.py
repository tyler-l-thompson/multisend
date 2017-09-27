'''
Created on Sept 25, 2017

@author: Tyler Thompson
'''

import Tools, threading

class RsyncThreaded(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, computer):
        threading.Thread.__init__(self)
        self.id = computer.id
        self.computer = computer
        self.tools = Tools.Tools()

    def run(self):
        if self.tools.getPing(ip=self.computer.ip) == True:
            self.computer.functionReturn=(str(self.tools.sendFile(user=self.computer.user, ip=self.computer.ip, src=self.computer.src, dest=self.computer.dest, idFile=self.computer.idFile)))
        else:
            self.computer.functionReturn=("Host Down.")
            self.computer.ping = False

    def join(self):
        return self.computer