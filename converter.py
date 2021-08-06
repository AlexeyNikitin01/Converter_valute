import logging

from erp import IExchangeRateProvider


class Converter:
    """Currency converter"""
    def __init__(self, exchange_rate_provider: IExchangeRateProvider):
        self.exchange_rate_provider = exchange_rate_provider

    def convert(self, first_currency: str, second_currency: str, money: float) -> float:
        logging.info(f"Converting {money} {first_currency} to {second_currency}")

        exchange_rate = self.exchange_rate_provider.exchange_rate()

        if first_currency not in exchange_rate:
            raise ValueError(f"Unexpected currency identifier: {first_currency}")

        if second_currency not in exchange_rate:
            raise ValueError(f"Unexpected currency identifier: {second_currency}")

        first_rate = exchange_rate[first_currency]
        second_rate = exchange_rate[second_currency]

        return round(first_rate * money / second_rate, 2)
