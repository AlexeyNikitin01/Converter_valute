from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from ui import Ui_MainWindow
import sys
from conve import *
 
class Converter_pyqt(QtWidgets.QMainWindow):
    def __init__(self):
        super(Converter_pyqt, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        #Кнопка
        self.ui.pushButton.clicked.connect(self.convert)

    def init_ui(self):
        #Вехняя чатсть проги
        self.setWindowTitle("Converter currency")
        self.setWindowIcon(QIcon("Icon.png"))

        #Подсказка в lineEdit
        self.ui.lineEdit.setPlaceholderText('Первая валюта')
        self.ui.lineEdit_2.setPlaceholderText('Вторая валюта')
        self.ui.lineEdit_3.setPlaceholderText('Ввод денег')
        self.ui.lineEdit_5.setPlaceholderText('Вывод денег')

    def convert(self):
        one_curr =  self.ui.lineEdit.text().upper()
        two_curr = self.ui.lineEdit_2.text().upper()
        money = self.ui.lineEdit_3.text()
        exem = Converter(one_curr, two_curr, money)
        out_money = exem.converter(one_curr, two_curr, money)
        #Вывод конвертированной валюты
        self.ui.lineEdit_5.setText(str(out_money))

app = QtWidgets.QApplication([])
application = Converter_pyqt()
application.show()
sys.exit(app.exec())