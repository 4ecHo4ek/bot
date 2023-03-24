import modules as mod
import commonFuncs as common
import classes as classes





def getVolumeInfo(pairInfo: classes.CoinPairBasic, workingInfo: classes.WorkingInfo, coinsDicts: classes.CoinSearcher, time: str):
    tmpInfo = classes.TmpPairInfo(0, "", "", "volume")
    # ....
    # coinsDictVolume - CoinSearcher
    coinsDicts.coinPairData, err = common.checkBeginig(coinsDicts.coinPairData, pairInfo.volume, time)
    if err == 3:
        return(coinsDicts, "", 3)
    lastTimeOfValue, lastValue, errMessage, err = common.getLastValueFromDict(coinsDicts.coinPairData)
    if err == 2:
        return(coinsDicts, "", 3)
    elif err == 3:
        coinsDicts.coinPairData[time] = pairInfo.volume
        return(coinsDicts, "", 0)
    percent = common.calcPersent(pairInfo.volume, lastValue)
    if abs(percent) >= abs(workingInfo.notInterestingPercent):
        coinsDicts.coinPairData[time] = pairInfo.volume
        return(coinsDicts, "", 0)
    if abs(percent) >= abs(workingInfo.attentionPercent):
        coinsDicts.timeAndMaxPersentDict[time] = percent
        # здесь должно быть оповещение
        # bot.sendMessage(message)
        pass
    coinsDicts.coinPairData = common.trimDict(coinsDicts.coinPairData, workingInfo.delimeter)
    coinsDicts.timeAndMaxPersentDict = common.trimDict(coinsDicts.timeAndMaxPersentDict, workingInfo.delimeter)


    # coinSearcher.timeAndMaxPersentDict = findMaxInDicts(coinSearcher, tmpInfo, workingInfo, bot, data, lastValue, time)


    coinsDicts.coinPairData[time] = pairInfo.volume
    pass






def getLastPriceInfo(pairInfo: classes.CoinPairBasic, coinsDicts: classes.CoinSearcher, workingInfo: classes.WorkingInfo, time: str):
    tmpInfo = classes.TmpPairInfo(0, "", "", "lastPrice")
    # ....
    pass


def sortThroughPairs(workingInfo: classes.WorkingInfo, pairs: dict, time: str):
    for pair in pairs:
        pairInfo, errMessage, err = common.getInfoFromDictOfPairs(pair)
        if err == 3:
            print(errMessage)
            continue
        coinsDicts = common.createDictsSaverElements(pairInfo.pairName, coinsDicts)
        # coinsDicts.coinsDictVolume[pairName] = CoinSearcher(pairName, {}, {})
        coinsDicts.coinsDictVolume[pairInfo.pairName], errMessage, err = getVolumeInfo(pairInfo, workingInfo, coinsDicts.coinsDictVolume[pairInfo.pairName], time)
        # err
        coinsDicts.coinsDictLastPrice[pairInfo.pairName], errMessage, err = getLastPriceInfo(pairInfo, workingInfo, coinsDicts.coinsDictLastPrice[pairInfo.pairName], time)
        # err
    return(coinsDicts) # err

        
def mainFunc(fileName: str) -> None:
    errMessage, err, workingInfo, bot = common.getDataFromFile(fileName)
    if err:
        print(errMessage)
        exit
    bot, client, errMessage, err = common.getConnectionsToResources(bot, workingInfo)
    if err == 1:
        common.writeLog(workingInfo.logFileName, "error", errMessage)
        exit
    
    message = f"nothing interesting less the {workingInfo.notInterestingPercent}% and much interest up {workingInfo.attentionPercent}%"
    bot.sendMessage(message)

    coinsDicts = classes.DictsSaver({}, {})

    while True:
        # common.waitNewMinute()
        pairs, errMessage, err = common.getInfo(client)
        if err == 2:
            common.writeLog(workingInfo.logFileName, "error", errMessage)
            continue
        time = f"{mod.datetime.datetime.now().hour}:{mod.datetime.datetime.now().minute}"

        mod.time.sleep(1)


        



if __name__ == "__main__":
    if len (mod.sys.argv) > 1:
        mainFunc(str(mod.sys.argv[1]))
    else:
        print ("\ngive values file\n")
    





# # def func(value: type) -> type:
# #     ...
# #     return(value, err)




