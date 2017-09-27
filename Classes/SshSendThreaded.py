'''
Created on Sept 25, 2017

@author: Tyler Thompson
'''

import Tools, threading

class SshSendThreaded(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, computer):
        threading.Thread.__init__(self)
        self.id = computer.id
        self.computer = computer
        self.tools = Tools.Tools()

    def run(self):
        #print ("Starting " + str(self.id))
        if self.tools.getPing(ip=self.computer.ip) == True:
            self.computer.functionReturn=(str(self.tools.sendSsh(user=self.computer.user, ip=self.computer.ip, cmd=self.computer.cmd)))

            # detect if reading a deep freeze status report
            if self.computer.dfstatus == True:
                if "BOOT FROZEN" in self.computer.functionReturn:
                    self.computer.functionReturn = "FROZEN"
                elif "BOOT THAWED" in self.computer.functionReturn:
                    self.computer.functionReturn = "THAWED"
                else:
                    self.computer.functionReturn = "UNKNOWN"

            if "timed out" in self.computer.functionReturn:
                self.computer.functionReturn = ("Connection timed out.")

        else:
            self.computer.functionReturn=("Host Down.")
            self.computer.ping = False
        #print ("Exiting " + str(self.id))

    def join(self):
        return self.computer