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
        for i, provider in enumerate(providers):
            self.ui.comboBox.addItem(provider.__name__, userData=provider)

        self.converter = Converter(OfflineExchangeRateProvider())
        self.change_provider(0)
        # Кнопка
        self.ui.pushButton.clicked.connect(self.convert)
        self.ui.comboBox.currentIndexChanged.connect(self.change_provider)

    def init_ui(self):
        # Дизайн верхней части программы
        self.setWindowTitle("Converter valute")
        self.setWindowIcon(QIcon("Icon.png"))

        # Подсказка в lineEdit
        self.ui.lineEdit.setPlaceholderText('Первая валюта')
        self.ui.lineEdit_2.setPlaceholderText('Вторая валюта')
        self.ui.lineEdit_3.setPlaceholderText('Ввод денег')
        self.ui.lineEdit_5.setPlaceholderText('Вывод денег')

        self.ui.lineEdit_3.setValidator(QDoubleValidator(0.0, 1000_000_000.0, 2))

    def convert(self):
        first_currency = self.ui.lineEdit.text().upper()
        second_currency = self.ui.lineEdit_2.text().upper()

        error_message = "Error"
        try:
            money = float(self.ui.lineEdit_3.text().replace(',', '.'))
        except ValueError as error:
            logging.error(f"Exception while converting: {str(error)}")
            self.ui.lineEdit_5.setText(error_message)
            return

        try:
            converted = self.converter.convert(first_currency, second_currency, money)
            self.ui.lineEdit_5.setText(str(converted))
        except ValueError as error:
            logging.error(f"Exception while converting: {str(error)}")
            self.ui.lineEdit_5.setText(error_message)

    def change_provider(self, index):
        provider = self.ui.comboBox.itemData(index)
        self.converter.exchange_rate_provider = provider()
        logging.info(f"Change exchange rate provider to '{provider.__name__}'")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
