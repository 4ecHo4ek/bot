import commonFuncs as common
import classes as classes



def calcPersent(currentValue: float, lastValue: float):
    return(round(float(1 - currentValue / lastValue), 2))


def findMaxInDict(coinSearcher: classes.CoinSearcher, tmpInfo: classes.TmpPairInfo, workingInfo: classes.WorkingInfo, data: float, time: str):

    for timeItem in coinSearcher.coinPairData:

        previosValue = coinSearcher.coinPairData[timeItem]
        if previosValue == 0:
            continue
        percent = calcPersent(data, previosValue)
        coinSearcher.timeAndMaxPersentDict[time] = percent
        if coinSearcher.pairName == "BTCUSDT":
            print(coinSearcher.timeAndMaxPersentDict)
        maxPrivPersent = max(list(coinSearcher.timeAndMaxPersentDict.values()))
       

        if abs(percent) <= abs(workingInfo.notInterestingPercent):
            continue
        if abs(percent) >= abs(workingInfo.attentionPercent) and abs(percent) > abs(tmpInfo.maxPercent):
            tmpInfo.maxPercent = percent
            message = common.createMessage(coinSearcher.pairName, tmpInfo.typeOfValue, percent, timeItem, time)
            common.sendMessage(workingInfo, message)
            common.writeLog(workingInfo.logFileName, "info", f"findMaxInDict | >= workingInfo.attentionPercent - {message}") # TEST
            continue
        
        if abs(percent) > abs(tmpInfo.maxPercent):
            tmpInfo.maxPercent = percent
            if abs(percent) > abs(maxPrivPersent):
                tmpInfo = common.fullTmpInfoClass(tmpInfo, timeItem, percent, time)

    if len(coinSearcher.coinPairData) and len(coinSearcher.timeAndMaxPersentDict):
        if abs(tmpInfo.maxPercent) > abs(maxPrivPersent) and abs(tmpInfo.maxPercent) > abs(workingInfo.notInterestingPercent):
            common.writeLog(workingInfo.logFileName, "info", f"findMaxInDict | tmpInfo.maxPercent - {tmpInfo.maxPercent}, maxPrivPersent - {maxPrivPersent}, tmpInfo.maxPercent - {tmpInfo.maxPercent}, workingInfo.notInterestingPercent - {workingInfo.notInterestingPercent}") # TEST
            message = common.createMessage(coinSearcher.pairName, tmpInfo.typeOfValue, percent, timeItem, time)
            common.sendMessage(workingInfo, message)
            common.writeLog(workingInfo.logFileName, "info", f"findMaxInDict | {message}") # TEST

    tmpInfo = common.cleanTmpInfoClass(tmpInfo)
    return(coinSearcher)



def calculations(workingInfo: classes.WorkingInfo, coinsDicts: classes.CoinSearcher, tmpInfo: classes.TmpPairInfo, data: float, time: str):

    coinsDicts.coinPairData, err = common.checkBeginig(coinsDicts.coinPairData, data, time)
    if err == 3:
        return(coinsDicts, "", 3)
    coinsDicts.coinPairData = common.trimDict(coinsDicts.coinPairData, workingInfo.delimeter)
    coinsDicts.timeAndMaxPersentDict = common.trimDict(coinsDicts.timeAndMaxPersentDict, workingInfo.delimeter)    
    coinsDicts = findMaxInDict(coinsDicts, tmpInfo, workingInfo, data, time)

    coinsDicts.coinPairData[time] = data
    return(coinsDicts, "", 0)


