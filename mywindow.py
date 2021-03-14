from PyQt5 import QtWidgets
from PyQt5.Qt import *
from MainWindow import Ui_MainWindow
from client import Client
import sys
import threading
import json


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Меняет размер всех колонок.
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3)
        # self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(1)
        self.machines = []

        row = 0
        for i in self.machines:
            a = QtWidgets.QTableWidgetItem()
            a.setData(Qt.DisplayRole, i)
            self.ui.tableWidget.setItem(row, 0, a)
            a = QtWidgets.QTableWidgetItem()
            a.setData(10, 2)
            self.ui.tableWidget.setItem(row, 1, a)
            a = QtWidgets.QTableWidgetItem()
            a.setData(Qt.DisplayRole, 'free')
            self.ui.tableWidget.setItem(row, 2, a)
            row += 1

    def main_logic(self):
        client = Client()
        self.machines = client.machine_list
        client.set_up('localhost', 5001)
        client.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MyWindow()
    win.show()
    sys.exit(app.exec())
