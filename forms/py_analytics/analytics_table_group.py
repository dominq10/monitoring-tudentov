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
from PyQt5.QtChart import QBarSeries, QBarSet, QChart, QChartView, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from db.models import Control
from forms.py_analytics.group_diagram import FormGroupDiagram
from report import Report, list_of_report_name, list_of_report_object
from style.dark_theme import (button_css, label_css, table_css,
                              table_header_css, window_css)


class FormAnalyticsTableGroup(object):
    def __init__(self, main_window):
        self.group = None
        self.type_analysis = None
        self.period = None
        self.stud_session = None
        self.table_header = None
        self.result: str = ''

        self.dark_theme = False
        self.session = main_window.session

        self.group_analytics_window = main_window.group_analytics_window
        self.analytics_table_group_window = main_window.analytics_table_group_window
        self.analytics_table_group_window.setObjectName("MainWindow")
        self.analytics_table_group_window.setFixedSize(800, 437)
        self.centralwidget = QtWidgets.QWidget(self.analytics_table_group_window)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 60, 751, 301))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(125, 10, 291, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 91, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(110, 30, 291, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 370, 191, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_diagram)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(550, 370, 111, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.previous_page)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(660, 370, 112, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.close_window)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(450, 10, 58, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(510, 10, 150, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(450, 30, 58, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(510, 30, 58, 16))
        self.label_8.setObjectName("label_8")
        self.analytics_table_group_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.analytics_table_group_window)
        self.statusbar.setObjectName("statusbar")
        self.analytics_table_group_window.setStatusBar(self.statusbar)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(210, 370, 181, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.report)

        self.group_diagram_window = QtWidgets.QMainWindow()
        self.group_diagram_ui = FormGroupDiagram(self)

        self.retranslateUi(self.analytics_table_group_window)
        QtCore.QMetaObject.connectSlotsByName(self.analytics_table_group_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Анализ успеваемости группы"))
        self.label.setText(_translate("MainWindow", "Номер группы:"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "Тип анализа:"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton.setText(_translate("MainWindow", "Отобразить диаграмму"))
        self.pushButton_2.setText(_translate("MainWindow", "Назад"))
        self.pushButton_3.setText(_translate("MainWindow", "Закрыть"))
        self.label_5.setText(_translate("MainWindow", "Период:"))
        self.label_6.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "Сессия:"))
        self.label_8.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_4.setText(_translate("MainWindow", "Сформировать отчет"))

    def close_window(self):
        self.analytics_table_group_window.close()

    def previous_page(self):
        self.analytics_table_group_window.hide()
        self.group_analytics_window.show()

    def report(self):
        r = Report()
        r.group_number = self.group
        r.type_analysis = self.type_analysis
        r.period = self.period
        r.session = self.stud_session
        r.header_table = self.table_header
        r.body_table = self.result
        name = "Группа: " + self.group + "/" + self.type_analysis

        if self.type_analysis == "Средняя оценка по итогам сессии":
            control = Control()
            proportional_result: np.ndarray = control.analysis_group_proportional(self.session, self.group, self.stud_session, self.period)
            r.proportional_result = proportional_result

        r.name = name
        list_of_report_object.append(r)
        list_of_report_name.append(name)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Отчет сформирован")
        msg.setInformativeText('Ваш отчет сформирован.')
        msg.setWindowTitle("Отчет сформирован")
        msg.exec_()

    def show_diagram(self):
        self.group_diagram_ui.label_4.setText(self.label_2.text())
        self.group_diagram_ui.label_7.setText(self.label_8.text())
        self.group_diagram_ui.label_8.setText(self.label_6.text())
        self.group_diagram_ui.label_10.setText(self.label_4.text())

        max_value = 0
        series = QBarSeries()
        for i in self.result:
            set0 = QBarSet(i[0])
            set0.append(float(i[1]))
            series.append(set0)
            if max_value < (float(i[1])):
                max_value = float(i[1])

        axisY = QValueAxis()
        axisY.setRange(0, max_value)

        chart = QChart()
        series.attachAxis(axisY)
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart.addAxis(axisY, Qt.AlignLeft)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        centralwidget = self.group_diagram_ui.centralwidget
        self.group_diagram_ui.chartview = QChartView(chart, centralwidget)
        self.group_diagram_ui.chartview.setGeometry(QtCore.QRect(10, 110, 880, 371))
        self.group_diagram_ui.pushButton_3.show()
        self.group_diagram_ui.update(self.dark_theme)
        self.group_diagram_window.show()

    def update(self, dark_theme):
        if dark_theme:
            self.analytics_table_group_window.setStyleSheet(window_css)
            self.tableWidget.setStyleSheet(table_css)
            self.tableWidget.horizontalHeader().setStyleSheet(table_header_css)
            self.tableWidget.verticalHeader().setStyleSheet(table_header_css)
            self.label_8.setStyleSheet(label_css)
            self.label_7.setStyleSheet(label_css)
            self.label_6.setStyleSheet(label_css)
            self.label_5.setStyleSheet(label_css)
            self.pushButton_3.setStyleSheet(button_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.pushButton.setStyleSheet(button_css)
            self.label_4.setStyleSheet(label_css)
            self.label_3.setStyleSheet(label_css)
            self.label.setStyleSheet(label_css)
            self.label_2.setStyleSheet(label_css)
            self.pushButton_4.setStyleSheet(button_css)
            self.dark_theme = True
        else:
            self.analytics_table_group_window.setStyleSheet("")
            self.tableWidget.setStyleSheet("")
            self.tableWidget.horizontalHeader().setStyleSheet("")
            self.tableWidget.verticalHeader().setStyleSheet("")
            self.label_8.setStyleSheet("")
            self.label_7.setStyleSheet("")
            self.label_6.setStyleSheet("")
            self.label_5.setStyleSheet("")
            self.pushButton_3.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.label_4.setStyleSheet("")
            self.label_3.setStyleSheet("")
            self.label.setStyleSheet("")
            self.label_2.setStyleSheet("")
            self.pushButton_4.setStyleSheet("")
            self.dark_theme = False
