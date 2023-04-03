import commonFuncs as common
import classes as classes



def calcPersent(currentValue: float, lastValue: float):
    return(round(float(1 - currentValue / lastValue), 2))


def checkValuesWithMoreThenMaxPersent(workingInfo: classes.WorkingInfo, tmpInfo: classes.TmpPairInfo, coinSearcher: classes.CoinSearcher, timeAndMaxPersentDict: dict, timeItem: float, time: str, percent: float):
    '''
    поиск интересующего процента
    timeItem - время, которое мы сравниваем
    time - текущее время
    '''
    message = ""
    if timeItem in timeAndMaxPersentDict:
        if abs(timeAndMaxPersentDict[timeItem]) < abs(percent) and abs(tmpInfo.maxPercent) < abs(percent):
            timeAndMaxPersentDict[timeItem] = percent
            tmpInfo = common.fullTmpInfoClass(tmpInfo, timeItem, percent, time)
            message = common.createMessage(coinSearcher.pairName, tmpInfo.typeOfValue, percent, tmpInfo.tBegin, tmpInfo.tEnd)
    else:
        if abs(tmpInfo.maxPercent) < abs(percent):
            timeAndMaxPersentDict[timeItem] = percent
            tmpInfo = common.fullTmpInfoClass(tmpInfo, timeItem, percent, time)
            message = common.createMessage(coinSearcher.pairName, tmpInfo.typeOfValue, percent, tmpInfo.tBegin, tmpInfo.tEnd)
    if len(message) > 0:
        common.sendMessage(workingInfo, message)
        common.writeLog(workingInfo.logFileName, "info", f"checkValuesWithMoreThenMaxPersent - {message}")
    return(timeAndMaxPersentDict, tmpInfo)


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



def findMaxInDict(coinSearcher: classes.CoinSearcher, tmpInfo: classes.TmpPairInfo, workingInfo: classes.WorkingInfo, data: float, time: str):
    for timeItem in coinSearcher.coinPairData:
        previosValue = coinSearcher.coinPairData[timeItem]
        if previosValue == 0:
            continue
        percent = calcPersent(data, previosValue)

        common.testDataCollecting(coinSearcher.pairName, f"findMaxInDict - percent - {percent} / data, previosValue - {data, previosValue}") # TEST
    
        if abs(percent) <= abs(workingInfo.notInterestingPercent):
            continue
        if abs(percent) >= abs(workingInfo.attentionPercent):

            common.testDataCollecting(coinSearcher.pairName, f"findMaxInDict - before checkValuesWithMoreThenMaxPersent len(coinSearcher.timeAndMaxPersentDict) - {len(coinSearcher.timeAndMaxPersentDict)}") # TEST
    
            coinSearcher.timeAndMaxPersentDict, tmpInfo = checkValuesWithMoreThenMaxPersent(workingInfo, tmpInfo, coinSearcher, 
                                                                                            coinSearcher.timeAndMaxPersentDict, 
                                                                                            timeItem, time, percent)
            
            common.testDataCollecting(coinSearcher.pairName, f"findMaxInDict - after checkValuesWithMoreThenMaxPersent len(coinSearcher.timeAndMaxPersentDict) - {len(coinSearcher.timeAndMaxPersentDict)}") # TEST
    
            continue
        tmpInfo, coinSearcher.timeAndMaxPersentDict = checkValuesWithInterestingPersent(tmpInfo, coinSearcher.timeAndMaxPersentDict, 
                                                                                        timeItem, percent, time)

    if abs(tmpInfo.maxPercent) > abs(workingInfo.notInterestingPercent):
        message = common.createMessage(coinSearcher.pairName, tmpInfo.typeOfValue, percent, tmpInfo.tBegin, tmpInfo.tEnd)
        common.sendMessage(workingInfo, message)
        common.writeLog(workingInfo.logFileName, "info", f"findMaxInDict - {message}")
    tmpInfo = common.cleanTmpInfoClass(tmpInfo)
    return(coinSearcher.timeAndMaxPersentDict)



def calculations(workingInfo: classes.WorkingInfo, coinsDicts: classes.CoinSearcher, tmpInfo: classes.TmpPairInfo, data: float, time: str):
    coinsDicts.coinPairData, err = common.checkBeginig(coinsDicts.coinPairData, data, time)
    if err == 3:
        return(coinsDicts, "", 3)
    lastTimeOfValue, lastValue, errMessage, err = common.getLastValueFromDict(coinsDicts.coinPairData)

    common.testDataCollecting(coinsDicts.pairName, f"calculations - lastTimeOfValue, lastValue - {lastTimeOfValue, lastValue}") # TEST
    
    if err == 2:
        return(coinsDicts, errMessage, 3)
    elif err == 3 or lastValue == 0:
        coinsDicts.coinPairData[time] = data
        return(coinsDicts, "", 0)
    percent = calcPersent(data, lastValue)
    coinsDicts.coinPairData[time] = data
    
    common.testDataCollecting(coinsDicts.pairName, f"calculations - len(coinsDicts.coinPairData) - {len(coinsDicts.coinPairData)}, percent - {percent}") # TEST
    
    if abs(percent) <= abs(workingInfo.notInterestingPercent):
        coinsDicts.coinPairData = common.trimDict(coinsDicts.coinPairData, workingInfo.delimeter)
        return(coinsDicts, "", 0)
    elif abs(percent) >= abs(workingInfo.attentionPercent):
        coinsDicts.timeAndMaxPersentDict[time] = percent
        message = common.createMessage(coinsDicts.pairName, tmpInfo.typeOfValue, percent, lastTimeOfValue, time)
        common.sendMessage(workingInfo, message)
        common.writeLog(workingInfo.logFileName, "info", f"calculations - {message}")
    coinsDicts.coinPairData = common.trimDict(coinsDicts.coinPairData, workingInfo.delimeter)
    coinsDicts.timeAndMaxPersentDict = common.trimDict(coinsDicts.timeAndMaxPersentDict, workingInfo.delimeter)
    coinsDicts.timeAndMaxPersentDict = findMaxInDict(coinsDicts, tmpInfo, workingInfo, data, time)

    common.testDataCollecting(coinsDicts.pairName, f"calculations - len(coinsDicts.timeAndMaxPersentDict) - {len(coinsDicts.timeAndMaxPersentDict)}, coinsDicts.timeAndMaxPersentDict - {coinsDicts.timeAndMaxPersentDict}") # TEST
    common.testDataCollecting(coinsDicts.pairName, f"calculations - len(coinsDicts.coinPairData) - {len(coinsDicts.coinPairData)}, coinsDicts.coinPairData - {coinsDicts.coinPairData}") # TEST
    
    return(coinsDicts, "", 0)


