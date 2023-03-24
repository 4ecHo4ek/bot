import modules as mod
import classes as classes

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
                workingInfo = classes.WorkingInfo(workingInfoDict["delimeter"], workingInfoDict["deltaPercent"], workingInfoDict["logFile"], workingInfoDict["maxPersent"], workingInfoDict["steps"], workingInfoDict["api_key"], workingInfoDict["api_secret"])
                bot = classes.BotClass(botClassDict["telegram_token"], botClassDict["chat_id"])
            return(errMessage, err, workingInfo, bot)
        except:
            errMessage = f"could read fild {fileName}\n"
            err = 1
            return(errMessage, err, None, None)
    else:
        errMessage = f"could not fild {fileName}\n"
        err = 1
        return(errMessage, err, None, None)
    

def writeLog(logFile, type, message):
    if not mod.os.path.exists('logs'):
        mod.os.makedirs('logs')
    time = mod.time.strftime("%Y-%m-%d %H:%M:%S", mod.time.localtime())
    if type == "warnig":
        type = "WARNING"
    elif type == "error":
        type = "ERROR"
    elif type == "info":
        type = "INFO"
    message = f"{time}\t{type}\t{message}"
    mod.os.system(f"echo {message} >> logs\\{logFile}")


def createDictsSaverElements(pairName: str, coinsDicts: classes.DictsSaver):
    # если в словаре нет ключа с такой парой
    if not pairName in coinsDicts.coinsDictVolume:
        # присваиваем этому ключу экземпляр класса
        coinsDicts.coinsDictVolume[pairName] = classes.CoinSearcher(pairName, {}, {})
    if not pairName in coinsDicts.coinsDictLastPrice:
        coinsDicts.coinsDictLastPrice[pairName] = classes.CoinSearcher(pairName, {}, {})
    return(coinsDicts)


def getInfoFromDictOfPairs(pair: dict):
    pairName = pair['symbol']
    if float(pair['bidPrice']) == 0.00000000:
            return(None, f"{pairName} does not trade!", 3)
    lastPrice = round(float(pair['lastPrice']), 2)
    volume = round(float(pair['volume']), 2)
    quoteVolume = round(float(pair['quoteVolume']), 2)
    pairInfo = classes.CoinPairBasic(pairName, lastPrice, volume, quoteVolume)
    return(pairInfo, None, 0)



def getInfo(client: mod.Client):
    # получаем значения рынка
    try:
        pairs = mod.Client.ticker_24hr(client)
    except:
        return(None, "Could not get info from server", 2)
    return(pairs, "", 0)


def waitNewMinute():
    message = f"wait {60 - int(mod.datetime.datetime.now().second)} seconds before continue"
    print(message)
    while (int(mod.datetime.datetime.now().second) > 1):
        mod.time.sleep(1)



def getConnectionsToResources(bot: classes.BotClass, workingInfo: classes.WorkingInfo):
    try:
        bot = classes.BotClass(bot.telegram_token, bot.chat_id)
    except:
        return(None, None, "Could not connect to bot", 1)
    try:
        client = mod.Client(workingInfo.api_key, workingInfo.api_secret)
    except:
        return(None, None, f"Could not connect to server {client}", 1)
    return(bot, client, "", 0)


def checkBeginig(coinPairData: dict, data: float, time: str):
    err = 0
    if len(coinPairData) == 0:
        coinPairData[time] = data
        err = 3
    return(coinPairData, err)


def getLastValueFromDict(coinPairData: dict):
    '''
    словарь пуст: err = 2
    крайний элемент = 0: err = 3
    все хорошо: err = 0
    '''
    err = 0
    try:
        [lastValueTime] = mod.collections.deque(coinPairData, maxlen=1)
        lastValue = coinPairData[lastValueTime]
    except:
        return(None, None, "", 2)
    if lastValue == 0:
        err == 3
    return(lastValueTime, lastValue, "", err)


def calcPersent(currentValue: float, lastValue: float):
    return(round(float(1 - currentValue / lastValue), 2))



def trimDict(trimedDict: dict, delimeter: int):
    if len(trimedDict) > delimeter:
        lenOfDict = len(trimedDict)
        tmpList = list(trimedDict)
        delItem = tmpList[lenOfDict - delimeter]
        for item in list(trimedDict.keys()):
            if item == delItem:
                break
            trimedDict.pop(item)
    return(trimedDict)



