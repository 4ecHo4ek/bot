import modules as mod

# рабочая информация о настройках поиска и работы
class WorkingInfo:
    def __init__(self, delimeter: int, deltaPercent: float, logFileName: str, maxPersent: float, steps: int, api_key: str, api_secret: str) -> None:
        # макисмальный рассматриваемый диапазон по времени в минутах
        self.delimeter = delimeter
        # разница в проценте, после которой обращаем вниманиеб пока не используется
        self.deltaPercent = deltaPercent
        # название лог файла
        self.logFileName = logFileName
        # максимальный процент, после которого начинать бить тревогу
        self.maxPersent = maxPersent
        # количество шагов для измерения процентов, каждый последующий шаг = деление на 2 процента от предыдущего шага: maxPersent, maxPersent/2, maxPersent/4...
        self.steps = steps
        # бинансовые потраха
        self.api_key = api_key
        self.api_secret = api_secret
        # получаем массив с процентами, по которым будем проводить выборку
        self.persentArraysForLooking = [maxPersent]

        # TODO продумать как вытаскивать эти проценты для сравнения
        for _ in range(1, steps):
            maxPersent = maxPersent / 2
            self.persentArraysForLooking.append(maxPersent)
        arrLen = int(len(self.persentArraysForLooking) / 2)
        interestArr = self.persentArraysForLooking[:arrLen + 1]
        # получаем минимальную границу, ниже которой не рассматриваем значения
        self.notInterestingPercent = round(float(self.persentArraysForLooking[arrLen]), 2)
        # в промежутке между нижней и верхней границей оповещаем только о макисмальном %, и продумать как отсеивать незначительный рост
        arrLen = int(len(interestArr) / 2)
        # получаем максимальный процент, после которого сразу оповещаеть
        self.attentionPercent = round(float(interestArr[arrLen]), 2)


class BotClass():
    def __init__(self, telegram_token: str, chat_id: int) -> None:
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        

    def sendMessage(self, message) -> None:
        bot = mod.telebot.TeleBot(self.telegram_token)
        bot.send_message(self.chat_id, message)


# класс для сохранения значений для каждой пары
class DictsSaver:
    def __init__(self, coinsDictVolume: dict, coinsDictLastPrice: dict, message: str) -> None:
        self.coinsDictVolume = coinsDictVolume
        self.coinsDictLastPrice = coinsDictLastPrice
        self.message = message


class CoinPairBasic:
    def __init__(self, pairName, lastPrice, volume, quoteVolume) -> None:
        self.pairName = pairName # название пары
        self.lastPrice = lastPrice # цена 
        self.volume = volume # объем торгов 1ой монеты
        self.quoteVolume = quoteVolume # объем торгов 2ой монеты


class CoinSearcher:
    def __init__(self, pairName: str, coinPairData: dict, timeAndMaxPersentDict: dict) -> None:
        self.pairName = pairName
        # храним предыдущее значение для сравнения
        self.coinPairData = coinPairData
        # словарь для хранения времени и максимального процента, который был относительно этого времени (для уменьшения повторных срабатываний)
        self.timeAndMaxPersentDict = timeAndMaxPersentDict


# запоминаем крайние значения для сверки с последующим
class TmpPairInfo:
    def __init__(self, maxPercent: float, tBegin: str, tEnd: str, typeOfValue: str) -> None:
        self.maxPercent = maxPercent
        self.tBegin = tBegin
        self.tEnd = tEnd
        self.typeOfValue = typeOfValue

    def clean(self):
        self.maxPercent = 0
        self.tBegin = ""
        self.tEnd = ""
        self.typeOfValue = ""
                