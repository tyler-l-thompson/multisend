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
        if self.tools.getPing(ip=self.computer.ip) == True:
            self.computer.functionReturn=(str(self.tools.sendSsh(user=self.computer.user, ip=self.computer.ip, cmd=self.computer.cmd))).replace("\n", "").replace("\t", "").replace(" ", "")

            # detect if reading a deep freeze status report
            if self.computer.dfstatus == True:
                if "BOOTFROZEN" in self.computer.functionReturn:
                    self.computer.functionReturn = "FROZEN"
                elif "BOOTTHAWED" in self.computer.functionReturn:
                    self.computer.functionReturn = "THAWED"
                else:
                    self.computer.functionReturn = "UNKNOWN"

            maxReturnLength = 60
            if len(self.computer.functionReturn) > maxReturnLength:
                self.computer.functionReturn = self.computer.functionReturn[:maxReturnLength - 3] + "..."

            if "timed out" in self.computer.functionReturn:
                self.computer.functionReturn = ("Connection timed out.")

        else:
            self.computer.functionReturn=("Host Down.")
            self.computer.ping = False

    def join(self):
        return self.computer