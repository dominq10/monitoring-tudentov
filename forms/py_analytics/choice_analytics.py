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

from db.models import Discipline, Group
from forms.py_analytics.choice_discipline import FormChoiceDiscipline
from forms.py_analytics.choice_group import FormChoiceGroup
from forms.py_analytics.group_analytics import FormGroupAnalytics
from style.dark_theme import button_css, combobox_css, label_css, window_css


class FormChoiceAnalyticsWindow(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.session = main_window.session
        self.choice_analytics_window = main_window.choice_analytics_window
        self.choice_analytics_window.setObjectName("MainWindow")
        self.choice_analytics_window.setFixedSize(349, 172)
        self.centralwidget = QtWidgets.QWidget(self.choice_analytics_window)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 40, 311, 32))
        self.comboBox.setObjectName("comboBox")
        ls = ["Группа", 'Дисциплина', "Студент"]
        self.comboBox.addItems(ls)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 171, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 100, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.choice_analytics)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 100, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.choice_analytics_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.choice_analytics_window)
        self.statusbar.setObjectName("statusbar")
        self.choice_analytics_window.setStatusBar(self.statusbar)

        self.choice_discipline_window = QtWidgets.QMainWindow()
        self.choice_discipline_ui = FormChoiceDiscipline(self)

        self.choice_group_window = QtWidgets.QMainWindow()
        self.choice_group_ui = FormChoiceGroup(self)

        self.group_analytics_window = QtWidgets.QMainWindow()
        self.group_analytics_ui = FormGroupAnalytics(self)

        self.retranslateUi(self.choice_analytics_window)
        QtCore.QMetaObject.connectSlotsByName(self.choice_analytics_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Выберите объект анализа"))
        self.label.setText(_translate("MainWindow", "Объект анализа"))
        self.pushButton.setText(_translate("MainWindow", "Далее"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))

    def choice_analytics(self):
        choice = self.comboBox.currentText()

        if choice == 'Студент':
            self.show_student_analytics_window()
        elif choice == 'Дисциплина':
            self.show_analytics_window()
        else:
            self.show_group_analytics_window()

    # Аналитика по дисциплинам
    def show_analytics_window(self):
        group = Group()
        ls_name = group.show_name(self.session)

        discipline = Discipline
        d_name = discipline.show_name(self.session)
        self.choice_discipline_ui.comboBox.clear()
        self.choice_discipline_ui.comboBox.addItems(d_name)

        self.choice_discipline_window.show()
        self.choice_discipline_ui.update(self.dark_theme)
        self.choice_analytics_window.hide()

    # Аналитика по группам
    def show_group_analytics_window(self):
        group = Group()
        ls_name = group.show_name(self.session)
        self.group_analytics_ui.comboBox.clear()
        self.group_analytics_ui.comboBox.addItems(ls_name)

        self.choice_analytics_window.hide()
        self.group_analytics_ui.update(self.dark_theme)
        self.group_analytics_window.show()

    # Аналитика по студенту
    def show_student_analytics_window(self):
        group = Group()
        ls_name = group.show_name(self.session)
        self.choice_group_ui.comboBox.clear()
        self.choice_group_ui.comboBox.addItems(ls_name)
        self.choice_analytics_window.hide()
        self.choice_group_ui.update(self.dark_theme)
        self.choice_group_window.show()

    def close_window(self):
        self.choice_analytics_window.close()

    def update(self, dark_theme):
        if dark_theme:
            self.choice_analytics_window.setStyleSheet(window_css)
            self.comboBox.setStyleSheet(combobox_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.pushButton.setStyleSheet(button_css)
            self.label.setStyleSheet(label_css)
            self.dark_theme = True
        else:
            self.choice_analytics_window.setStyleSheet("")
            self.comboBox.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.label.setStyleSheet("")
            self.dark_theme = False
