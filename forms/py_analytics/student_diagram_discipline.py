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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView

from style.dark_theme import button_css, label_css, window_css


class FormStudentDiagramDiscipline(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.analytics_table_discipline_student_window = main_window.analytics_table_discipline_student_window
        self.session = main_window.session
        self.student_diagram_discipline_window = main_window.student_diagram_discipline_window
        self.student_diagram_discipline_window.setObjectName("MainWindow")
        self.student_diagram_discipline_window.setFixedSize(900, 563)
        self.centralwidget = QtWidgets.QWidget(self.student_diagram_discipline_window)
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
        self.label_11.hide()

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 110, 880, 371))
        chart = QChart()
        self.chartview = QChartView(chart, self.centralwidget)
        self.chartview.setGeometry(QtCore.QRect(10, 100, 101, 2))

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 100, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(102, 10, 361, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(370, 10, 51, 20))
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(425, 10, 141, 21))
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 30, 90, 20))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(70, 30, 250, 20))
        self.label_10.setObjectName("label_10")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(102, 50, 373, 21))
        self.label_8.setObjectName("label_8")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 50, 100, 21))
        self.label.setObjectName("label")

        self.student_diagram_discipline_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.student_diagram_discipline_window)
        self.statusbar.setObjectName("statusbar")
        self.student_diagram_discipline_window.setStatusBar(self.statusbar)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 500, 281, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_proportional_chart)

        self.retranslateUi(self.student_diagram_discipline_window)
        QtCore.QMetaObject.connectSlotsByName(self.student_diagram_discipline_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Аналитика: вывод диаграммы"))
        self.pushButton.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_2.setText(_translate("MainWindow", "Назад"))
        self.label_11.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "Дисциплина:"))
        self.label_4.setText(_translate("MainWindow", "ФИО"))
        self.label_7.setText(_translate("MainWindow", "Тип сессии"))
        self.label_9.setText(_translate("MainWindow", "Группа:"))
        self.label_10.setText(_translate("MainWindow", "Наименование типа анализа"))
        self.label_8.setText(_translate("MainWindow", "Наименование периода"))
        self.label.setText(_translate("MainWindow", "Тип анализа:"))
        self.pushButton_3.setText(_translate("MainWindow", "Отобразить диаграмму в пропорциях"))

    def close_window(self):
        self.student_diagram_discipline_window.close()

    def show_proportional_chart(self):
        self.student_diagram_discipline_window.hide()
        self.chartview.hide()

        name = []
        value = []
        for i in self.data:
            name.append(str(i[0]))
            value.append(float(i[1]))

        fig = Figure(figsize=(10, 3),
                     dpi=100)  # Инициализирования объект fig класса Figure размером 5 на 3 и плотность 100
        ax = fig.add_subplot()  # Инициализиурем subplot ax

        # Задаем ax что будет именно круговая диаграмма
        ax.pie(value,  # Значения сколько раз встречается определенная степень образования
               labels=name,  # title для частей
               shadow=0,  # Тень
               startangle=90,  # Угол с которого будет начинаться первая доля
               autopct='%1.1f%%'  # Указываем, что необходимо отобраджать проценты
               )

        canvas = FigureCanvasQTAgg(fig)
        canvas.draw()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(canvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        self.widget.setLayout(layout)
        self.widget.show()

        self.chartview.setGeometry(QtCore.QRect(2, 2, 3, 3))
        self.pushButton_3.hide()

        self.student_diagram_discipline_window.show()

    def previous_page(self):
        self.student_diagram_discipline_window.hide()
        self.analytics_table_discipline_student_window.show()

    def update(self, dark_theme):
        if dark_theme:
            self.student_diagram_discipline_window.setStyleSheet(window_css)
            self.pushButton_3.setStyleSheet(button_css)
            self.pushButton.setStyleSheet(button_css)
            self.label.setStyleSheet(label_css)
            self.label_8.setStyleSheet(label_css)
            self.label_10.setStyleSheet(label_css)
            self.label_9.setStyleSheet(label_css)
            self.label_7.setStyleSheet(label_css)
            self.label_5.setStyleSheet(label_css)
            self.label_4.setStyleSheet(label_css)
            self.label_3.setStyleSheet(label_css)
            self.pushButton_2.setStyleSheet(button_css)

            self.dark_theme = True
        else:
            self.student_diagram_discipline_window.setStyleSheet("")
            self.pushButton_3.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.label.setStyleSheet("")
            self.label_8.setStyleSheet("")
            self.label_10.setStyleSheet("")
            self.label_9.setStyleSheet("")
            self.label_7.setStyleSheet("")
            self.label_5.setStyleSheet("")
            self.label_4.setStyleSheet("")
            self.label_3.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")

            self.dark_theme = False
