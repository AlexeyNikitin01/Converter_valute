import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from ui import Ui_MainWindow
from converter import *
 

class Converter_pyqt(QtWidgets.QMainWindow):
    def __init__(self):
        super(Converter_pyqt, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        #Кнопка
        self.ui.pushButton.clicked.connect(self.convert)

    def init_ui(self):
        #Дизайн верзней части программы
        self.setWindowTitle("Converter valute")
        self.setWindowIcon(QIcon("Icon.png"))

        #Подсказка в lineEdit
        self.ui.lineEdit.setPlaceholderText('Первая валюта')
        self.ui.lineEdit_2.setPlaceholderText('Вторая валюта')
        self.ui.lineEdit_3.setPlaceholderText('Ввод денег')
        self.ui.lineEdit_5.setPlaceholderText('Вывод денег')

    def convert(self):
        first_valute =  self.ui.lineEdit.text().upper()
        second_valute = self.ui.lineEdit_2.text().upper()
        money = self.ui.lineEdit_3.text()
        exem = Converter(first_valute, second_valute, money)
        out_money = exem.convert(first_valute, second_valute, money)
        #Вывод конвертированной валюты
        self.ui.lineEdit_5.setText(str(out_money))

app = QtWidgets.QApplication([])
application = Converter_pyqt()
application.show()
sys.exit(app.exec())