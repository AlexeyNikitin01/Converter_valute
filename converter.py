import requests
import json


class Converter:
    """Converter valute"""
    def __init__(self, first_valute, second_valute, money):
        self.first_valute = first_valute
        self.second_valute = second_valute
        self.money = money 

    #API 
    def api_json(self):
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        value = requests.get(url).json()
        return value

    #Правильный ввод валют
    def input_valute(self, first_valute, second_valute):
        value = self.api_json()
        
        if ((self.first_valute in value["Valute"] or self.first_valute == "RUB") and 
                (self.second_valute in value["Valute"] or self.second_valute == "RUB")):
            return self.first_valute, self.second_valute
        elif ((not self.first_valute in value["Valute"]) or 
                (not self.second_valute in value["Valute"])):
            return 
        
    #Обработка ввода денег
    def input_money(self, money):
        try:
            float(self.money)
            return float(self.money)
        except ValueError:
            return False

    def convert(self, first_valute, second_valute, money):
        value = self.api_json()
        self.money = self.input_money(self.money)
   
        if self.input_valute(self.first_valute, self.second_valute) == None:
            return 'Нет такой валюты'
        elif self.input_money(self.money) == False:
            return 'Надо число денег'
        else:
            #Конвертирование валюты
            if self.first_valute == "RUB" and self.second_valute == "RUB":
                converter = self.money
            elif self.first_valute == "RUB":
                converter = self.money/value["Valute"][self.second_valute]["Value"]
            elif self.second_valute == "RUB":
                converter = value["Valute"][self.first_valute]["Value"]*self.money
            elif ((self.first_valute in value["Valute"]) and 
                    (self.second_valute in value["Valute"])):
                converter = ((value["Valute"][self.first_valute]["Value"]/
                                value["Valute"][self.second_valute]["Value"])*self.money)
            return round(converter, 2)
