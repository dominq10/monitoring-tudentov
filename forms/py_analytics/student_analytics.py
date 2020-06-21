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
from forms.py_analytics.analytics_table_student import \
    FormAnalyticsTableStudent
from style.dark_theme import button_css, combobox_css, label_css, window_css
from transform.items import set_items_to_table


class FormStudentAnalytics(object):
    def __init__(self, main_window):
        self.group = None
        self.dark_theme = False
        self.session = main_window.session
        self.choice_group_window = main_window.choice_group_window
        self.student_analytics_window = main_window.student_analytics_window
        self.student_analytics_window.setObjectName("MainWindow")
        self.student_analytics_window.setFixedSize(380, 369)
        self.centralwidget = QtWidgets.QWidget(self.student_analytics_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 221, 16))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 40, 361, 32))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 100, 361, 32))
        self.comboBox_2.setObjectName("comboBox_2")
        ls_2 = ['Зимняя', 'Летняя', 'Все сессии']
        self.comboBox_2.addItems(ls_2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 58, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 58, 16))
        self.label_3.setObjectName("label_3")

        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(10, 160, 361, 32))
        self.comboBox_3.setObjectName("comboBox_3")

        ls_3 = ['За последний год', 'За последние 2 года', 'За последние 3 года', 'За все время']
        self.comboBox_3.addItems(ls_3)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 200, 161, 16))
        self.label_4.setObjectName("label_4")

        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(10, 220, 361, 32))
        self.comboBox_4.setObjectName("comboBox_4")

        ls_4 = ['Средняя оценка по итогам сессии', 'Средняя оценка за работы в семестре',
                'Максимальная оценка по итогам сессии', 'Максимальная оценка по итогам работы в семестре',
                'Минимальная оценка по итогам сессии', 'Минимальная оценка по итогам работы в семестре',
                'Количество сданных работ в семестре']
        self.comboBox_4.addItems(ls_4)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 260, 181, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.analysis)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 290, 181, 32))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_2.clicked.connect(self.previous_page)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 290, 111, 32))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_3.clicked.connect(self.close_window)
        self.student_analytics_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.student_analytics_window)
        self.statusbar.setObjectName("statusbar")
        self.student_analytics_window.setStatusBar(self.statusbar)

        self.analytics_table_student_window = QtWidgets.QMainWindow()
        self.analytics_table_student_ui = FormAnalyticsTableStudent(self)

        self.retranslateUi(self.student_analytics_window)
        QtCore.QMetaObject.connectSlotsByName(self.student_analytics_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Анализ успеваемости студента"))
        self.label.setText(_translate("MainWindow", "ФИО студента"))
        self.label_2.setText(_translate("MainWindow", "Сессия"))
        self.label_3.setText(_translate("MainWindow", "Период"))
        self.label_4.setText(_translate("MainWindow", "Тип анализа"))
        self.pushButton.setText(_translate("MainWindow", "Выполнить анализ"))
        self.pushButton_2.setText(_translate("MainWindow", "Назад"))
        self.pushButton_3.setText(_translate("MainWindow", "Закрыть"))

    def close_window(self):
        self.student_analytics_window.close()

    def previous_page(self):
        self.student_analytics_window.hide()
        self.choice_group_window.show()

    def analysis(self):
        student = self.comboBox.currentText()
        type_analysis = self.comboBox_4.currentText()
        period = self.comboBox_3.currentText()
        session = self.comboBox_2.currentText()

        self.analytics_table_student_ui.label_2.setText(student)
        self.analytics_table_student_ui.label_4.setText(type_analysis)
        self.analytics_table_student_ui.label_6.setText(period)
        self.analytics_table_student_ui.label_8.setText(session)

        control = Control()
        grade = Grade()
        if type_analysis == 'Средняя оценка по итогам сессии':
            result: np.ndarray = control.analysis_student_average_rating(self.session, student, session, period)
        elif type_analysis == 'Максимальная оценка по итогам сессии':
            result: np.ndarray = control.analysis_student_rating(self.session, student, session, period, max=True)
        elif type_analysis == 'Минимальная оценка по итогам сессии':
            result: np.ndarray = control.analysis_student_rating(self.session, student, session, period, max=False)
        elif type_analysis == 'Средняя оценка за работы в семестре':
            result: np.ndarray = grade.analysis_student_average_rating(self.session, student, session, period)
        elif type_analysis == 'Максимальная оценка по итогам работы в семестре':
            result: np.ndarray = grade.analysis_student_rating_semester(self.session, student, session, period, max=True)
        elif type_analysis == 'Минимальная оценка по итогам работы в семестре':
            result: np.ndarray = grade.analysis_student_rating_semester(self.session, student, session, period, max=False)
        elif type_analysis == 'Количество сданных работ в семестре':
            result: np.ndarray = grade.analysis_student_number_works(self.session, student, session, period)

        self.analytics_table_student_ui.result = result
        if type_analysis == 'Количество сданных работ в семестре':
            self.analytics_table_student_ui.tableWidget.setColumnCount(3)
        else:
            self.analytics_table_student_ui.tableWidget.setColumnCount(2)

        if type_analysis == 'Средняя оценка по итогам сессии':
            table_header = ['Учебный год', 'Средняя оценка']
        elif type_analysis == 'Средняя оценка за работы в семестре':
            table_header = ['Учебный год', 'Средняя оценка']
        elif type_analysis == 'Максимальная оценка по итогам сессии':
            table_header = ['Учебный год', 'Максимальная оценка']
        elif type_analysis == 'Минимальная оценка по итогам сессии':
            table_header = ['Учебный год', 'Минимальная оценка']
        elif type_analysis == 'Максимальная оценка по итогам работы в семестре':
            table_header = ['Учебный год', 'Максимальная оценка']
        elif type_analysis == 'Минимальная оценка по итогам работы в семестре':
            table_header = ['Учебный год', 'Минимальная оценка']
        elif type_analysis == 'Количество сданных работ в семестре':
            table_header = ['Учебный год', 'Количество сданных работ', 'Количество работ']

        if type_analysis == 'Средняя оценка по итогам сессии':
            self.analytics_table_student_ui.student_diagram_ui.pushButton_3.setText("Отобразить диаграмму в пропорциях")
        else:
            self.analytics_table_student_ui.student_diagram_ui.pushButton_3.setText("Отобразить диаграмму в круговом виде")
            self.analytics_table_student_ui.student_diagram_ui.pushButton_3.hide()
            self.analytics_table_student_ui.student_diagram_ui.data = result

        self.analytics_table_student_ui.tableWidget.setHorizontalHeaderLabels(table_header)
        self.analytics_table_student_ui.tableWidget = set_items_to_table(self.analytics_table_student_ui.tableWidget,
                                                                         result, DARK_THEME=self.dark_theme)
        self.analytics_table_student_ui.update(self.dark_theme)
        self.analytics_table_student_ui.tableWidget.resizeColumnsToContents()

        self.analytics_table_student_ui.student = student
        self.analytics_table_student_ui.type_analysis = type_analysis
        self.analytics_table_student_ui.period = period
        self.analytics_table_student_ui.stud_session = session
        self.analytics_table_student_ui.table_header = table_header
        self.analytics_table_student_ui.group = self.group
        self.analytics_table_student_ui.result = result

        self.student_analytics_window.hide()

        self.analytics_table_student_window.show()

    def update(self, dark_theme):
        if dark_theme:
            self.student_analytics_window.setStyleSheet(window_css)
            self.label.setStyleSheet(label_css)
            self.comboBox.setStyleSheet(combobox_css)
            self.comboBox_2.setStyleSheet(combobox_css)
            self.pushButton_3.setStyleSheet(button_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.pushButton.setStyleSheet(button_css)
            self.label_4.setStyleSheet(label_css)
            self.label_3.setStyleSheet(label_css)
            self.label_2.setStyleSheet(label_css)
            self.comboBox_3.setStyleSheet(combobox_css)
            self.comboBox_4.setStyleSheet(combobox_css)

            self.dark_theme = True
        else:
            self.student_analytics_window.setStyleSheet("")
            self.label.setStyleSheet("")
            self.comboBox.setStyleSheet("")
            self.comboBox_2.setStyleSheet("")
            self.pushButton_3.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.label_4.setStyleSheet("")
            self.label_3.setStyleSheet("")
            self.label_2.setStyleSheet("")
            self.comboBox_3.setStyleSheet("")
            self.comboBox_4.setStyleSheet("")
            self.dark_theme = False
