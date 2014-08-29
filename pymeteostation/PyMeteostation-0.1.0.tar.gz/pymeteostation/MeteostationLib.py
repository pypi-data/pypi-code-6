from pymlab import config
import time, json, urllib, urllib2, sys, os, ast, ConfigParser, base64


class Meteostation:
    def __init__(self,configFileName):
        self.settings = self.__getSettings(configFileName)

        try:
            cfg = config.Config(i2c={"port":1}, bus=self.settings["I2C_configuration"])
            cfg.initialize()

            self.NameTypeDict = self.__getTypes(self.settings["I2C_configuration"])

            self.Devices = {}
            for device in self.__getNames(self.settings["I2C_configuration"]):
                self.Devices[device] = cfg.get_device(device)
        except Exception, e:
            sys.exit("Initialization of I2c failed: "+str(e))

        time.sleep(0.5)

    def getData(self,requestList="all"):        # returns requested sensor data
        outputList = {}
        outputList["time"] = int(time.time())
        if requestList == "all":
            for device in self.Devices.keys():
                outputList[device] = self.__getSensorData(device,self.NameTypeDict[device])
        else:
            for request in requestList:
                outputList[request] = self.__getSensorData(request,self.NameTypeDict[device])

        return outputList

    def __getSensorData(self,sensorName,sensorType):       # must return list
        try:
            if sensorType == "sht25":
                self.Devices[sensorName].route()
                return [self.Devices[sensorName].get_hum(),self.Devices[sensorName].get_temp()]
            elif sensorType == "altimet01":     # returns atmospheric pressure readings corrected to sea level altitude.
                self.Devices[sensorName].route()
                data = self.Devices[sensorName].get_tp()
                return [data[0],data[1]/((1-((0.0065*self.settings["altitude"])/288.15))**5.255781292873008*100)]
        except Exception, e:
            print sensorName + " sensor error:",str(e)
            return ["error",str(e)]

    def log(self,dataDict,logFileName=""):      # logging function
        if logFileName == "":
            logFileName = time.strftime("%Y-%m-%d:%H-", time.localtime()) + "meteoData.log"
            FULLlogFileName = self.settings["logpath"] + time.strftime("%Y/", time.localtime()) + time.strftime("%m/", time.localtime()) + time.strftime("%d/", time.localtime()) + logFileName

        if not os.path.exists(FULLlogFileName):
            self.__generateLogFile(logFileName,self.settings["logpath"] + time.strftime("%Y/", time.localtime()) + time.strftime("%m/", time.localtime()) + time.strftime("%d/", time.localtime()))

        try:
            with open(FULLlogFileName,"r") as f:
                savedData = json.load(f)

            with open(FULLlogFileName,"w") as f:
                savedData.append(dataDict)
                f.write(json.dumps(savedData))
        except Exception, e:
            print "Logging failed:", str(e)
            
    def __generateLogFile(self,logFileName,logPath):      # generator of a log file
        defaultLog = []
        try:
            if not logPath == "" and not os.path.exists(logPath):
                os.makedirs(logPath)

            with open(logPath+logFileName,"w") as f:
                f.write(json.dumps(defaultLog))
        except Exception, e:
            print "Cannot generate log file:",str(e)

    def sendData(self,username,password,sendDict):      # sends data to openweathermap.com
        sendData = self.translateToPOST(sendDict)
        url = "http://openweathermap.org/data/post"

        request = urllib2.Request(url,data=urllib.urlencode(sendData),headers={"Authorization":"Basic "+base64.encodestring(username+":"+password)[:-1]})
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            if hasattr(e, "code"):
                return (False, {"message":e.reason,"cod":e.code,"id":"0"})
            else:
                return (False, {"message":e.reason,"cod":"Failed to reach server","id":"0"})
        except Exception as e:
            return (False, {"message":str(e),"cod":"Network error","id":"0"})
        else:
            try:
                result = result.read()
                return (True, json.loads(result))
            except Exception as e:
                return (False, {"message":result,"cod":str(e),"id":"0"})

    def translateToPOST(self,sendDict):    # translates sensor values to POST request format
        payload = {}
        for itemKey in sendDict.keys():
            if not itemKey == "time" and not sendDict[itemKey][0] == "error":
                for transList in self.settings["Translation_Into_POST"]:
                    if itemKey == transList[1]:
                        payload[transList[0]] = str(round(sendDict[itemKey][transList[2]],2))

        if self.settings["stationname"]:
            payload["name"] = str(self.settings["stationname"])
        if self.settings["latitude"] and self.settings["longitude"]:
            payload["lat"] = str(self.settings["latitude"])
            payload["long"] = str(self.settings["longitude"])
        if self.settings["altitude"]:
            payload["alt"] = str(self.settings["altitude"])
        return payload

    def __getNames(self,busConfig):  # recursively searches for all "name" dictionary keys and returns their values: ["name1", "name2", ...]
        names = []
        for item in busConfig:
            for key in item.keys():
                if key == "name":
                    names.append(item[key])
                if type(item[key]) == list:
                    names += self.__getNames(item[key])
        return names

    def __getTypes(self,busConfig):  # recursively searches for all "name" and "type" dictionary keys and return their values: {name:type, ...}
        names = {}
        for item in busConfig:
            for key in item.keys():
                if key == "name":
                    names[item[key]] = item["type"]
                if type(item[key]) == list:
                    names = dict(names.items() + self.__getTypes(item[key]).items())
        return names

    def __getSettings(self,fileName):   # returns settings dictionary made of config file
        parser = ConfigParser.SafeConfigParser()
        try:
            parser.read(fileName)
        except Exception, e:
            sys.exit("Unable to load configuration file. Error: "+str(e))

        options = {}
        for sectionName in ["Meteostation","I2C_Device","Translation_Into_POST"]:
            if not parser.has_section(sectionName):
                sys.exit("Unable to find \'%s\' section" % (sectionName))
            else:
                options[sectionName] = parser.options(sectionName)

        requiedOptions = ["username","password","uploadinterval","logpath"]
        missingOptions = requiedOptions
        missingOptionsString = ""
        for requiedOptionID in range(len(requiedOptions)):
            for option in options["Meteostation"]:
                if option == requiedOptions[requiedOptionID]:
                    missingOptions[requiedOptionID] = ""
                    break

        for missingOption in missingOptions:
            if missingOption != "":
                missingOptionsString += "\'"+missingOption+"\', "

        if len(missingOptionsString) != 0:
            sys.exit("Unable to find %s option(s)." % (missingOptionsString[:len(missingOptionsString)-2]))

        possibleOptions = ["username","password","uploadinterval","logpath","stationname","latitude","longitude","altitude"]
        settings = {}
        try:
            for option in possibleOptions:
                if parser.has_option("Meteostation",option):
                    try:
                        settings[option] = float(parser.get("Meteostation",option))
                    except ValueError:
                        settings[option] = parser.get("Meteostation",option)
                else:
                    settings[option] = ""
            if not settings["altitude"]:
                settings["altitude"] = 0
            
            settings["I2C_configuration"] = [self.__getI2CConfig(parser,"I2C_Device")]
            
            settings["Translation_Into_POST"] = []
            for option in options["Translation_Into_POST"]:
                if parser.get("Translation_Into_POST",option) == "":
                    translationListPart = ['',0]
                else:
                    try:
                        translationListPart = self.__getOptionList(parser.get("Translation_Into_POST",option))
                        if len(translationListPart) != 2:
                            print "Strange value set to option \'%s\'. Using default value." % (option)
                            translationListPart = ['',0]
                    except:
                        print "Strange value set to option \'%s\'. Using default value." % (option)
                        translationListPart = ['',0]
                settings["Translation_Into_POST"].append([option,translationListPart[0],int(translationListPart[1])])
        except Exception, e:
            sys.exit("Bad format of configuration file. Error: "+str(e))
        return settings

    def __getI2CConfig(self,parser,section): # recursively generates I2C configuration from configuration file
        result = {}
        for option in parser.options(section):
            if option == "children":
                children = self.__getOptionList(parser.get(section,option))
                result[option] = []
                for child in children:
                    result[option].append(self.__getI2CConfig(parser,child))
            elif option == "address":
                result[option] = int(parser.get(section,option),base=16)
            elif option == "channel":
                result[option] = int(parser.get(section,option))
            else:
                result[option] = parser.get(section,option)
        return result

    def __getOptionList(self,string):
        lastPosition = 0
        optionList = []
        for letterPos in range(len(string)):
            if string[letterPos] == ";":
                optionList.append(string[lastPosition:letterPos])
                lastPosition = letterPos+1
        if lastPosition < len(string):
            optionList.append(string[lastPosition:len(string)])
        return optionList