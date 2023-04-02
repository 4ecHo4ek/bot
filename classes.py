import modules as mod

# рабочая информация о настройках поиска и работы
class WorkingInfo:
    def __init__(self, delimeter: int, deltaPercent: float, logFileName: str, maxPersent: float, steps: int, api_key: str, api_secret: str, url: str, port: int) -> None:
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
        self.url = url
        self.port = port
        # получаем массив с процентами, по которым будем проводить выборку
        self.persentArraysForLooking = []

        # TODO продумать как вытаскивать эти проценты для сравнения
        for i in range(1, steps + 1):
            self.persentArraysForLooking.append(round(maxPersent / mod.math.sqrt(i), 3))
        self.notInterestingPercent = self.persentArraysForLooking[-1]
        self.attentionPercent = self.persentArraysForLooking[int(len(self.persentArraysForLooking) / 2) - int(len(self.persentArraysForLooking) / 4)]



# класс для сохранения значений для каждой пары
class DictsSaver:
    def __init__(self, coinsDictVolume: dict, coinsDictLastPrice: dict, message: str, errMessage: str) -> None:
        self.coinsDictVolume = coinsDictVolume
        self.coinsDictLastPrice = coinsDictLastPrice
        self.message = message
        self.errMessage = errMessage


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
                