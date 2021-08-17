import json
import logging
import datetime

import requests

from dateutil import parser
from typing import Dict


class IExchangeRateProvider:
    def exchange_rate(self):
        raise NotImplementedError()


class OnlineExchangeRateProvider(IExchangeRateProvider):
    URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

    def exchange_rate(self) -> dict:
        return self._exchange_rate()

    def _exchange_rate(self):
        exchange_rate = None
        try:
            response = requests.get(self.URL)
            response.raise_for_status()
            exchange_rate = self._process_response(response.json())
        except requests.HTTPError as http_error:
            logging.error(f"HTTPError: {http_error}")
        except Exception as e:
            logging.error(f"Exception: {str(e)}")
        return exchange_rate

    @staticmethod
    def _process_response(response_json: dict):
        result = {}
        for currency_id, data in response_json["Valute"].items():
            result["Valute"][currency_id] = data["Value"] / data["Nominal"]
        result["Valute"]["RUB"] = 1.0
        result["Date"] = response_json["Date"]
        return result


class OfflineExchangeRateProvider(IExchangeRateProvider):
    PATH_TO_FILE = 'outfile.json'

    def __init__(self):
        self._exchange_rate = None
        with open("outfile.json", "r") as file:
            self._exchange_rate = json.load(file)

    def exchange_rate(self):
        return self._exchange_rate


class CombinedExchangeRate(IExchangeRateProvider):
    def __init__(self):
        self.offline_provider = OfflineExchangeRateProvider()
        self.online_provider = OnlineExchangeRateProvider()

    def exchange_rate(self):
        return self.online_provider.exchange_rate() or self.offline_provider.exchange_rate()


class CacheExchangeRateProvider(IExchangeRateProvider):
    def __init__(self):
        self.offline_provider = OfflineExchangeRateProvider()
        self.online_provider = OnlineExchangeRateProvider()

    def is_cache_valid(self):
        date_now = datetime.datetime.today().timestamp()
        date_offline_provider = parser.parse(self.offline_provider.exchange_rate()["Date"]).timestamp()
        difference_today_and_offline = date_now - date_offline_provider
        return difference_today_and_offline < 3600 * 24

    def update_cache(self):
        update_exchange_rate = self.online_provider.exchange_rate()
        with open("outfile.json", "w") as file:
            json.dump(update_exchange_rate, file, indent=2)

    def exchange_rate(self):
        if self.is_cache_valid():
            return self.offline_provider.exchange_rate()
        self.update_cache()
        return self.offline_provider.exchange_rate()
