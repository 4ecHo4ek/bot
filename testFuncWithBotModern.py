import modules as mod
import internalClasses as inClass


        
def mainFunc(fileName: str) -> None:
    errMessage, err, workingInfo, bot = inClass.common.getDataFromFile(fileName)
    if err:
        print(errMessage)
        exit
    
    print(workingInfo.logFileName)
    print(bot.chat_id)
    print(bot.telegram_token)

    coinsDicts = inClass.classes.DictsSaver({}, {})
    try:
        bot = inClass.classes.BotClass(bot.telegram_token, bot.chat_id)
    except:
        # inClass.common.writeLog(workingInfo.logFileName, "error", f"Could not connect to bot")
        exit

    try:
        client = mod.Client(workingInfo.api_key, workingInfo.api_secret)
    except:
        # inClass.common.writeLog(workingInfo.logFileName, "error", f"Could not connect to server {client}")
        exit
    
    message = f"nothing interesting less the {workingInfo.notInterestingPercent}% and much interest up {workingInfo.attentionPercent}%"
    bot.sendMessage(message)

    # while True:
    #     coinsDicts = getInfo(client, workingInfo, coinsDicts)
    # # for i in range(0, 60):
    #     waitNewMinute(workingInfo)
    #     print(datetime.datetime.now())
    #     timeBegining = time()
    #     coinsDicts = getInfo(client, workingInfo, coinsDicts, bot)
    #     sleep(1)
    #     print(f"working time is {time() - timeBegining}")

        



if __name__ == "__main__":
    if len (mod.sys.argv) > 1:
        mainFunc(str(mod.sys.argv[1]))
    else:
        print ("\ngive values file\n")






# # def func(value: type) -> type:
# #     ...
# #     return(value, err)




