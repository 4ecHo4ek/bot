import modules as mod
import internalClasses as inClass








def getVolumeInfo(pairInfo: inClass.classes.CoinPairBasic, coinsDicts: inClass.classes.CoinSearcher, workingInfo: inClass.classes.WorkingInfo, time: str):
    tmpInfo = inClass.classes.TmpPairInfo(0, "", "", "volume")
    # ....
    pass


def getLastPriceInfo(pairInfo: inClass.classes.CoinPairBasic, coinsDicts: inClass.classes.CoinSearcher, workingInfo: inClass.classes.WorkingInfo, time: str):
    tmpInfo = inClass.classes.TmpPairInfo(0, "", "", "lastPrice")
    # ....
    pass


def sortThroughPairs(workingInfo: inClass.classes.WorkingInfo, pairs: dict, time: str):
    for pair in pairs:
        pairInfo, errMessage, err = inClass.common.getInfoFromDictOfPairs(pair)
        if err == 2:
            print(errMessage)
            continue
        coinsDicts = inClass.common.createNewElements(pairInfo.pairName, coinsDicts)
        coinsDicts.coinsDictVolume[pairInfo.pairName] = getVolumeInfo(pairInfo, coinsDicts.coinsDictVolume[pairInfo.pairName], workingInfo, time)
        # err
        coinsDicts.coinsDictLastPrice[pairInfo.pairName] = getLastPriceInfo(pairInfo, coinsDicts.coinsDictLastPrice[pairInfo.pairName], workingInfo, time)
        # err
    return(coinsDicts) # err

        
def mainFunc(fileName: str) -> None:
    errMessage, err, workingInfo, bot = inClass.common.getDataFromFile(fileName)
    if err:
        print(errMessage)
        exit
    bot, client, errMessage, err = inClass.common.getConnectionsToResources(bot, workingInfo)
    if err == 1:
        inClass.common.writeLog(workingInfo.logFileName, "error", errMessage)
        exit
    
    message = f"nothing interesting less the {workingInfo.notInterestingPercent}% and much interest up {workingInfo.attentionPercent}%"
    bot.sendMessage(message)

    coinsDicts = inClass.classes.DictsSaver({}, {})

    while True:
        inClass.common.waitNewMinute()
        pairs, errMessage, err = inClass.common.getInfo(client)
        if err == 2:
            inClass.common.writeLog(workingInfo.logFileName, "error", errMessage)
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




