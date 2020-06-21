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

from db.models import Group, Specialty
from forms.py.student.add_group import FormAddGroup
from forms.py.student.update_group import FormUpdateGroup
from style.dark_theme import (button_css, combobox_css, label_css, table_css,
                              table_header_css, window_css)


class FormGroupWindow(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.combo = main_window.comboBox
        self.session = main_window.session
        self.group_window = main_window.group_window
        self.group_window.setObjectName("MainWindow")
        self.group_window.setFixedSize(661, 498)
        self.centralwidget = QtWidgets.QWidget(self.group_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(170, 360, 151, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_update_group)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 430, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 631, 341))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["Специальность", "Номер группы"])
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 360, 151, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_add_group)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(170, 390, 151, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.delete)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(30, 420, 621, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.group_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.group_window)
        self.statusbar.setObjectName("statusbar")
        self.group_window.setStatusBar(self.statusbar)

        self.add_group_window = QtWidgets.QMainWindow()
        self.add_group_ui = FormAddGroup(self)

        self.update_group_window = QtWidgets.QMainWindow()
        self.update_group_ui = FormUpdateGroup(self)

        self.retranslateUi(self.group_window)
        QtCore.QMetaObject.connectSlotsByName(self.group_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Группы"))
        self.pushButton.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_3.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить"))

    def close_window(self):
        self.group_window.close()

    def show_add_group(self):
        specialty = Specialty()
        ls_name = specialty.show_name(self.session)
        self.add_group_ui.comboBox.addItems(ls_name)
        self.add_group_ui.update(self.dark_theme)
        self.add_group_window.show()

    def show_update_group(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            row = self.tableWidget.row(i)

            specialty = self.tableWidget.item(row, 0).text()
            number = self.tableWidget.item(row, 1).text()
            self.update_group_ui.lineEdit.setText(number)

            s = Specialty()
            ls_name = s.show_name(self.session)
            self.update_group_ui.comboBox.addItems(ls_name)
            current_index = ls_name.index(specialty)
            self.update_group_ui.comboBox.setCurrentIndex(current_index)

            self.update_group_ui.update_value = number
            self.update_group_ui.row = row

            self.update_group_ui.update_window(self.dark_theme)
            self.update_group_window.show()
            break

    def delete(self):
        items = self.tableWidget.selectedItems()
        for i in items:
            row = self.tableWidget.row(i)
            number = self.tableWidget.item(row, 1).text()

            group = Group()
            group.delete(self.session, number)

            self.tableWidget.removeRow(row)
            self.combo.clear()
            ls_name = group.show_name(self.session)
            self.combo.addItems(ls_name)

    def update(self, dark_theme):
        if dark_theme:
            self.group_window.setStyleSheet(window_css)
            self.pushButton.setStyleSheet(button_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.tableWidget.setStyleSheet(table_css)
            self.tableWidget.horizontalHeader().setStyleSheet(table_header_css)
            self.tableWidget.verticalHeader().setStyleSheet(table_header_css)
            self.pushButton_3.setStyleSheet(button_css)
            self.pushButton_4.setStyleSheet(button_css)
            self.dark_theme = True
        else:
            self.group_window.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.tableWidget.setStyleSheet("")
            self.tableWidget.horizontalHeader().setStyleSheet("")
            self.tableWidget.verticalHeader().setStyleSheet("")
            self.pushButton_3.setStyleSheet("")
            self.pushButton_4.setStyleSheet("")
            self.dark_theme = False
