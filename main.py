import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class Wind(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.bd = sqlite3.connect('data/coffee.db')
        self.show_table()

        self.add_window = AddCoffeeForm()
        self.add_window.add_btn.clicked.connect(self.show_table)
        self.add_btn.clicked.connect(self.add_coffee)

    def show_table(self):
        data = self.bd.cursor().execute('select * from coffe').fetchall()

        self.tableWidget.setColumnCount(len(data[0]))
        self.tableWidget.setRowCount(0)

        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        head = ['ID', 'название сорта', 'степень обжарки',
                'молотый/в зернах', 'описание вкуса', 'цена',
                'объем упаковки']
        self.tableWidget.setHorizontalHeaderLabels(head)
        self.tableWidget.resizeColumnsToContents()

    def add_coffee(self):
        if not self.add_window.isVisible():
            self.add_window.show()


class AddCoffeeForm(QWidget):
    def __init__(self):
        super().__init__()
        self.bd = sqlite3.connect('data/coffee.db')
        uic.loadUi('addEditCoffeeForm.ui', self)
        KINDS = {
            'молотый': 'молотый',
            'в зернах': 'в зернах'
        }
        self.comboBox.addItems(KINDS.keys())


        self.spinBox_3.setMaximum(1000000)
        self.spinBox_2.setMaximum(1000000)

        self.add_btn.clicked.connect(self.add_coffee)

    def add_coffee(self):
        name = self.lineEdit.text()
        roasting = self.lineEdit_2.text()
        kind = self.comboBox.currentText()
        taste = self.lineEdit_3.text()
        price = self.spinBox_3.value()
        volumn = self.spinBox_2.value()

        self.bd.cursor().execute(f"insert into coffe('название сорта', 'степень обжарки', "
                                 f"'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки') "
                                 f"values('{name}', '{roasting}', '{kind}', '{taste}', '{price}', "
                                 f"'{volumn}')")
        self.bd.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Wind()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

