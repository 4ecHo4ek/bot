import commonFuncs as common
import classes as classes



def calcPersent(currentValue: float, lastValue: float):
    return(round(float(1 - currentValue / lastValue), 2))



def checkValuesWithMoreThenMaxPersent(tmpInfo: classes.TmpPairInfo, coinSearcher: classes.CoinSearcher, timeAndMaxPersentDict: dict, timeItem: float, percent: float, message: str):
    '''
    поиск интересующего процента
    '''
    if timeItem in timeAndMaxPersentDict:
        if abs(timeAndMaxPersentDict[timeItem]) < abs(percent):
            timeAndMaxPersentDict[timeItem] = percent
        if abs(tmpInfo.maxPercent) < abs(timeAndMaxPersentDict[timeItem]):
            tmpInfo.maxPercent = timeAndMaxPersentDict[timeItem]
            message += common.createMessage(message, coinSearcher.pairName, tmpInfo.typeOfValue, percent, tmpInfo.tBegin, tmpInfo.tEnd)
    else:
        if abs(tmpInfo.maxPercent) < abs(percent):
            tmpInfo.maxPercent = percent
            timeAndMaxPersentDict[timeItem] = percent
            message += common.createMessage(message, coinSearcher.pairName, tmpInfo.typeOfValue, percent, tmpInfo.tBegin, tmpInfo.tEnd)
    return(timeAndMaxPersentDict, message)



def checkValuesWithInterestingPersent(tmpInfo: classes.TmpPairInfo, timeAndMaxPersentDict: dict, timeItem: float, percent: float, time: str):
    if timeItem in timeAndMaxPersentDict:
        if abs(timeAndMaxPersentDict[timeItem]) < abs(percent) and abs(tmpInfo.maxPercent) < abs(percent):
            timeAndMaxPersentDict[timeItem] = percent
            tmpInfo = common.fullTmpInfoClass(tmpInfo, timeItem, percent, time)
    else:
        timeAndMaxPersentDict[timeItem] = percent
        if abs(tmpInfo.maxPercent) < abs(percent):
            tmpInfo = common.fullTmpInfoClass(tmpInfo, timeItem, percent, time)
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
        message += common.createMessage(message, coinSearcher.pairName, tmpInfo.typeOfValue, percent, tmpInfo.tBegin, tmpInfo.tEnd)
    tmpInfo = common.cleanTmpInfoClass(tmpInfo)
    return(coinSearcher.timeAndMaxPersentDict, message)



def calculations(workingInfo: classes.WorkingInfo, coinsDicts: classes.CoinSearcher, tmpInfo: classes.TmpPairInfo, data: float, time: str, message: str):
    coinsDicts.coinPairData, err = common.checkBeginig(coinsDicts.coinPairData, data, time)
    if err == 3:
        return(coinsDicts, message, "", 3)
    lastTimeOfValue, lastValue, errMessage, err = common.getLastValueFromDict(coinsDicts.coinPairData)
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
        message = common.createMessage(message, coinsDicts.pairName, tmpInfo.typeOfValue, percent, lastTimeOfValue, time)
    coinsDicts.coinPairData = common.trimDict(coinsDicts.coinPairData, workingInfo.delimeter)
    coinsDicts.timeAndMaxPersentDict = common.trimDict(coinsDicts.timeAndMaxPersentDict, workingInfo.delimeter)
    coinsDicts.timeAndMaxPersentDict, message = findMaxInDict(coinsDicts, tmpInfo, workingInfo, data, time, message)
    coinsDicts.coinPairData[time] = data
    return(coinsDicts, message, "", 0)


