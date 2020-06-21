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
from style.dark_theme import button_css, label_css, line_edit_css, window_css


class FormUpdateStudent(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.session = main_window.session
        self.table = main_window.tableWidget

        self.update_value: str = ''
        self.row: int = 0

        self.update_student_window = main_window.update_student_window
        self.update_student_window.setObjectName("MainWindow")
        self.update_student_window.setFixedSize(405, 238)
        self.centralwidget = QtWidgets.QWidget(self.update_student_window)
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
        self.pushButton.clicked.connect(self.update)
        self.update_student_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.update_student_window)
        self.statusbar.setObjectName("statusbar")
        self.update_student_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.update_student_window)
        QtCore.QMetaObject.connectSlotsByName(self.update_student_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Обновить сведения  о студенте"))
        self.label.setText(_translate("MainWindow", "ФИО "))
        self.label_2.setText(_translate("MainWindow", "Номер зачетной книжки"))
        self.pushButton.setText(_translate("MainWindow", "Сохранить"))

    def update(self):
        name = self.lineEdit.text()
        record_book = self.lineEdit_2.text()

        student = Student()
        student.update(self.session, self.update_value, name, record_book)

        self.table.setItem(self.row, 0, QtWidgets.QTableWidgetItem(name))
        self.table.setItem(self.row, 1, QtWidgets.QTableWidgetItem(record_book))

        self.update_student_window.close()

    def update_window(self, dark_theme):
        if dark_theme:
            self.update_student_window.setStyleSheet(window_css)
            self.pushButton.setStyleSheet(button_css)
            self.lineEdit_2.setStyleSheet(line_edit_css)
            self.lineEdit.setStyleSheet(line_edit_css)
            self.label.setStyleSheet(label_css)
            self.label_2.setStyleSheet(label_css)
            self.dark_theme = True
        else:
            self.update_student_window.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.lineEdit_2.setStyleSheet("")
            self.lineEdit.setStyleSheet("")
            self.label.setStyleSheet("")
            self.label_2.setStyleSheet("")
            self.dark_theme = False
