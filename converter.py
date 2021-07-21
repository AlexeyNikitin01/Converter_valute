import json
import requests

class Converter:
    """Converter valute"""
    def __init__(self, one_curr, two_curr, money):
        self.one_curr = one_curr
        self.two_curr = two_curr
        self.money = money 

    def api_json(self):
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        value = requests.get(url).json()
        return value

    #Переменные для валют и проверка на корректное введение
    def currency(self, one_curr, two_curr):
        #Вызов словарика API
        value = self.api_json()
        #проверка на верность ввода валют
        if (self.one_curr in value["Valute"] or self.one_curr == "RUS") and (self.two_curr in value["Valute"] or self.two_curr == "RUS"):
            return self.one_curr, self.two_curr
        elif (not self.one_curr in value["Valute"]) or (not self.two_curr in value["Valute"]):
            return False
        
    #метод для ввода денег, необходимых перевода из первой валюты, и проверка колличества денежных средств
    def input_money(self, money):
        #Исключения для ввода неверного значения денег
        try:
            float(self.money)
            return float(self.money)
        except ValueError:
            return False

    #метод для условия перевода валют и вывод конвернтированной валюты
    def converter(self, one_curr, two_curr, money):
        #Вызов словарика API
        value = self.api_json()
        self.money = self.input_money(self.money)
        #Проверка на верный ввод данных
        if self.currency(self.one_curr, self.two_curr) == False:
            return 'Нет такой валюты'
        elif self.input_money(self.money) == False:
            return 'Надо число денег'
        else:
            #Проверка на ввод валюты и вывод денег
            if self.one_curr == "RUS" and self.two_curr == "RUS":
                converter = self.money
            elif self.one_curr == "RUS":
                converter = (1/value["Valute"][self.two_curr]["Value"])*self.money
            elif self.two_curr == "RUS":
                converter = (value["Valute"][self.one_curr]["Value"]/1)*self.money
            elif (self.one_curr in value["Valute"]) and (self.two_curr in value["Valute"]):
                converter = (value["Valute"][self.one_curr]["Value"]/value["Valute"][self.two_curr]["Value"])*self.money
            return round(converter, 2)
