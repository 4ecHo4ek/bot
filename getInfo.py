import modules as mod
import commonFuncs as common
import classes as classes


def getVolume(workingInfo: classes.WorkingInfo, coinsDicts: classes.CoinSearcher,  data: float, time: str, type: str):
    tmpInfo = classes.TmpPairInfo(0, "", "", type)
    coinsDicts, message, errMessage, err = common.calculations(workingInfo, coinsDicts, tmpInfo, data, time)
    return(coinsDicts, message, errMessage, err)


def sortThroughPairs(coinsDicts: classes.DictsSaver, workingInfo: classes.WorkingInfo, pairs: dict, time: str):
    for pair in pairs:
        pairInfo, errMessage, err = common.getInfoFromDictOfPairs(pair)
        if err == 3:
            # print(errMessage)
            continue
        coinsDicts = common.createDictsSaverElements(pairInfo.pairName, coinsDicts)
        # coinsDicts.coinsDictVolume[pairInfo.pairName], errMessage, err = getVolumeInfo(pairInfo, workingInfo, coinsDicts.coinsDictVolume[pairInfo.pairName], time)
        coinsDicts.coinsDictVolume[pairInfo.pairName], coinsDicts.message, errMessage, err = getVolume(workingInfo, coinsDicts.coinsDictVolume[pairInfo.pairName], pairInfo.volume, time, "volume")
        if err == 3:
            continue
        # coinsDicts.coinsDictLastPrice[pairInfo.pairName], errMessage, err = getLastPriceInfo(pairInfo, workingInfo, coinsDicts.coinsDictLastPrice[pairInfo.pairName], time)
        coinsDicts.coinsDictLastPrice[pairInfo.pairName], coinsDicts.message, errMessage, err = getVolume(workingInfo, coinsDicts.coinsDictLastPrice[pairInfo.pairName], pairInfo.lastPrice, time, "lastPrice")
        if err == 3:
            continue

        # if pairInfo.pairName == "IDEUR":
        #     print(pairInfo.pairName)
        #     coinsDicts.message += "one\n"
        #     coinsDicts.message += "two\n"

    return(coinsDicts) # err


def botLogs(workingInfo: classes.WorkingInfo, r):
    if r.status_code == 500:
        common.writeLog(workingInfo.logFileName, "error", f"uncorrect reques to server {r.status_code} {r.reason}")
    elif r.status_code == 404:
        common.writeLog(workingInfo.logFileName, "error", f"bot error {r.status_code} {r.reason}")
    elif r.status_code != 200:
        common.writeLog(workingInfo.logFileName, "error", f"connetion to bot failed {r.status_code} {r.reason}")
    print(r.status_code, r.reason)


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

    coinsDicts = classes.DictsSaver({}, {}, "")
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
            botLogs(workingInfo, r)
        mod.time.sleep(3)


if __name__ == "__main__":
    if len (mod.sys.argv) > 1:
        mainFunc(str(mod.sys.argv[1]))
    else:
        print ("\ngive values file\n")
    

# # def func(value: type) -> type:
# #     ...
# #     return(value, err)



#  составляем большое соообщение из всех сообщений для бота и в конце вызываем бота и отправляем все скопом



