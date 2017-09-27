'''
Created on July 6, 2017

@author: Tyler Thompson
'''
import commands,re

class Tools(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def prettyPrintObjects(self, objects, title=None, dividers=False, objFilter=None):
        horizontalLine = u'\u2501'
        verticalLine = u'\u2503'
        topLeftCorner = u'\u250F'
        topRightCorner = u'\u2513'
        bottomLeftCorner = u'\u2517'
        bottomeRightCorner = u'\u251B'
        leftThreeWay = u'\u2523'
        rightThreeWay = u'\u252B'
        topThreeWay = u'\u2533'
        bottomThreeWay = u'\u253B'
        fourWay = u'\u254B'
        thinHorizontalLine = u'\u2500'
        thinVerticalLine = u'\u2502'
        thinFourWay = u'\u253C'
        thinThickLeftThreeWay = u'\u2520'
        thinThickRightThreeWay = u'\u2528'
        thinThickBottomThreeWay = u'\u2537'
        thinThickTopFourWay = u'\u2547'

        if objects == None:
            print "None"
            return None
        try:
            if len(objects) == 0:
                print "Empty"
                return None
        except:
            pass

        #test is if only single object was passed
        try:
            objects[0]
        except:
            objects = [objects]


        #filter out specified variables DOES NOT WORK!
        # try:
        #     if objFilter != None:
        #         objFilter = objFilter.split(',')
        #         for afilter in objFilter:
        #             for object in objects:
        #                 del object.__dict__[afilter]
        # except:
        #     pass
        if objFilter != None:
            objFilter = objFilter.split(',')
        else:
            objFilter = []


        #get the individual spacer lengths
        #numHeaders = len(vars(objects[0]))
        #filter objects
        #print vars(objects[0])
        objVars = vars(objects[0])
        filteredObjVars = []
        for key in objVars:
            #print key
            if key in objFilter:
                continue
            filteredObjVars.append(key)
        numHeaders = len(filteredObjVars)
        #print filteredObjVars
        #print numHeaders

        #spacerHeaders = len(vars(objects[0]))

        spacerLengths = []
        for i in range(0, numHeaders):
            #spacerLength = len(str(vars(objects[0]).keys()[i]))
            spacerLength = len(str(filteredObjVars[i]))
            for objecty in objects:
                valueLength = len(str(vars(objecty)[filteredObjVars[i]]))
                #valueLength = len(str(vars(objecty).values()[i]))
                #valueLength = vars(objecty)[objFilter[i]]
                if valueLength > spacerLength:
                    spacerLength = valueLength
            spacerLengths.append(spacerLength)
        #print spacerLengths


        #computer header length
        headerLength = 0
        for spacerLength in spacerLengths:
            headerLength = headerLength + spacerLength + 3
        print


        # print the title if it exists
        if title != None:
            title = str(title)
            # print the top title underline
            header = topLeftCorner
            for _ in range(1, headerLength):
                header = header + horizontalLine
            header = header + topRightCorner
            print header

            titleSpacerLength = (headerLength / 2) - (len(title) / 2)
            titleString = verticalLine
            for _ in range(0, titleSpacerLength):
                titleString = titleString + " "
            titleString = titleString + title
            for _ in range(1, titleSpacerLength):
                titleString = titleString + " "
            #fix length of spaces in title
            if len(titleString) > headerLength:
                titleString = titleString[:-1]
            elif len(titleString) > headerLength:
                titleString = titleString + " "

            titleString = titleString + verticalLine
            print titleString

        #compute the cross section points
        crossSectionPoints = []
        lastSpacerLength = 0
        for spacerLength in spacerLengths:
            nextSpacerLength = (spacerLength + lastSpacerLength + 3)
            crossSectionPoints.append(nextSpacerLength)
            lastSpacerLength = nextSpacerLength


        # print the top header underline
        if title == None:
            header = topLeftCorner
        else:
            header = leftThreeWay
        curHeader = 0
        for i in range(1, headerLength):
            if i == crossSectionPoints[curHeader]:
                header = header + topThreeWay
                curHeader = curHeader + 1
                if curHeader > (len(crossSectionPoints) - 1):
                    curHeader = (len(crossSectionPoints) - 1)
            else:
                header = header + horizontalLine
        if title == None:
            header = header + topRightCorner
        else:
            header = header + rightThreeWay
        print header


        #print the headers
        print verticalLine,
        i = 0;
        for key in vars(objects[0]):
            #object filter
            if key in objFilter:
                continue

            #spacer = spacerLengths[vars(objects[0]).keys().index(key)]
            spacer = spacerLengths[i]

            i = i + 1
            spaceNum = spacer - len(str(key))
            divider = ""
            for _ in range(0, spaceNum):
                divider = divider + " "
            divider = divider + " " + verticalLine
            print str(key).upper() + divider,
        print


        #print the bottom header underline
        header = leftThreeWay
        curHeader = 0
        for i in range(1, headerLength):
            if i == crossSectionPoints[curHeader]:
                header = header + thinThickTopFourWay
                curHeader = curHeader + 1
                if curHeader > (len(crossSectionPoints) - 1):
                    curHeader = (len(crossSectionPoints) - 1)
            else:
                header = header + horizontalLine
        header = header + rightThreeWay
        print header


        #print the objects
        for objecty in objects:
            print verticalLine,
            i = 0
            for key, value in vars(objecty).iteritems():
                # object filter
                if key in objFilter:
                    continue

                #spaceNum = spacerLengths[vars(objects[0]).keys().index(key)] - len(str(value))
                spaceNum = spacerLengths[i] - len(str(value))

                divider = ""
                for _ in range(0, spaceNum):
                    divider = divider + " "
                divider = divider + " " + thinVerticalLine
                if vars(objecty).keys().index(key) == (len(vars(objecty).keys()) - 1) or key == filteredObjVars[len(filteredObjVars) - 1]:
                    divider = divider[:-1]
                    divider = divider + verticalLine
                i = i + 1
                print str(value) + divider,
            print

            # print the divider line
            if dividers:
                if objects.index(objecty) != (len(objects) - 1):
                    header = thinThickLeftThreeWay
                    curHeader = 0
                    for i in range(1, headerLength):
                        if i == crossSectionPoints[curHeader]:
                            header = header + thinFourWay
                            curHeader = curHeader + 1
                            if curHeader > (len(crossSectionPoints) - 1):
                                curHeader = (len(crossSectionPoints) - 1)
                        else:
                            header = header + thinHorizontalLine
                    header = header + thinThickRightThreeWay
                    print header



        # print the footer underline
        header = bottomLeftCorner
        curHeader = 0
        for i in range(1, headerLength):
            if i == crossSectionPoints[curHeader]:
                header = header + thinThickBottomThreeWay
                curHeader = curHeader + 1
                if curHeader > (len(crossSectionPoints) - 1):
                    curHeader = (len(crossSectionPoints) - 1)
            else:
                header = header + horizontalLine
        header = header + bottomeRightCorner
        print header
        print





    def getPing(self, ip):
        response = commands.getoutput("ping -c 1 -w 1 " + ip)
        regex = re.compile(r', 0% packet loss')
        if regex.search(response) is not None:
            return True
        else:
            return False

    def sendSsh(self, user, ip, cmd, idFile="~/.ssh/id_rsa", connectTimeout="5", strictHostKeyChecking="no", batchMode="yes"):
        status = commands.getoutput('ssh -o ConnectTimeout=' + str(connectTimeout) + ' -o StrictHostKeyChecking='
                                  + strictHostKeyChecking + ' -o BatchMode=' + batchMode + ' -i ' + idFile
                                  + ' ' + user + '@' + ip + ' -C "' + cmd + '"')
        if "Permission denied" in status:
            print "Failed to connect to " + ip + " " + status
            return "Permission Denied"
        return str(status).strip()

    def sendFile(self, user, ip, src, dest, idFile="~/.ssh/id_rsa", connectTimeout="5", strictHostKeyChecking="no", batchMode="yes"):
        status = commands.getoutput("rsync -hav -e 'ssh -i " + idFile + " -o connectTimeout=" + str(connectTimeout) +
                                    " -o strictHostKeyChecking=" + strictHostKeyChecking + " -o batchMode=" + batchMode + "' " +
                                    src + " " + user + "@" + ip + ":" + dest)
        if "Permission denied" in status:
            #print "Failed to connect to " + ip + " " + status
            return "Permission Denied"
        elif "timed out" in status:
            #print "Connection timed out to " + ip
            return "Connection timed out"
        elif "sent" in status and "received" in status and "speedup" in status:
            return "File transfer complete"
        else:
            return status
