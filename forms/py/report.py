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

from report import Report, list_of_report_name, list_of_report_object


class FormReport(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.report_window = main_window.report_window
        self.report_window.setObjectName("MainWindow")
        self.report_window.resize(581, 188)
        self.centralwidget = QtWidgets.QWidget(self.report_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 16))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(0, 30, 551, 32))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(list_of_report_name)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 90, 261, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.clear_report)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 120, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 60, 261, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.save_report)
        self.report_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.report_window)
        self.statusbar.setObjectName("statusbar")
        self.report_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.report_window)
        QtCore.QMetaObject.connectSlotsByName(self.report_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Сохранить отчет"))
        self.label.setText(_translate("MainWindow", "Выберите отчет"))
        self.pushButton.setText(_translate("MainWindow", "Удалить сформированные отчеты"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_3.setText(_translate("MainWindow", "Сохранить отчет"))

    def close_window(self):
        self.report_window.close()

    def clear_report(self):
        self.comboBox.clear()
        self.report_window.hide()
        self.report_window.show()

    def save_report(self):
        name = self.comboBox.currentText()
        for r in list_of_report_object:
            if r.name == name:
                name = QtWidgets.QFileDialog.getSaveFileName(self.report_window, 'Save File', "Отчет аналитики.pdf")
                r.make_report(name[0])
                break
