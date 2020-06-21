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
from PyQt5.QtChart import (QBarCategoryAxis, QBarSet, QChart, QChartView,
                           QPercentBarSeries, QPieSeries, QPieSlice)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

from db.models import Control
from style.dark_theme import button_css, label_css, window_css


class FormGroupDiagram(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.analytics_table_group_window = main_window.analytics_table_group_window
        self.session = main_window.session
        self.group_diagram_window = main_window.group_diagram_window
        self.group_diagram_window.setObjectName("MainWindow")
        self.group_diagram_window.setFixedSize(900, 563)
        self.centralwidget = QtWidgets.QWidget(self.group_diagram_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(760, 500, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_window)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 500, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.previous_page)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 110, 551, 371))
        self.label_11.setMinimumSize(QtCore.QSize(400, 0))
        self.label_11.setObjectName("label_11")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 111, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(115, 10, 361, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(360, 10, 51, 20))
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(415, 10, 141, 21))
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 30, 90, 20))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(100, 30, 373, 20))
        self.label_10.setObjectName("label_10")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(70, 45, 373, 31))
        self.label_8.setObjectName("label_8")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 50, 58, 21))
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 500, 281, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_proportional_chart)
        self.group_diagram_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.group_diagram_window)
        self.statusbar.setObjectName("statusbar")
        self.group_diagram_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.group_diagram_window)
        QtCore.QMetaObject.connectSlotsByName(self.group_diagram_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Аналитика: вывод диаграммы"))
        self.pushButton.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_2.setText(_translate("MainWindow", "Назад"))
        self.label_11.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "Номер группы:"))
        self.label_4.setText(_translate("MainWindow", "ФИО"))
        self.label_5.setText(_translate("MainWindow", "Сессия:"))
        self.label_7.setText(_translate("MainWindow", "Тип сессии"))
        self.label_9.setText(_translate("MainWindow", "Тип анализа:"))
        self.label_10.setText(_translate("MainWindow", "Наименование типа анализа"))
        self.label_8.setText(_translate("MainWindow", "Наименование периода"))
        self.label.setText(_translate("MainWindow", "Период:"))
        self.pushButton_3.setText(_translate("MainWindow", "Отобразить диаграмму в пропорциях"))

    def close_window(self):
        self.group_diagram_window.close()

    def show_proportional_chart(self):
        type_diagram = self.pushButton_3.text()
        self.group_diagram_window.hide()
        if type_diagram == "Отобразить диаграмму в пропорциях":

            group = self.label_4.text()
            session = self.label_7.text()
            period = self.label_8.text()

            control = Control()
            result: np.ndarray = control.analysis_group_proportional(self.session, group, session, period)

            r_len = len(result)
            set0 = QBarSet('0-24')
            set1 = QBarSet('25-49')
            set2 = QBarSet('50-74')
            set3 = QBarSet('75-100')

            if r_len == 4:
                set0 << int(result[0][1]) << int(result[1][1]) << int(result[2][1]) << int(result[3][1])
                set1 << int(result[0][2]) << int(result[1][2]) << int(result[2][2]) << int(result[3][2])
                set2 << int(result[0][3]) << int(result[1][3]) << int(result[2][3]) << int(result[3][3])
                set3 << int(result[0][4]) << int(result[1][4]) << int(result[2][4]) << int(result[3][4])

            elif r_len == 3:
                set0 << int(result[0][1]) << int(result[1][1]) << int(result[2][1])
                set1 << int(result[0][2]) << int(result[1][2]) << int(result[2][2])
                set2 << int(result[0][3]) << int(result[1][3]) << int(result[2][3])
                set3 << int(result[0][4]) << int(result[1][4]) << int(result[2][4])

            elif r_len == 2:
                set0 << int(result[0][1]) << int(result[1][1])
                set1 << int(result[0][2]) << int(result[1][2])
                set2 << int(result[0][3]) << int(result[1][3])
                set3 << int(result[0][4]) << int(result[1][4])

            else:
                set0 << int(result[0][1])
                set1 << int(result[0][2])
                set2 << int(result[0][3])
                set3 << int(result[0][4])

            cat = []
            for i in result:
                cat.append(i[0])

            series = QPercentBarSeries()
            series.append(set0)
            series.append(set1)
            series.append(set2)
            series.append(set3)

            chart = QChart()
            chart.addSeries(series)
            chart.setAnimationOptions(QChart.SeriesAnimations)

            axis = QBarCategoryAxis()
            axis.append(cat)
            chart.createDefaultAxes()
            chart.setAxisX(axis, series)

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            centralwidget = self.centralwidget
            self.chartview = QChartView(chart, centralwidget)
            self.chartview.setGeometry(QtCore.QRect(10, 110, 880, 371))

        else:
            series = QPieSeries()
            for i in self.data:
                value = str(i[0]) + " / " + str(i[1])
                series.append(value, int(i[1]))

            # adding slice
            slice = QPieSlice()
            slice = series.slices()[0]
            slice.setExploded(True)
            slice.setLabelVisible(True)
            slice.setPen(QPen(Qt.darkGreen, 2))
            slice.setBrush(Qt.green)

            chart = QChart()
            chart.legend().hide()
            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setAnimationOptions(QChart.SeriesAnimations)

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            centralwidget = self.centralwidget
            self.chartview = QChartView(chart, centralwidget)
            self.chartview.setGeometry(QtCore.QRect(10, 110, 880, 371))

        self.pushButton_3.hide()
        self.group_diagram_window.show()

    def previous_page(self):
        self.group_diagram_window.hide()
        self.analytics_table_group_window.show()

    def update(self, dark_theme):
        if dark_theme:
            self.group_diagram_window.setStyleSheet(window_css)
            self.pushButton.setStyleSheet(button_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.label_11.setStyleSheet(label_css)
            self.label.setStyleSheet(label_css)
            self.pushButton_3.setStyleSheet(button_css)
            self.label_8.setStyleSheet(label_css)
            self.label_10.setStyleSheet(label_css)
            self.label_9.setStyleSheet(label_css)
            self.label_3.setStyleSheet(label_css)
            self.label_4.setStyleSheet(label_css)
            self.label_7.setStyleSheet(label_css)
            self.label_5.setStyleSheet(label_css)

            self.dark_theme = True
        else:
            self.group_diagram_window.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.label_11.setStyleSheet("")
            self.label.setStyleSheet("")
            self.pushButton_3.setStyleSheet("")
            self.label_8.setStyleSheet("")
            self.label_10.setStyleSheet("")
            self.label_9.setStyleSheet("")
            self.label_3.setStyleSheet("")
            self.label_4.setStyleSheet("")
            self.label_7.setStyleSheet("")
            self.label_5.setStyleSheet("")
            self.dark_theme = False
