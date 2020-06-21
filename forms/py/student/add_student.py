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

from db.models import Student
from style.dark_theme import (button_css, combobox_css, label_css,
                              line_edit_css, window_css)


class FormAddStudent(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.group_number: str = ''
        self.session = main_window.session
        self.table = main_window.tableWidget
        self.add_student_window = main_window.add_student_window
        self.add_student_window.setObjectName("MainWindow")
        self.add_student_window.setFixedSize(405, 238)
        self.centralwidget = QtWidgets.QWidget(self.add_student_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 58, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 361, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 171, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 100, 361, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 160, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)
        self.add_student_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_student_window)
        self.statusbar.setObjectName("statusbar")
        self.add_student_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_student_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_student_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить студента"))
        self.label.setText(_translate("MainWindow", "ФИО "))
        self.label_2.setText(_translate("MainWindow", "Номер зачетной книжки"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))

    def add(self):
        name = self.lineEdit.text()
        record_book = self.lineEdit_2.text()

        student = Student()
        student.add(self.session, name, record_book, self.group_number)
        number = self.table.rowCount()

        self.table.setRowCount(number + 1)
        self.table.setItem(number, 0, QtWidgets.QTableWidgetItem(name))
        self.table.setItem(number, 1, QtWidgets.QTableWidgetItem(record_book))

        self.lineEdit.clear()
        self.lineEdit_2.clear()

        self.add_student_window.close()

    def update(self, dark_theme):
        if dark_theme:
            self.add_student_window.setStyleSheet(window_css)
            self.label.setStyleSheet(label_css)
            self.lineEdit.setStyleSheet(line_edit_css)
            self.pushButton.setStyleSheet(button_css)
            self.lineEdit_2.setStyleSheet(line_edit_css)
            self.label_2.setStyleSheet(label_css)
            self.dark_theme = True
        else:
            self.add_student_window.setStyleSheet("")
            self.label.setStyleSheet("")
            self.lineEdit.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.lineEdit_2.setStyleSheet("")
            self.label_2.setStyleSheet("")
            self.dark_theme = False
