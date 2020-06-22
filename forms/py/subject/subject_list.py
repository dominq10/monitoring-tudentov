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

from db.models import Discipline
from style.dark_theme import label_css, list_css, window_css
from transform.query import query_to_list_of_name


class FormSubjectList(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.session = main_window.session
        self.subject_window = main_window.subject_window
        self.subject_window.setObjectName("MainWindow")
        self.subject_window.setFixedSize(573, 314)
        self.centralwidget = QtWidgets.QWidget(self.subject_window)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 551, 231))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setEditTriggers(QtWidgets.QListWidget.NoEditTriggers)

        discipline = Discipline()
        query_list = discipline.all(self.session)
        ls = query_to_list_of_name(query_list)
        self.listWidget.addItems(ls)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 171, 16))
        self.label.setObjectName("label")
        self.subject_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.subject_window)
        self.statusbar.setObjectName("statusbar")
        self.subject_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.subject_window)
        QtCore.QMetaObject.connectSlotsByName(self.subject_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Дисциплины"))
        self.label.setText(_translate("MainWindow", "Диспциплины"))

    def update(self, dark_theme):
        if dark_theme:
            self.subject_window.setStyleSheet(window_css)
            self.listWidget.setStyleSheet(list_css)
            self.label.setStyleSheet(label_css)
            self.dark_theme = True
        else:
            self.subject_window.setStyleSheet("")
            self.listWidget.setStyleSheet("")
            self.label.setStyleSheet("")
            self.dark_theme = False
