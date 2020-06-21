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
from PyQt5 import QtCore, QtWidgets


class FormLaggingStudents(object):
    def __init__(self, main_window):
        self.lagging_students_window = main_window.lagging_students_window
        self.lagging_students_window.setObjectName("MainWindow")
        self.lagging_students_window.resize(800, 534)
        self.centralwidget = QtWidgets.QWidget(self.lagging_students_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 131, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 58, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 80, 151, 16))
        self.label_4.setObjectName("label_4")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(199, 9, 581, 451))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 579, 449))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.listWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listWidget.setGeometry(QtCore.QRect(-5, -9, 591, 461))
        self.listWidget.setObjectName("listWidget")
        ls = ["Антонов Варлам Парфеньевич",
              "Гусев Гаянэ Ростиславович",
              "Иванов Оскар Иосифович",
              "Лыткин Герман Олегович",
              "Носов Мечислав Яковович",
              "Силин Тарас Якунович",
              "Ширяев Яков Филиппович"
              ]
        self.listWidget.addItems(ls)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(670, 470, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_window)
        self.lagging_students_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.lagging_students_window)
        self.statusbar.setObjectName("statusbar")
        self.lagging_students_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.lagging_students_window)
        QtCore.QMetaObject.connectSlotsByName(self.lagging_students_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Аналитика: список отстающих студентов"))
        self.label.setText(_translate("MainWindow", "Дисциплина:"))
        self.label_2.setText(_translate("MainWindow", "Наименование"))
        self.label_3.setText(_translate("MainWindow", "Группа:"))
        self.label_4.setText(_translate("MainWindow", "Наименование группы"))
        self.pushButton.setText(_translate("MainWindow", "Закрыть"))

    def close_window(self):
        self.lagging_students_window.close()
