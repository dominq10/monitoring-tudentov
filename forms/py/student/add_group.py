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

from db.models import Group
from style.dark_theme import (button_css, combobox_css, label_css,
                              line_edit_css, window_css)


class FormAddGroup(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.session = main_window.session
        self.combo = main_window.combo
        self.table = main_window.tableWidget
        self.add_group_window = main_window.add_group_window
        self.add_group_window.setObjectName("MainWindow")
        self.add_group_window.setFixedSize(410, 197)
        self.centralwidget = QtWidgets.QWidget(self.add_group_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 70, 131, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 90, 371, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(260, 120, 131, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_group)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 391, 32))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 131, 16))
        self.label_2.setObjectName("label_2")
        self.add_group_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_group_window)
        self.statusbar.setObjectName("statusbar")
        self.add_group_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_group_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_group_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить группу"))
        self.label.setText(_translate("MainWindow", "Номер группы"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.label_2.setText(_translate("MainWindow", "Специальность"))

    def add_group(self):
        number = self.lineEdit.text()
        specialty: str = self.comboBox.currentText()
        group = Group()
        group.add(self.session, number, specialty)
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(specialty))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(number))
        self.combo.addItem(number)
        self.comboBox.clear()
        self.lineEdit.clear()
        self.add_group_window.close()

    def update(self, dark_theme):
        if dark_theme:
            self.add_group_window.setStyleSheet(window_css)
            self.label.setStyleSheet(label_css)
            self.lineEdit.setStyleSheet(line_edit_css)
            self.pushButton.setStyleSheet(button_css)
            self.comboBox.setStyleSheet(combobox_css)
            self.label_2.setStyleSheet(label_css)
            self.dark_theme = True
        else:
            self.add_group_window.setStyleSheet("")
            self.label.setStyleSheet("")
            self.lineEdit.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.comboBox.setStyleSheet("")
            self.label_2.setStyleSheet("")
            self.dark_theme = False
