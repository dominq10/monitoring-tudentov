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
from forms.py_analytics.student_analytics import FormStudentAnalytics
from style.dark_theme import button_css, combobox_css, label_css, window_css


class FormChoiceGroup(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.choice_analytics_window = main_window.choice_analytics_window
        self.session = main_window.session
        self.choice_group_window = main_window.choice_group_window
        self.choice_group_window.setObjectName("MainWindow")
        self.choice_group_window.setFixedSize(347, 145)

        self.centralwidget = QtWidgets.QWidget(self.choice_group_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 80, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.next)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 80, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_2.clicked.connect(self.previous_page)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 331, 32))
        self.comboBox.setObjectName("comboBox")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 241, 16))
        self.label.setObjectName("label")

        self.choice_group_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.choice_group_window)
        self.statusbar.setObjectName("statusbar")
        self.choice_group_window.setStatusBar(self.statusbar)

        self.student_analytics_window = QtWidgets.QMainWindow()
        self.student_analytics_ui = FormStudentAnalytics(self)

        self.retranslateUi(self.choice_group_window)
        QtCore.QMetaObject.connectSlotsByName(self.choice_group_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Выберите группу студента"))
        self.pushButton.setText(_translate("MainWindow", "Далее"))
        self.pushButton_2.setText(_translate("MainWindow", "Назад"))
        self.label.setText(_translate("MainWindow", "Номер группы студента"))

    def previous_page(self):
        self.choice_group_window.hide()
        self.choice_analytics_window.show()

    def next(self):
        group_number = self.comboBox.currentText()
        student = Student()
        student_name = student.all_name(self.session, group_number)
        self.student_analytics_ui.comboBox.clear()
        self.student_analytics_ui.comboBox.addItems(student_name)
        self.student_analytics_ui.update(self.dark_theme)
        self.student_analytics_ui.group = group_number
        self.student_analytics_window.show()

    def update(self, dark_theme):
        if dark_theme:
            self.choice_group_window.setStyleSheet(window_css)
            self.pushButton.setStyleSheet(window_css)
            self.pushButton_2.setStyleSheet(window_css)
            self.comboBox.setStyleSheet(combobox_css)
            self.label.setStyleSheet(label_css)
            self.dark_theme = True
        else:
            self.choice_group_window.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.comboBox.setStyleSheet("")
            self.label.setStyleSheet("")
            self.dark_theme = False
