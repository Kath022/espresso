import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class Wind(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.bd = sqlite3.connect('coffee.db')
        self.show_table()

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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Wind()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

