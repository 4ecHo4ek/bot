import modules as mod
import internalClasses as inClass


def trimString(string: str) -> str:
    string = string[string.find(":") + 1:]
    if string[0] == " ":
        string = string[1:].replace("\n", "")
    return(string)


def findDataInReadedFile(lines: list[str]): #-> dict, dict:
    workingInfoDict = {"delimeter": 0, "deltaPercent": 0, "logFile": "", "maxPersent": 0, "steps": 0, "api_key": "", "api_secret": ""}
    botClassDict = {"telegram_token": "", "chat_id": ""}
    for line in lines:
        if 'delimeter' in line:
            workingInfoDict["delimeter"] = int(trimString(line))
        elif 'deltaPercent' in line:
            workingInfoDict["deltaPercent"] = float(trimString(line))
        elif 'logFile' in line:
            workingInfoDict["logFile"] = trimString(line)
        elif 'maxPersent' in line:
            workingInfoDict["maxPersent"] = float(trimString(line))
        elif 'steps' in line:
            workingInfoDict["steps"] = int(trimString(line))
        elif 'api_key' in line:
            workingInfoDict["api_key"] = trimString(line)
        elif 'api_secret' in line:
            workingInfoDict["api_secret"] = trimString(line)
        elif 'telegram_token' in line:
            botClassDict["telegram_token"] = trimString(line)
        elif 'chat_id' in line:
            botClassDict["chat_id"] = int(trimString(line))
    return(workingInfoDict, botClassDict)


def getDataFromFile(fileName: str):
    err = 0
    errMessage = ""
    if mod.os.path.exists(fileName):
        try:
            with open(fileName,'r') as file:
                lines = file.readlines()
                (workingInfoDict, botClassDict) = findDataInReadedFile(lines)
                workingInfo = inClass.classes.WorkingInfo(workingInfoDict["delimeter"], workingInfoDict["deltaPercent"], workingInfoDict["logFile"], workingInfoDict["maxPersent"], workingInfoDict["steps"], workingInfoDict["api_key"], workingInfoDict["api_secret"])
                bot = inClass.classes.BotClass(botClassDict["telegram_token"], botClassDict["chat_id"])
            return(errMessage, err, workingInfo, bot)
        except:
            errMessage = f"could read fild {fileName}\n"
            err = 1
            return(errMessage, err, None, None)
    else:
        errMessage = f"could not fild {fileName}\n"
        err = 1
        return(errMessage, err, None, None)
    

