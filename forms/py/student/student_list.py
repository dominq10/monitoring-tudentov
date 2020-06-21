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
import csv

from PyQt5 import QtCore, QtWidgets
from forms.py.moodle_settings import FormMoodleSettings
from db.models import Student
from forms.py.student.add_student import FormAddStudent
from forms.py.student.update_student import FormUpdateStudent
from style.dark_theme import (button_css, label_css, table_css,
                              table_header_css, window_css)


class FormStudentList(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.group_number: str = ''
        self.session = main_window.session
        self.student_window = main_window.student_list_window
        self.student_window.setObjectName("MainWindow")
        self.student_window.setFixedSize(676, 530)
        self.centralwidget = QtWidgets.QWidget(self.student_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 241, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(160, 360, 141, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.update)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(530, 460, 141, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 360, 141, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.add)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(20, 440, 641, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(300, 360, 141, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.import_from_csv)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(300, 390, 141, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.import_from_moodle)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 631, 321))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["ФИО", "Номер зачетной книжки"])
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.resizeColumnsToContents()
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(160, 390, 141, 32))
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_6.clicked.connect(self.delete)
        self.student_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.student_window)
        self.statusbar.setObjectName("statusbar")
        self.student_window.setStatusBar(self.statusbar)

        self.add_student_window = QtWidgets.QMainWindow()
        self.add_student_ui = FormAddStudent(self)

        self.update_student_window = QtWidgets.QMainWindow()
        self.update_student_ui = FormUpdateStudent(self)

        self.retranslateUi(self.student_window)
        QtCore.QMetaObject.connectSlotsByName(self.student_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Список группы"))
        self.label.setText(_translate("MainWindow", "Список группы №423342"))
        self.pushButton.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_3.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_4.setText(_translate("MainWindow", "Импорт из .csv"))
        self.pushButton_5.setText(_translate("MainWindow", "Импорт из Moodle"))
        self.pushButton_6.setText(_translate("MainWindow", "Удалить"))

    def add(self):
        self.add_student_ui.group_number = self.group_number
        self.add_student_ui.update(self.dark_theme)
        self.add_student_window.show()

    def update(self):
        items = self.tableWidget.selectedItems()

        for i in items:
            row = self.tableWidget.row(i)

            name = self.tableWidget.item(row, 0).text()
            record_book = self.tableWidget.item(row, 1).text()

            self.update_student_ui.lineEdit.setText(name)
            self.update_student_ui.lineEdit_2.setText(record_book)

            self.update_student_ui.update_value = record_book
            self.update_student_ui.row = row

            self.update_student_ui.update_window(self.dark_theme)
            self.update_student_window.show()
            break

    def delete(self):
        items = self.tableWidget.selectedItems()
        for i in items:
            row = self.tableWidget.row(i)
            record_book = self.tableWidget.item(row, 1).text()

            student = Student()
            student.delete(self.session, record_book)

            self.tableWidget.removeRow(row)

    def import_from_csv(self):
       # msg = QMessageBox()
       # msg.setIcon(QMessageBox.Critical)
       # try:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self.student_window, "Open Image", ".",
                                                        "Image Files (*.csv)")

        with open(path, "r") as f_obj:
            reader = csv.reader(f_obj)
            for row in reader:
                name = row[0]
                record_book = int(row[1])

                student = Student()
                student.add(self.session, name, record_book)
                number = self.tableWidget.rowCount()

                self.tableWidget.setRowCount(number + 1)
                self.tableWidget.setItem(number, 0, QtWidgets.QTableWidgetItem(name))
                self.tableWidget.setItem(number, 1, QtWidgets.QTableWidgetItem(str(record_book)))
                self.tableWidget.resizeColumnsToContents()






    def import_from_moodle(self):
        self.moodle_settings_window.show()

    def close_window(self):
        self.tableWidget.setRowCount(0)
        self.student_window.close()

    def update_window(self, dark_theme):
        if dark_theme:
            self.student_window.setStyleSheet(window_css)
            self.label.setStyleSheet(label_css)
            self.pushButton.setStyleSheet(button_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.pushButton_3.setStyleSheet(button_css)
            self.pushButton_4.setStyleSheet(button_css)
            self.pushButton_5.setStyleSheet(button_css)
            self.tableWidget.setStyleSheet(table_css)
            self.tableWidget.horizontalHeader().setStyleSheet(table_header_css)
            self.tableWidget.verticalHeader().setStyleSheet(table_header_css)
            self.pushButton_6.setStyleSheet(button_css)
            self.dark_theme = True
        else:
            self.student_window.setStyleSheet("")
            self.label.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.pushButton_3.setStyleSheet("")
            self.pushButton_4.setStyleSheet("")
            self.pushButton_5.setStyleSheet("")
            self.tableWidget.setStyleSheet("")
            self.tableWidget.horizontalHeader().setStyleSheet("")
            self.tableWidget.verticalHeader().setStyleSheet("")
            self.pushButton_6.setStyleSheet("")
            self.dark_theme = False
