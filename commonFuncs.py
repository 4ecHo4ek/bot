import modules as mod
import classes as classes


# составление сообщения для отправки
def createMessage(message: str, pairName: str, typeOfValue: str, persent: float, timeBegin: str, timeEnd: str):
    '''
    составляем сообщение для отправки
    '''
    if typeOfValue == "volume":
        message += f"Объем первой монеты в паре {pairName} изменился на "
    elif typeOfValue == "lastPrice":
        message += f"Цена в паре {pairName} изменилась на "
    message += f"{persent}% с {timeBegin} по {timeEnd}\n"
    return(message)


def trimString(string: str) -> str:
    '''
    разделение строки для получения информации из файла
    '''
    string = string[string.find(":") + 1:]
    if string[0] == " ":
        string = string[1:]
        string = string.replace("\n", "")
    return(string)


def findDataInReadedFile(lines: list[str]):
    '''
    составление информации и заполнение в словари для хранения и инициализации классов
    '''
    workingInfoDict = {"delimeter": 0, "deltaPercent": 0, "logFile": "", "maxPersent": 0, "steps": 0, "api_key": "", "api_secret": "", "url": "", "port": ""}
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
        elif 'url' in line:
            workingInfoDict["url"] = trimString(line)
        elif 'port' in line:
            workingInfoDict["port"] = int(trimString(line))
    return(workingInfoDict)


def getDataFromFile(fileName: str):
    '''
    получаем информацию из файла
    '''
    err = 0
    errMessage = ""
    if mod.os.path.exists(fileName):
        try:
            with open(fileName,'r') as file:
                lines = file.readlines()
                (workingInfoDict) = findDataInReadedFile(lines)
                workingInfo = classes.WorkingInfo(workingInfoDict["delimeter"], workingInfoDict["deltaPercent"], 
                                                  workingInfoDict["logFile"], workingInfoDict["maxPersent"],
                                                  workingInfoDict["steps"], workingInfoDict["api_key"], 
                                                  workingInfoDict["api_secret"], workingInfoDict["url"], 
                                                  workingInfoDict["port"]
                                                  )
            return(errMessage, err, workingInfo)
        except:
            errMessage = f"could read fild {fileName}\n"
            err = 1
            return(errMessage, err, None)
    else:
        errMessage = f"could not fild {fileName}\n"
        err = 1
        return(errMessage, err, None)
    

def writeLog(logFile, type, message):
    '''
    функция для написания лога
    '''
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
    '''
    создаем словари для хранения инфорации
    о рассматриваемых данных
    '''
    # если в словаре нет ключа с такой парой
    if not pairName in coinsDicts.coinsDictVolume:
        # присваиваем этому ключу экземпляр класса
        coinsDicts.coinsDictVolume[pairName] = classes.CoinSearcher(pairName, {}, {})
    if not pairName in coinsDicts.coinsDictLastPrice:
        coinsDicts.coinsDictLastPrice[pairName] = classes.CoinSearcher(pairName, {}, {})
    return(coinsDicts)


def getInfoFromDictOfPairs(pair: dict):
    '''
    получаем информацию о паре
    '''
    try:
        pairName = pair['symbol']
        if float(pair['bidPrice']) == 0.00000000:
                return(None, None, 3)
        lastPrice = round(float(pair['lastPrice']), 2)
        volume = round(float(pair['volume']), 2)
        quoteVolume = round(float(pair['quoteVolume']), 2)
        pairInfo = classes.CoinPairBasic(pairName, lastPrice, volume, quoteVolume)
    except:
        pairInfo = classes.CoinPairBasic("", 0, 0, 0)
        message = f"somthihg wrong with getting info in getInfoFromDictOfPairs - {pair}"
        return(pairInfo, message, 3)
    return(pairInfo, None, 0)



def getInfo(client: mod.Client):
    '''
    получаем инфорацию от сервера
    '''
    # получаем значения рынка
    try:
        pairs = mod.Client.ticker_24hr(client)
    except:
        return(None, "Could not get info from server", 2)
    return(pairs, "", 0)


def waitNewMinute():
    '''
    функция для ожидания
    '''
    message = f"wait {60 - int(mod.datetime.datetime.now().second)} seconds before continue"
    print(message)
    while (int(mod.datetime.datetime.now().second) > 1):
        mod.time.sleep(1)



def getConnectionsToResources(workingInfo: classes.WorkingInfo):
    '''
    подключаемся к серверу
    '''
    try:
        client = mod.Client(workingInfo.api_key, workingInfo.api_secret)
    except:
        return(None, None, f"Could not connect to server {client}", 1)
    return(client, "", 0)


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
        return(None, None, f"dict - {coinPairData}", 2)
    if lastValue == 0:
        err == 3
    return(lastValueTime, lastValue, "", err)


def calcPersent(currentValue: float, lastValue: float):
    return(round(float(1 - currentValue / lastValue), 2))



def trimDict(trimedDict: dict, delimeter: int):
    '''
    ограничиваем словари до велечины
    delimeter - количество минут, которые храним
    '''
    if len(trimedDict) > delimeter:
        lenOfDict = len(trimedDict)
        tmpList = list(trimedDict)
        delItem = tmpList[lenOfDict - delimeter]
        for item in list(trimedDict.keys()):
            if item == delItem:
                break
            trimedDict.pop(item)
    return(trimedDict)


def checkValuesWithMoreThenMaxPersent(tmpInfo: classes.TmpPairInfo, coinSearcher: classes.CoinSearcher, timeAndMaxPersentDict: dict, timeItem: float, percent: float, message: str):
    '''
    поиск интересующего процента
    '''
    if timeItem in timeAndMaxPersentDict:
        if abs(timeAndMaxPersentDict[timeItem]) < abs(percent):
            timeAndMaxPersentDict[timeItem] = percent
        if abs(tmpInfo.maxPercent) < abs(timeAndMaxPersentDict[timeItem]):
            tmpInfo.maxPercent = timeAndMaxPersentDict[timeItem]
            message += createMessage(message, coinSearcher.pairName, tmpInfo.typeOfValue, percent, tmpInfo.tBegin, tmpInfo.tEnd)
    else:
        if abs(tmpInfo.maxPercent) < abs(percent):
            tmpInfo.maxPercent = percent
            timeAndMaxPersentDict[timeItem] = percent
            message += createMessage(message, coinSearcher.pairName, tmpInfo.typeOfValue, percent, tmpInfo.tBegin, tmpInfo.tEnd)
    return(timeAndMaxPersentDict, message)


def cleanTmpInfoClass(tmpInfo: classes.TmpPairInfo):
    tmpInfo.maxPercent = 0
    tmpInfo.tBegin = "00:00"
    tmpInfo.tEnd = "00:00"
    return(tmpInfo)


def fullTmpInfoClass(tmpInfo: classes.TmpPairInfo, timeItem: float, percent: float, time: str):
    tmpInfo.maxPercent = percent
    tmpInfo.tBegin = timeItem
    tmpInfo.tEnd = time
    return(tmpInfo)


def checkValuesWithInterestingPersent(tmpInfo: classes.TmpPairInfo, timeAndMaxPersentDict: dict, timeItem: float, percent: float, time: str):
    if timeItem in timeAndMaxPersentDict:
        if abs(timeAndMaxPersentDict[timeItem]) < abs(percent) and abs(tmpInfo.maxPercent) < abs(percent):
            timeAndMaxPersentDict[timeItem] = percent
            tmpInfo = fullTmpInfoClass(tmpInfo, timeItem, percent, time)
    else:
        timeAndMaxPersentDict[timeItem] = percent
        if abs(tmpInfo.maxPercent) < abs(percent):
            tmpInfo = fullTmpInfoClass(tmpInfo, timeItem, percent, time)
    return(tmpInfo, timeAndMaxPersentDict)


def findMaxInDict(coinSearcher: classes.CoinSearcher, tmpInfo: classes.TmpPairInfo, workingInfo: classes.WorkingInfo, data: float, time: str, message: str):
    for timeItem in coinSearcher.coinPairData:
        previosValue = coinSearcher.coinPairData[timeItem]
        if previosValue == 0:
            continue
        percent = calcPersent(data, previosValue)
        if abs(percent) <= abs(workingInfo.notInterestingPercent):
            continue
        if abs(percent) >= abs(workingInfo.attentionPercent):    
            coinSearcher.timeAndMaxPersentDict, message = checkValuesWithMoreThenMaxPersent(tmpInfo, coinSearcher, 
                                                                                            coinSearcher.timeAndMaxPersentDict, 
                                                                                            timeItem, percent, message)
            continue
        tmpInfo, coinSearcher.timeAndMaxPersentDict = checkValuesWithInterestingPersent(tmpInfo, coinSearcher.timeAndMaxPersentDict, 
                                                                                        timeItem, percent, time)

    if abs(tmpInfo.maxPercent) > abs(workingInfo.notInterestingPercent):
        message += createMessage(message, coinSearcher.pairName, tmpInfo.typeOfValue, percent, tmpInfo.tBegin, tmpInfo.tEnd)
    tmpInfo = cleanTmpInfoClass(tmpInfo)
    return(coinSearcher.timeAndMaxPersentDict, message)



def calculations(workingInfo: classes.WorkingInfo, coinsDicts: classes.CoinSearcher, tmpInfo: classes.TmpPairInfo, data: float, time: str, message: str):
    coinsDicts.coinPairData, err = checkBeginig(coinsDicts.coinPairData, data, time)
    if err == 3:
        return(coinsDicts, message, "", 3)
    lastTimeOfValue, lastValue, errMessage, err = getLastValueFromDict(coinsDicts.coinPairData)
    if err == 2:
        return(coinsDicts, message, errMessage, 3)
    elif err == 3 or lastValue == 0:
        coinsDicts.coinPairData[time] = data
        return(coinsDicts, message, "", 0)
    percent = calcPersent(data, lastValue)
    if abs(percent) <= abs(workingInfo.notInterestingPercent):
        coinsDicts.coinPairData[time] = data
        return(coinsDicts, message, "", 0)
    if abs(percent) >= abs(workingInfo.attentionPercent):
        coinsDicts.timeAndMaxPersentDict[time] = percent
        message = createMessage(message, coinsDicts.pairName, tmpInfo.typeOfValue, percent, lastTimeOfValue, time)
        pass
    coinsDicts.coinPairData = trimDict(coinsDicts.coinPairData, workingInfo.delimeter)
    coinsDicts.timeAndMaxPersentDict = trimDict(coinsDicts.timeAndMaxPersentDict, workingInfo.delimeter)
    coinsDicts.timeAndMaxPersentDict, message = findMaxInDict(coinsDicts, tmpInfo, workingInfo, data, time, message)
    coinsDicts.coinPairData[time] = data
    return(coinsDicts, message, "", 0)


def botLogs(workingInfo: classes.WorkingInfo, r):
    if r.status_code == 500:
        writeLog(workingInfo.logFileName, "error", f"uncorrect reques to server {r.status_code} {r.reason}")
    elif r.status_code == 404:
        writeLog(workingInfo.logFileName, "error", f"bot error {r.status_code} {r.reason}")
    elif r.status_code != 200:
        writeLog(workingInfo.logFileName, "error", f"connetion to bot failed {r.status_code} {r.reason}")
    print(r.status_code, r.reason)

