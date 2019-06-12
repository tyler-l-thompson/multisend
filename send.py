#!/usr/bin/python
'''
Created on Aug 2, 2017

@author: Tyler Thompson
'''

import optparse,sys,os
from Classes import Tools,Computers

tools = Tools.Tools()
cd = None

configFilePath = "/alva/LabInfo/json/C-220.json"
serverConfigFilePath = "/alva/ServerInfo/multisend/serverinfo.json"

def main():
    args = getArgs()
    #print "DEBUG ARGS: " + str(args)

    #-f alternate config file
    global configFilePath
    if args.f != False:
        configFilePath = args.f

    #set the server config file if the user puts it in server mode.
    if args.s != False:
        if os.path.isfile(serverConfigFilePath):
            configFilePath = serverConfigFilePath
        else:
            configFilePath = "/etc/ControlStation/ServerInfo/multisend/serverinfo.json"

    global cd
    cd = Computers.Computers(configFilePath=configFilePath)

    # limit list of computers to that specified
    cd.setRange(idRange=args.n)
    cd.setList(idList=args.m)

    #-p prints the config
    if args.p == True:
        print "\nConfig File: " + configFilePath
        tools.prettyPrintObjects(objects=cd.computers, title="C-220 Computers", objFilter="dest,src,ping,idFile,functionReturn,dfstatus,cmd")
        sys.exit(0)

    #--rename
    if args.rename == True:
        cmd = "scutil --set HostName "
        if not args.y:
            confirmSend(cmd=cmd)
        cd.sendSshToAllThreaded(cmd=cmd, user=args.u, idFile=args.i, rename=True)
        sys.exit(0)

    #--rsync
    elif args.rsync != False:
        if args.src == False or args.dest == False:
            print "--rsync must be used with --src and --dest. Use --help to see usage."
            sys.exit(0)
        if not args.y:
            confirmSend(cmd="rsync")
        cd.sendFileToAllThreaded(src=args.src, dest=args.dest, user=args.u, idfile=args.i)

    #-c command to remote execute
    elif args.c != None:
        if not args.y:
            confirmSend(cmd=args.c)
        cd.sendSshToAllThreaded(cmd=args.c, user=args.u, idFile=args.i)

    #--dffreeze DeepFreeze Freeze
    elif args.dffreeze == True:
        # cmd = "DFXPSWD=" + args.dfpass + " '/Library/Application Support/Faronics/Deep Freeze/deepfreeze' -u " + args.dfuser + " -p bootFrozen"
        cmd = "DFXPSWD={0} /usr/local/bin/deepfreeze freeze --env".format(args.dfpass)
        if not args.y:
            confirmSend(cmd=cmd)
        cd.sendSshToAllThreaded(cmd=cmd, user=args.u, idFile=args.i)

    #--dfthaw DeepFreeze Thaw
    elif args.dfthaw == True:
        # cmd = "DFXPSWD=" + args.dfpass + " '/Library/Application Support/Faronics/Deep Freeze/deepfreeze' -u " + args.dfuser + " -p bootThawed"
        cmd = "DFXPSWD={0} /usr/local/bin/deepfreeze thaw --env".format(args.dfpass)
        if not args.y:
            confirmSend(cmd=cmd)
        cd.sendSshToAllThreaded(cmd=cmd, user=args.u, idFile=args.i)

    #--dfstatus DeepFreeze Status
    elif args.dfstatus == True:
        # cmd = "DFXPSWD=" + args.dfpass + " '/Library/Application Support/Faronics/Deep Freeze/deepfreeze' -u " + args.dfuser + " -p status"
        cmd = "DFXPSWD={0} /usr/local/bin/deepfreeze status --env".format(args.dfpass)
        if not args.y:
            confirmSend(cmd=cmd)
        cd.sendSshToAllThreaded(cmd=cmd, user=args.u, idFile=args.i, dfstatus=True)

    #--shutdown shutdown computers
    if args.shutdown == True:
        cmd = "shutdown -h now"
        if not args.y:
            confirmSend(cmd=cmd)
        cd.sendSshToAllThreaded(cmd=cmd, user=args.u, idFile=args.i)

    #--reboot reboot computers
    elif args.reboot == True:
        cmd = "reboot"
        if not args.y:
            confirmSend(cmd=cmd)
        cd.sendSshToAllThreaded(cmd=cmd, user=args.u, idFile=args.i)

    sys.exit(0)


def confirmSend(cmd):
    yesCmd = "yeah bro"
    noCmd = "nah man"
    print "\nPreparing to send terminal command '" + cmd + "' to the following computers:"
    tools.prettyPrintObjects(objects=cd.computers, title="Targeted Computers", objFilter="src,dest,cmd,ping,idFile,functionReturn,dfstatus")
    while True:
        userInput = raw_input("Are you sure you want to send the command? [ " + yesCmd + " | " + noCmd + " ]\n>> ")
        if userInput != yesCmd and userInput != noCmd:
            print "Please specify '" + yesCmd + "' or '" + noCmd + "'"
        if userInput == noCmd:
            print "Thats cool..."
            sys.exit(0)
        if userInput == yesCmd:
            print "Hell yeah, lets do this!"
            break



def getArgs():
    parser = optparse.OptionParser(usage='%prog -c <COMMAND> [options]',description="C-220 SSH Send. Send a terminal command to all the computers in C-220. Optionally you can send a command to a single computer or a range of computers.")
    parser.add_option('-y', action="store_true", default=False, help="Suppress confirmation prompt.")
    parser.add_option('-c', action="store", help="Command to send")
    parser.add_option('-u', action="store", default="root", help="User to send command as. Default: root")
    parser.add_option('-i', action="store", default="~/.ssh/id_rsa", help="Identity file to use. Default: ~/.ssh/id_rsa")
    parser.add_option('-n', action="store", default=False, help="Set a range of computers to send command to. ie. 00-06")
    parser.add_option('-m', action="store", default=False, help="Set comma delimited list of computers to send command to. ie. 03,05,10,23")
    parser.add_option('-p', action="store_true", default=False, help="Print the config and exit.")
    parser.add_option('-f', action="store", default=False, help="Specify a different config file to read. Default: " + configFilePath)
    parser.add_option('-s', action="store_true", default=False, help="Use the server config instead. Default: " + serverConfigFilePath)
    parser.add_option('--rename', action="store_true", default=False, help="Rename the computer's hostname to the one specified in the config file.")
    parser.add_option('--dffreeze', action="store_true", default=False, help="DeepFreeze: Freeze specified computers.")
    parser.add_option('--dfthaw', action="store_true", default=False, help="DeepFreeze: Thaw specified computers")
    parser.add_option('--dfstatus', action="store_true", default=False, help="DeepFreeze: Get DeepFreeze status")
    parser.add_option('--dfuser', action="store", default="admin", help="DeepFreeze: The DeepFreeze user. Default: admin")
    parser.add_option('--dfpass', action="store", default="youshallnotpass", help="DeepFreeze: The DeepFreeze password. Default: youshallnotpass")
    parser.add_option('--rsync', action="store_true", default=False, help="Send a file unsing rsync to the remote host(s)")
    parser.add_option('--src', action="store", default=False, help="Source file to send. Must be used with --rsync")
    parser.add_option('--dest', action="store", default=False, help="Destination for file being sent. Must be used with --rsync")
    parser.add_option('--shutdown', action="store_true", default=False, help="Shutdown the specified computers. Can be used consecutively with other commands.")
    parser.add_option('--reboot', action="store_true", default=False, help="Reboot the specified computers. Can be used consecutively with other commands.")
    options, args = parser.parse_args()
    return options


if __name__ == '__main__':
    main()
