import sys
import logging

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QDoubleValidator
from ui import Ui_MainWindow
from converter import *
from erp import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()

        providers = [OnlineExchangeRateProvider, OfflineExchangeRateProvider, CombinedExchangeRate]
        for provider in providers:
            self.ui.switch_providers.addItem(provider.__name__, userData=provider)

        self.converter = Converter(OfflineExchangeRateProvider())
        self.change_provider(0)

        self.ui.button_convert.clicked.connect(self.convert)
        self.ui.switch_providers.currentIndexChanged.connect(self.change_provider)

    def init_ui(self):
        self.setWindowTitle("Converter currency")
        self.setWindowIcon(QIcon("Icon.png"))

        # Подсказка в lineEdit
        self.ui.first_currency.setPlaceholderText('Первая валюта')
        self.ui.second_currency.setPlaceholderText('Вторая валюта')
        self.ui.money.setPlaceholderText('Ввод денег')
        self.ui.converted.setPlaceholderText('Вывод денег')

        self.ui.money.setValidator(QDoubleValidator(0.0, 1000_000_000.0, 2))

    def convert(self):
        first_currency = self.ui.first_currency.text().upper()
        second_currency = self.ui.second_currency.text().upper()

        error_message = "Error"
        try:
            money = float(self.ui.money.text().replace(',', '.'))
            converted = self.converter.convert(first_currency, second_currency, money)
            self.ui.converted.setText(str(converted))
        except ValueError as error:
            logging.error(f"Exception while converting: {str(error)}")
            self.ui.converted.setText(error_message)

    def change_provider(self, index):
        provider = self.ui.switch_providers.itemData(index)
        self.converter.exchange_rate_provider = provider()
        logging.info(f"Change exchange rate provider to '{provider.__name__}'")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
