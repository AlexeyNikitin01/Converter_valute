import json
import logging

import requests

from typing import Dict


class IExchangeRateProvider:
    def exchange_rate(self) -> Dict[str, float]:
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
    def _process_response(response_json: dict) -> Dict[str, float]:
        result = {}
        for currency_id, data in response_json["Valute"].items():
            result[currency_id] = data["Value"] / data["Nominal"]
        result["RUB"] = 1.0
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
