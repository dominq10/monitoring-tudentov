#Copyright 2020 Pavel Tolkachev

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <https://www.gnu.org/licenses/>.
from PyQt5 import QtCore, QtGui, QtWidgets


class form_not_submitted_work(object):
    def __init__(self, MainWindow):
        self.not_submitted_work_window = MainWindow.not_submitted_work_window
        self.not_submitted_work_window.setObjectName("MainWindow")
        self.not_submitted_work_window.resize(737, 536)
        self.centralwidget = QtWidgets.QWidget(self.not_submitted_work_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 211, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 121, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 221, 16))
        self.label_3.setObjectName("label_3")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 90, 691, 391))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Дисциплина", "Задолженность"])
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Операционные системы"))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("Лабораторная работа №1"))
        self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("Операционные системы"))
        self.tableWidget.setItem(1, 1, QtWidgets.QTableWidgetItem("Тест №1"))
        self.tableWidget.resizeColumnsToContents()
        self.not_submitted_work_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.not_submitted_work_window)
        self.statusbar.setObjectName("statusbar")
        self.not_submitted_work_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.not_submitted_work_window)
        QtCore.QMetaObject.connectSlotsByName(self.not_submitted_work_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Не сданные работы"))
        self.label.setText(_translate("MainWindow", "Студент: Иванов Иван Иванович"))
        self.label_2.setText(_translate("MainWindow", "Группа: №453453"))
        self.label_3.setText(_translate("MainWindow", "Номер зачетной книжки: 43543"))

