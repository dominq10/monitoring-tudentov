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
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from db.models import Control, Grade
from forms.py_analytics.analytics_table_discipline_group import \
    FormAnalyticsTableDisciplineGroup
from style.dark_theme import button_css, combobox_css, label_css, window_css
from transform.items import set_items_to_table


class FormChoiceDisciplineGroup(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.discipline = ""
        self.session = main_window.session
        self.choice_discipline_group_or_student_window = main_window.choice_discipline_group_or_student_window
        self.choice_discipline_group_window = main_window.choice_discipline_group_window
        self.choice_discipline_group_window.setObjectName("MainWindow")
        self.choice_discipline_group_window.setFixedSize(417, 130)
        self.centralwidget = QtWidgets.QWidget(self.choice_discipline_group_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 70, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.previous_page)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(170, 70, 121, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.analysis)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 111, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 30, 391, 32))
        self.comboBox_2.setObjectName("comboBox_2")
        ls = ['Средняя оценка по итогам сессии', 'Средняя оценка за работы в семестре',
                'Максимальная оценка по итогам сессии', 'Максимальная оценка по итогам работы в семестре',
                'Минимальная оценка по итогам сессии', 'Минимальная оценка по итогам работы в семестре']
        self.comboBox_2.clear()
        self.comboBox_2.addItems(ls)
        self.choice_discipline_group_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.choice_discipline_group_window)
        self.statusbar.setObjectName("statusbar")
        self.choice_discipline_group_window.setStatusBar(self.statusbar)

        self.analytics_table_discipline_group_window = QtWidgets.QMainWindow()
        self.analytics_table_discipline_group_ui = FormAnalyticsTableDisciplineGroup(self)

        self.retranslateUi(self.choice_discipline_group_window)
        QtCore.QMetaObject.connectSlotsByName(self.choice_discipline_group_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Аналитика"))
        self.pushButton_2.setText(_translate("MainWindow", "Назад"))
        self.pushButton_3.setText(_translate("MainWindow", "Далее"))
        self.label_2.setText(_translate("MainWindow", "Тип анализа"))

    def previous_page(self):
        self.choice_discipline_group_window.hide()
        self.choice_discipline_group_or_student_window.show()

    def analysis(self):
        type_analysis = self.comboBox_2.currentText()

        grade = Grade()
        control = Control()
        if type_analysis == 'Средняя оценка за работы в семестре':
            result: np.ndarray = grade.analysis_group_average_rating_discipline(self.session, self.discipline)
        elif type_analysis == 'Максимальная оценка по итогам работы в семестре':
            result: np.ndarray = grade.analysis_group_rating_semester_discipline(self.session, self.discipline, max=True)
        elif type_analysis == 'Минимальная оценка по итогам работы в семестре':
            result: np.ndarray = grade.analysis_group_rating_semester_discipline(self.session, self.discipline, max=False)
        elif type_analysis == 'Средняя оценка по итогам сессии':
            result: np.ndarray = control.analysis_group_average_rating_discipline(self.session, self.discipline)
        elif type_analysis == 'Максимальная оценка по итогам сессии':
            result: np.ndarray = control.analysis_group_maxmin_discipline(self.session, self.discipline, max=True)
        else:
            result: np.ndarray = control.analysis_group_maxmin_discipline(self.session, self.discipline,max=False)

        self.analytics_table_discipline_group_ui.tableWidget.setColumnCount(2)

        if type_analysis == 'Средняя оценка за работы в семестре':
            table_header = ['Учебная группа', 'Средняя оценка']
        elif type_analysis == 'Максимальная оценка по итогам работы в семестре':
            table_header = ['Учебная группа', 'Максимальная оценка']
        elif type_analysis == 'Минимальная оценка по итогам работы в семестре':
            table_header = ['Учебная группа', 'Минимальная оценка']
        elif type_analysis == 'Средняя оценка по итогам сессии':
            table_header = ['Учебная группа', 'Средняя оценка']
        elif type_analysis == 'Максимальная оценка по итогам сессии':
            table_header = ['Учебная группа', 'Максимальная оценка']
        else:
            table_header = ['Учебная группа', 'Минимальная оценка']

        self.analytics_table_discipline_group_ui.tableWidget.setHorizontalHeaderLabels(table_header)
        self.analytics_table_discipline_group_ui.tableWidget = set_items_to_table(
            self.analytics_table_discipline_group_ui.tableWidget,
            result, DARK_THEME=self.dark_theme)
        self.analytics_table_discipline_group_ui.update(self.dark_theme)
        self.analytics_table_discipline_group_ui.tableWidget.resizeColumnsToContents()

        self.analytics_table_discipline_group_ui.label_6.setText(self.discipline)
        self.analytics_table_discipline_group_ui.label_2.setText(type_analysis)
        self.analytics_table_discipline_group_ui.result = result
        self.analytics_table_discipline_group_ui.discipline = self.discipline
        self.analytics_table_discipline_group_ui.table_header = table_header
        self.analytics_table_discipline_group_ui.type_analysis = type_analysis

        self.choice_discipline_group_window.hide()
        self.analytics_table_discipline_group_window.show()

    def update(self, dark_theme):
        if dark_theme:
            self.choice_discipline_group_window.setStyleSheet(window_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.pushButton_3.setStyleSheet(button_css)
            self.label_2.setStyleSheet(label_css)
            self.comboBox_2.setStyleSheet(combobox_css)
            self.dark_theme = True
        else:
            self.choice_discipline_group_window.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.pushButton_3.setStyleSheet("")
            self.label_2.setStyleSheet("")
            self.comboBox_2.setStyleSheet("")
            self.dark_theme = False
