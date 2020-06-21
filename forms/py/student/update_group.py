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


class FormUpdateGroup(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.session = main_window.session
        self.row: int = 0
        self.update_value: str = ''
        self.table = main_window.tableWidget
        self.update_group_window = main_window.update_group_window
        self.update_group_window.setObjectName("MainWindow")
        self.update_group_window.setFixedSize(410, 197)
        self.centralwidget = QtWidgets.QWidget(self.update_group_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 70, 131, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 90, 371, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 120, 191, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 391, 32))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 131, 16))
        self.label_2.setObjectName("label_2")
        self.update_group_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_group_window)
        self.statusbar.setObjectName("statusbar")
        self.update_group_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_group_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_group_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить группу"))
        self.label.setText(_translate("MainWindow", "Номер группы"))
        self.pushButton.setText(_translate("MainWindow", "Сохранить изменения"))
        self.label_2.setText(_translate("MainWindow", "Специальность"))

    def update(self):
        number = self.lineEdit.text()
        specialty: str = self.comboBox.currentText()

        group = Group()
        group.update(self.session, self.update_value, number, specialty)

        self.table.setItem(self.row, 0, QtWidgets.QTableWidgetItem(specialty))
        self.table.setItem(self.row, 1, QtWidgets.QTableWidgetItem(number))

        self.update_group_window.close()

    def update_window(self, dark_theme):
        if dark_theme:
            self.update_group_window.setStyleSheet(window_css)
            self.label.setStyleSheet(label_css)
            self.lineEdit.setStyleSheet(line_edit_css)
            self.pushButton.setStyleSheet(button_css)
            self.comboBox.setStyleSheet(combobox_css)
            self.label_2.setStyleSheet(label_css)
            self.dark_theme = True
        else:
            self.update_group_window.setStyleSheet("")
            self.label.setStyleSheet("")
            self.lineEdit.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.comboBox.setStyleSheet("")
            self.label_2.setStyleSheet("")
            self.dark_theme = False
