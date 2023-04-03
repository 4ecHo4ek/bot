from flask import Flask, request, jsonify
import telebot
# from twilio import twiml
import sys
import os
import subprocess


app = Flask(__name__)
global telegram_token
global chat_id


def trimString(string: str) -> str:
    string = string[string.find(":") + 1:]
    if string[0] == " ":
        string = string[1:].replace("\n", "")
    return(string)


def findDataInReadedFile(lines: list[str]):
    for line in lines:
        if 'telegram_token' in line:
            telegram_token = trimString(line)
        elif 'chat_id' in line:
            chat_id = int(trimString(line))
    return(telegram_token, chat_id)


def getDataFromFile(fileName: str):
    if os.path.exists(fileName):
        try:
            with open(fileName,'r') as file:
                lines = file.readlines()
                telegram_token, chat_id = findDataInReadedFile(lines)
            return(telegram_token, chat_id)
        except:
            print(f"could read fild {fileName}\n")
            exit
    else:
        print(f"could not fild {fileName}\n")
        exit


@app.route('/sendMessage', methods=['POST']) 
def sendMessage():
    data = request.json
    message = data["message"]
    bot = telebot.TeleBot(telegram_token)
    bot.send_message(chat_id, message)
    return jsonify(data)


@app.route('/startTradeBot', methods=['POST']) 
def startTradeBot():
    data = request.json
    pairName = data["pairName"]

    subprocess.Popen([sys.executable, "test.py", pairName])




    return jsonify(data)




if __name__ == "__main__":
    str(sys.argv[1])
    
    if len (sys.argv) > 1:
        telegram_token, chat_id = getDataFromFile(str(sys.argv[1]))
        app.run()
    else:
        print ("\ngive values file\n")

# http://127.0.0.1:5000/sendMessage