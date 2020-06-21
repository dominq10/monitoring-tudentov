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
from PyQt5.QtWidgets import QMessageBox

from parsers.moodle import parser_moodle
from style.dark_theme import button_css, label_css, line_edit_css, window_css


class FormMoodleSettings(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.session = main_window.session

        self.moodle_settings_window = main_window.moodle_settings_window
        self.moodle_settings_window.setObjectName("MainWindow")
        self.moodle_settings_window.setFixedSize(570, 258)
        self.centralwidget = QtWidgets.QWidget(self.moodle_settings_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 221, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 521, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 58, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 100, 271, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 58, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 160, 271, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(151, 190, 291, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.moodle)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 190, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.moodle_settings_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.moodle_settings_window)
        self.statusbar.setObjectName("statusbar")
        self.moodle_settings_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.moodle_settings_window)
        QtCore.QMetaObject.connectSlotsByName(self.moodle_settings_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Синхронизация данных из LMS Moodle"))
        self.label.setText(_translate("MainWindow", "Адрес панели входа"))
        self.label_2.setText(_translate("MainWindow", "Логин"))
        self.label_3.setText(_translate("MainWindow", "Пароль"))
        self.pushButton.setText(_translate("MainWindow", "Синхронизировать данные"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))

    def moodle(self):
        address = self.lineEdit.text()
        login = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        result = parser_moodle(address, login, password, self.session)
        msg = QMessageBox()

        if not result:
            msg.setText("Успешно")
            msg.setInformativeText('Синхронизация с LMS Moodle прошла успешно.')
            msg.setWindowTitle("Успешно")
        else:
            msg.setText("Не удачно")
            msg.setInformativeText('Синхронизация с LMS Moodle прошла не успешно.')
            msg.setWindowTitle("Не удачно")
        msg.exec_()

    def close_window(self):
        self.moodle_settings_window.close()

    def update(self, dark_theme):
        if dark_theme:
            self.moodle_settings_window.setStyleSheet(window_css)
            self.label.setStyleSheet(label_css)
            self.lineEdit.setStyleSheet(line_edit_css)
            self.label_2.setStyleSheet(label_css)
            self.label_3.setStyleSheet(label_css)
            self.lineEdit_2.setStyleSheet(line_edit_css)
            self.lineEdit_3.setStyleSheet(line_edit_css)
            self.pushButton.setStyleSheet(button_css)
            self.pushButton_2.setStyleSheet(button_css)

            self.dark_theme = True
        else:
            self.moodle_settings_window.setStyleSheet("")
            self.label.setStyleSheet("")
            self.lineEdit.setStyleSheet("")
            self.label_2.setStyleSheet("")
            self.label_3.setStyleSheet("")
            self.lineEdit_2.setStyleSheet("")
            self.lineEdit_3.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")

            self.dark_theme = False
