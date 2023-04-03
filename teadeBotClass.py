import os
from binance.spot import Spot as Client
from py3cw.request import Py3CW



class TradeBotClass:
    def __init__(self, pairName, fileName) -> None:
        self.pairName = pairName
        self.maxPerice = 0
        self.err = False
        self.getInfoFromFile(fileName)


    def trimString(string: str) -> str:
        string = string[string.find(":") + 1:]
        if string[0] == " ":
            string = string[1:]
            string = string.replace("\n", "")
        return(string)


    def getInfoFromFile(self, fileName: str):
        if os.path.exists(fileName):
            try:
                with open(fileName,'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        if "api_key" in line:
                            self.api_key = self.trimString(line)
                        elif "api_secret" in line:
                            self.api_secret = self.trimString(line)
                        elif "botSecret" in line:
                            self.botSecret = self.trimString(line)
                        elif "botApi_key" in line:
                            self.botApi_key = self.trimString(line)
                        elif "account_id" in line:
                            self.account_id = self.trimString(line) # int?
                        elif "stopPersent" in line:
                            self.stopPersent = int(self.trimString(line))
            except:
                self.err = True
        else:
            self.err = True


    def stopBot(self):
        client = Client(self.api_key, self.api_secret)
        pairInfo = Client.ticker_24hr(client, symbol=self.pairName)
        lastPrice = round(float(pairInfo['lastPrice']), 2)
        if self.maxPerice * (1 - self.stopPersent / 100 ) >= lastPrice:
            return(True)
        return(False)



p3cw = Py3CW(
    key='8cd7e5f860ec414185061704466526f11a78d16bb2cc4255affa8722e35c8887', 
    secret='350dc6b84223f0b7044ff3c877479cf02222732c81dbec76b00bea18973adb5028e2487a58162d1a4054dd6b9b3c6b04575d43436554ee4f11f92a39f74a8fa6ba7fa298171e05eee7c0048461c53cb32f6a33510e7b160e86e0197c7bcb0e3748b500bd',
    request_options={
        'request_timeout': 10,
        'nr_of_retries': 1,
        'retry_status_codes': [502],
        'retry_backoff_factor': 0.1
    }
)

print(p3cw.request(entity="accounts", action="account_id"))

# With no action
# Destruct response to error and data
# and check first if we have an error, otherwise check the data
# error, data = p3cw.request(
#     entity='smart_trades_v2',
#     action=''
# )

# # With payload data
# # Destruct response to error and data
# # and check first if we have an error, otherwise check the data
# error, data  = p3cw.request(
#     entity='smart_trades_v2', 
#     action='new', 
#     payload={
#         "account_id": 123456,
#     }
# )

# # With action_id replaced in URL
# # Destruct response to error and data
# # and check first if we have an error, otherwise check the data
# error, data = p3cw.request(
#     entity='smart_trades_v2', 
#     action='get_by_id',
#     action_id='123456'
# )






# GET /ver1/bots
# curl -H "Apikey: 8cd7e5f860ec414185061704466526f11a78d16bb2cc4255affa8722e35c8887" -H "Secret: 350dc6b84223f0b7044ff3c877479cf02222732c81dbec76b00bea18973adb5028e2487a58162d1a4054dd6b9b3c6b04575d43436554ee4f11f92a39f74a8fa6ba7fa298171e05eee7c0048461c53cb32f6a33510e7b160e86e0197c7bcb0e3748b500bd" -X POST 'https://api.3commas.io/public/api/ver1/bots'



# Имя: testBot

# API key:
# 8cd7e5f860ec414185061704466526f11a78d16bb2cc4255affa8722e35c8887


# Secret:
# 350dc6b84223f0b7044ff3c877479cf02222732c81dbec76b00bea18973adb5028e2487a58162d1a4054dd6b9b3c6b04575d43436554ee4f11f92a39f74a8fa6ba7fa298171e05eee7c0048461c53cb32f6a33510e7b160e86e0197c7bcb0e3748b500bd
