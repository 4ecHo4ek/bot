import modules as mod
import commonFuncs as common
import classes as classes



def getVolumeInfo(pairInfo: classes.CoinPairBasic, workingInfo: classes.WorkingInfo, coinsDicts: classes.CoinSearcher, time: str):
    tmpInfo = classes.TmpPairInfo(0, "", "", "volume")
    coinsDicts = common.calculations(workingInfo, coinsDicts, tmpInfo, pairInfo.volume, time)
    return(coinsDicts)


def getLastPriceInfo(pairInfo: classes.CoinPairBasic, coinsDicts: classes.CoinSearcher, workingInfo: classes.WorkingInfo, time: str):
    tmpInfo = classes.TmpPairInfo(0, "", "", "lastPrice")
    coinsDicts = common.calculations(workingInfo, coinsDicts, tmpInfo, pairInfo.lastPrice, time)
    return(coinsDicts)


def sortThroughPairs(coinsDicts: classes.DictsSaver, workingInfo: classes.WorkingInfo, pairs: dict, time: str):
    for pair in pairs:
        pairInfo, errMessage, err = common.getInfoFromDictOfPairs(pair)
        if err == 3:
            # print(errMessage)
            continue
        coinsDicts = common.createDictsSaverElements(pairInfo.pairName, coinsDicts)
        coinsDicts.coinsDictVolume[pairInfo.pairName], errMessage, err = getVolumeInfo(pairInfo, workingInfo, coinsDicts.coinsDictVolume[pairInfo.pairName], time)
        if err == 3:
            continue
        coinsDicts.coinsDictLastPrice[pairInfo.pairName], errMessage, err = getLastPriceInfo(pairInfo, workingInfo, coinsDicts.coinsDictLastPrice[pairInfo.pairName], time)
        if err == 3:
            continue
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
    
    # message = f"nothing interesting less the {workingInfo.notInterestingPercent}% and much interest up {workingInfo.attentionPercent}%"
    # bot.sendMessage(message)
    print(f"nothing interesting less the {workingInfo.notInterestingPercent}% and much interest up {workingInfo.attentionPercent}%")

    coinsDicts = classes.DictsSaver({}, {})

    while True:
        common.waitNewMinute()
        pairs, errMessage, err = common.getInfo(client)
        if err == 2:
            common.writeLog(workingInfo.logFileName, "error", errMessage)
            continue
        time = f"{mod.datetime.datetime.now().hour}:{mod.datetime.datetime.now().minute}"
        coinsDicts = sortThroughPairs(coinsDicts, workingInfo, pairs, time)
        # print("test")
        mod.time.sleep(3)


        



if __name__ == "__main__":
    if len (mod.sys.argv) > 1:
        mainFunc(str(mod.sys.argv[1]))
    else:
        print ("\ngive values file\n")
    





# # def func(value: type) -> type:
# #     ...
# #     return(value, err)




