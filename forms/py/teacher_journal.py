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

from style.dark_theme import (button_css, table_css, table_header_css,
                              window_css)


class FormTeacherJournal(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.teacher_journal_window = main_window.teacher_journal_window
        self.teacher_journal_window.setObjectName("MainWindow")
        self.teacher_journal_window.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self.teacher_journal_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_window)
        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.teacher_journal_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.teacher_journal_window)
        self.statusbar.setObjectName("statusbar")
        self.teacher_journal_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.teacher_journal_window)
        QtCore.QMetaObject.connectSlotsByName(self.teacher_journal_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Оценки"))
        self.pushButton.setText(_translate("MainWindow", "Закрыть"))

    def close_window(self):
        self.tableWidget.setRowCount(0)
        self.teacher_journal_window.close()

    def update(self, dark_theme):
        if dark_theme:
            self.teacher_journal_window.setStyleSheet(window_css)
            self.tableWidget.setStyleSheet(table_css)
            self.tableWidget.horizontalHeader().setStyleSheet(table_header_css)
            self.tableWidget.verticalHeader().setStyleSheet(table_header_css)
            self.pushButton.setStyleSheet(button_css)
            self.dark_theme = True
        else:
            self.teacher_journal_window.setStyleSheet("")
            self.tableWidget.setStyleSheet("")
            self.tableWidget.horizontalHeader().setStyleSheet("")
            self.tableWidget.verticalHeader().setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.dark_theme = False
