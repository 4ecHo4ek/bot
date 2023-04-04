import modules as mod
import classes as classes


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
    message = f"{time}\t{type}\t{message}\n"
    # print(message)
    with open(mod.os.path.join("logs", logFile), "a", encoding='utf-8') as file:
        file.writelines(message)



def sendMessage(workingInfo: classes.WorkingInfo, message: str):
    try:
        r = mod.requests.post(f"{workingInfo.url}:{workingInfo.port}/sendMessage", json={'message': f"{message}\n"})
    except:
        writeLog(workingInfo.logFileName, "error", f"sendMessage | could not send message to {workingInfo.url}:{workingInfo.port}/sendMessage")
        return
    if r.status_code == 500:
        writeLog(workingInfo.logFileName, "error", f"sendMessage | uncorrect reques to server {r.status_code} {r.reason}")
    elif r.status_code == 404:
        writeLog(workingInfo.logFileName, "error", f"sendMessage | bot error {r.status_code} {r.reason}")
    elif r.status_code != 200:
        writeLog(workingInfo.logFileName, "error", f"sendMessage | connetion to bot failed {r.status_code} {r.reason}")


def makePrediction(persent: float, reverse: bool):
    koef = 1
    if reverse:
        koef = -1
    if koef * persent > 0:
        prediction = "СНИЖЕНИЕ"
    else:
        prediction = "УВЕЛЕЧЕНИЕ"
    return(prediction)


# составление сообщения для отправки
def createMessage(pairName: str, typeOfValue: str, persent: float, timeBegin: str, timeEnd: str):
    '''
    составляем сообщение для отправки
    '''
    if typeOfValue == "volume":
        message = f"(ожидается {makePrediction(persent, False)} цены {pairName}) Объем первой монеты в паре {pairName} изменился на "
    elif typeOfValue == "lastPrice":
        message = f"Цена в паре {pairName} изменилась на "
    elif typeOfValue == "quoteVolume":
        message = f"(ожидается {makePrediction(persent, True)} цены {pairName}) Объем второй монеты в паре {pairName} изменился на "
    message += f"{persent}% с {timeBegin} по {timeEnd}"
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
    

def createDictsSaverElements(pairName: str, coinsDicts: classes.DictsSaver):
    '''
    создаем словари для хранения инфорации
    о рассматриваемых данных
    '''
    # если в словаре нет ключа с такой парой
    if not pairName in coinsDicts.coinsDictVolume:
        coinsDicts.coinsDictVolume[pairName] = classes.CoinSearcher(pairName, {}, {})
    if not pairName in coinsDicts.coinsDictLastPrice:
        coinsDicts.coinsDictLastPrice[pairName] = classes.CoinSearcher(pairName, {}, {})
    if not pairName in coinsDicts.coinsDictQuoteVolume:
        coinsDicts.coinsDictQuoteVolume[pairName] = classes.CoinSearcher(pairName, {}, {})
    return(coinsDicts)


def getInfoFromDictOfPairs(pair: dict):
    '''
    получаем информацию о паре
    err == 2 - пустая пара, пропускаем без записи в лог
    '''
    try:
        pairName = pair['symbol']
        if float(pair['bidPrice']) == 0.00000000:
            return(classes.CoinPairBasic(None, None, None, None), "pair does not trade", 2)
        lastPrice = round(float(pair['lastPrice']), 2)
        volume = round(float(pair['volume']), 2)
        quoteVolume = round(float(pair['quoteVolume']), 2)
    except:
        pairInfo = classes.CoinPairBasic("", 0, 0, 0)
        message = f"somthihg wrong with getting info in getInfoFromDictOfPairs - {pair}"
        return(classes.CoinPairBasic(None, None, None, None), message, 3)
    pairInfo = classes.CoinPairBasic(pairName, lastPrice, volume, quoteVolume)
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
        return(None, None, f"Could not connect to server", 1)
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



def getTime():
    if mod.datetime.datetime.now().minute < 10:
        minutes = f"0{mod.datetime.datetime.now().minute}"
    else:
        minutes = f"{mod.datetime.datetime.now().minute}"
    time = f"{mod.datetime.datetime.now().hour}:{minutes}"
    return(time)


