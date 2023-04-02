import modules as mod
import commonFuncs as common
import classes as classes
import calculating as calc


def getVolume(workingInfo: classes.WorkingInfo, coinsDicts: classes.CoinSearcher,  data: float, time: str, type: str, message: str):
    tmpInfo = classes.TmpPairInfo(0, "", "", type)
    coinsDicts, message, errMessage, err = calc.calculations(workingInfo, coinsDicts, tmpInfo, data, time, message)
    return(coinsDicts, message, errMessage, err)


def sortThroughPairs(coinsDicts: classes.DictsSaver, workingInfo: classes.WorkingInfo, pairs: dict, time: str):
    coinsDicts.message = ""
    for pair in pairs:
        pairInfo, errMessage, err = common.getInfoFromDictOfPairs(pair)
        if err == 3:
            # print(errMessage)
            continue

        # TEST
        if pairInfo.pairName == "WINGUSDT":
            print(pair)

        coinsDicts = common.createDictsSaverElements(pairInfo.pairName, coinsDicts)
        coinsDicts.coinsDictVolume[pairInfo.pairName], coinsDicts.message, errMessage, err = getVolume(workingInfo, 
                                                                                                       coinsDicts.coinsDictVolume[pairInfo.pairName], 
                                                                                                       pairInfo.volume, time, "volume", coinsDicts.message)
        if len(errMessage) > 0:
            common.writeLog(workingInfo.logFileName, "error", errMessage)
        elif err == 3:
            continue
        coinsDicts.coinsDictLastPrice[pairInfo.pairName], coinsDicts.message, errMessage, err = getVolume(workingInfo, 
                                                                                                          coinsDicts.coinsDictLastPrice[pairInfo.pairName], 
                                                                                                          pairInfo.lastPrice, time, "lastPrice", coinsDicts.message)
        if len(errMessage) > 0:
            common.writeLog(workingInfo.logFileName, "error", errMessage)
        elif err == 3:
            continue
        coinsDicts.coinsDictQuoteVolume[pairInfo.pairName], coinsDicts.message, errMessage, err = getVolume(workingInfo, 
                                                                                                          coinsDicts.coinsDictQuoteVolume[pairInfo.pairName], 
                                                                                                          pairInfo.lastPrice, time, "quoteVolume", coinsDicts.message)
        if len(errMessage) > 0:
            common.writeLog(workingInfo.logFileName, "error", errMessage)
        elif err == 3:
            continue

    return(coinsDicts) # err


def mainFunc(fileName: str) -> None:
    errMessage, err, workingInfo = common.getDataFromFile(fileName)
    if err:
        print(errMessage)
        exit
    client, errMessage, err = common.getConnectionsToResources(workingInfo)
    if err == 1:
        common.writeLog(workingInfo.logFileName, "error", errMessage)
        exit

    print(f"nothing interesting less the {workingInfo.notInterestingPercent}% and much interest up {workingInfo.attentionPercent}%")

    coinsDicts = classes.DictsSaver({}, {}, {}, "")
    while True:
        common.waitNewMinute()
        pairs, errMessage, err = common.getInfo(client)
        if err == 2:
            common.writeLog(workingInfo.logFileName, "error", errMessage)
            continue
        time = f"{mod.datetime.datetime.now().hour}:{mod.datetime.datetime.now().minute}"
        coinsDicts = sortThroughPairs(coinsDicts, workingInfo, pairs, time)
        if len(coinsDicts.message) > 0:
            r = mod.requests.post(f"{workingInfo.url}:{workingInfo.port}/sendMessage", json={'message': coinsDicts.message})
            coinsDicts.message = ""
            common.botLogs(workingInfo, r)
        mod.time.sleep(3)


if __name__ == "__main__":
    if len (mod.sys.argv) > 1:
        mainFunc(str(mod.sys.argv[1]))
    else:
        print ("\ngive values file\n")


# зделать вывод лога в одном месте, вначале собираем всю инфу и передаем ее, потом в 1 момент выводим