#!/usr/bin/python
'''
Created on Aug 2, 2017

@author: Tyler Thompson
'''

import optparse,sys
from Classes import Tools,Computers

tools = Tools.Tools()
cd = None

configFilePath = "/alva/LabInfo/json/C-220.json"

def main():
    args = getArgs()
    #print "DEBUG ARGS: " + str(args)

    global configFilePath
    if args.f != False:
        configFilePath = args.f

    global cd
    cd = Computers.Computers(configFilePath=configFilePath)

    if args.p == True:
        print "\nConfig File: " + configFilePath
        tools.prettyPrintObjects(objects=cd.computers, title="C-220 Computers")
        sys.exit(0)

    # limit list of computers to that specified
    cd.setRange(idRange=args.n)
    cd.setList(idList=args.m)

    if args.rsync != False:
        if args.src == False or args.dest == False:
            print "--rsync must be used with --src and --dest. Use --help to see usage."
            sys.exit(0)
        confirmSend(cmd="rsync")
        cd.sendFileToAll(src=args.src, dest=args.dest, user=args.u, idfile=args.i)
        sys.exit(0)

    elif args.c != None:
        confirmSend(cmd=args.c)
        cd.sendSshToAll(cmd=args.c, user=args.u, idFile=args.i)
        sys.exit(0)

    elif args.dffreeze == True:
        cmd = "DFXPSWD=" + args.dfpass + " '/Library/Application Support/Faronics/DeepFreeze/deepfreeze' -u " + args.dfuser + " -p bootFrozen"
        confirmSend(cmd=cmd)
        cd.sendSshToAll(cmd=cmd, user=args.u, idFile=args.i)
        sys.exit(0)

    elif args.dfthaw == True:
        cmd = "DFXPSWD=" + args.dfpass + " '/Library/Application Support/Faronics/DeepFreeze/deepfreeze' -u " + args.dfuser + " -p bootThawed"
        confirmSend(cmd=cmd)
        cd.sendSshToAll(cmd=cmd, user=args.u, idFile=args.i)
        sys.exit(0)

    else:
        print "You must pass a command. Use --help to see usage."
        sys.exit(0)


def confirmSend(cmd):
    yesCmd = "yeah bro"
    noCmd = "nah man"
    print "\nPreparing to send terminal command '" + cmd + "' to the following computers:"
    tools.prettyPrintObjects(objects=cd.computers, title="Targeted Computers")
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
    parser.add_option('-c', action="store", help="Command to send")
    parser.add_option('-u', action="store", default="root", help="User to send command as. Default: root")
    parser.add_option('-i', action="store", default="~/.ssh/id_rsa", help="Identity file to use. Default: ~/.ssh/id_rsa")
    parser.add_option('-n', action="store", default=False, help="Set a range of computers to send command to. ie. 00-06")
    parser.add_option('-m', action="store", default=False, help="Set comma delimited list of computers to send command to. ie. 03,05,10,23")
    parser.add_option('-p', action="store_true", default=False, help="Print the config and exit.")
    parser.add_option('-f', action="store", default=False, help="Specify a different config file to read. Default: " + configFilePath)
    parser.add_option('--dffreeze', action="store_true", default=False, help="DeepFreeze: Freeze specified computers.")
    parser.add_option('--dfthaw', action="store_true", default=False, help="DeepFreeze: Thaw specified computers")
    parser.add_option('--dfuser', action="store", default="admin", help="DeepFreeze: The DeepFreeze user. Default: admin")
    parser.add_option('--dfpass', action="store", default="youshallnotpass", help="DeepFreeze: The DeepFreeze password. Default: youshallnotpass")
    parser.add_option('--rsync', action="store_true", default=False, help="Send a file unsing rsync to the remote host(s)")
    parser.add_option('--src', action="store", default=False, help="Source file to send. Must be used with --rsync")
    parser.add_option('--dest', action="store", default=False, help="Destination for file being sent. Must be used with --rsync")
    options, args = parser.parse_args()
    return options


if __name__ == '__main__':
    main()