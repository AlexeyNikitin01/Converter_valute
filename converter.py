from erp import ExchangeRateProvider, IExchangeRateProvider


class Converter:
    """Currency converter"""
    def __init__(self, exchange_rate_provider: IExchangeRateProvider = ExchangeRateProvider()):
        self.exchange_rate_provider = exchange_rate_provider

    def convert(self, first_currency: str, second_currency: str, money: float) -> float:
        exchange_rate = self.exchange_rate_provider.exchange_rate()

        if first_currency not in exchange_rate:
            raise ValueError(f"Unexpected currency identifier: {first_currency}")

        if second_currency not in exchange_rate:
            raise ValueError(f"Unexpected currency identifier: {second_currency}")

        first_rate = exchange_rate[first_currency]
        second_rate = exchange_rate[second_currency]

        return round(first_rate * money / second_rate, 2)
