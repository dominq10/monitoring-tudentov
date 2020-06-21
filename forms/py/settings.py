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

from forms.py.moodle_settings import FormMoodleSettings
from style.dark_theme import button_css, radio_css, window_css


class FormSettings(object):
    def __init__(self, main_window):
        self.session = main_window.session
        self.dark_theme = False
        self.main_window = main_window
        self.settings_window = main_window.settings_window
        self.settings_window.setObjectName("MainWindow")
        self.settings_window.setFixedSize(301, 184)
        self.centralwidget = QtWidgets.QWidget(self.settings_window)
        self.centralwidget.setObjectName("centralwidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(10, 10, 251, 20))
        self.radioButton.setObjectName("radioButton")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 120, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_window)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 40, 281, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 60, 281, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show_moodle)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 100, 281, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.settings_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.settings_window)
        self.statusbar.setObjectName("statusbar")
        self.settings_window.setStatusBar(self.statusbar)

        self.moodle_settings_window = QtWidgets.QMainWindow()
        self.moodle_settings_ui = FormMoodleSettings(self)

        self.retranslateUi(self.settings_window)
        QtCore.QMetaObject.connectSlotsByName(self.settings_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Параметры"))
        self.radioButton.setText(_translate("MainWindow", "Темная тема интерфейса"))
        self.pushButton.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_2.setText(_translate("MainWindow", "Импорт данных из LMS Moodle"))

    def close_window(self):
        if self.radioButton.isChecked():
            dark = True
        else:
            dark = False
        self.main_window.update(dark)
        self.settings_window.close()
        self.main_window.show()

    def show_moodle(self):
        self.moodle_settings_ui.update(self.dark_theme)
        self.moodle_settings_window.show()

    def update(self, dark_theme):
        if dark_theme is True:
            self.settings_window.setStyleSheet(window_css)
            self.pushButton.setStyleSheet(button_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.radioButton.setStyleSheet(radio_css)

            self.dark_theme = True
        else:
            self.settings_window.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.radioButton.setStyleSheet("")

            self.dark_theme = False
