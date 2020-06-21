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
from PyQt5 import QtCore, QtWidgets

from db.models import Group, Student
from forms.py.student.group_list import FormGroupWindow
from forms.py.student.student_list import FormStudentList
from style.dark_theme import button_css, combobox_css, label_css, window_css
from transform.items import set_items_to_table


class FormGroupChoice(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.session = main_window.session
        self.group_choice_window = main_window.group_choice_window
        self.group_choice_window.setObjectName("MainWindow")
        self.group_choice_window.setFixedSize(510, 187)
        self.centralwidget = QtWidgets.QWidget(self.group_choice_window)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 40, 241, 32))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 141, 16))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(380, 120, 121, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 50, 221, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.show_student_list)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(280, 20, 221, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.show_group_window)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(20, 100, 471, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.group_choice_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.group_choice_window)
        self.statusbar.setObjectName("statusbar")
        self.group_choice_window.setStatusBar(self.statusbar)

        self.student_list_window = QtWidgets.QMainWindow()
        self.student_list_ui = FormStudentList(self)

        self.group_window = QtWidgets.QMainWindow()
        self.group_ui = FormGroupWindow(self)

        self.retranslateUi(self.group_choice_window)
        QtCore.QMetaObject.connectSlotsByName(self.group_choice_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Студенты"))
        self.label.setText(_translate("MainWindow", "Выберите группу"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton_3.setText(_translate("MainWindow", "Просмотреть список группы"))
        self.pushButton_4.setText(_translate("MainWindow", "Группы"))

    def show_student_list(self):
        student = Student()
        group_number: str = self.comboBox.currentText()
        ls_all: list = student.all(self.session, group_number)
        ls_all: np.ndarray = np.array(ls_all)
        self.student_list_ui.tableWidget = set_items_to_table(self.student_list_ui.tableWidget, ls_all, DARK_THEME=self.dark_theme)
        self.student_list_ui.update_window(self.dark_theme)
        self.student_list_ui.tableWidget.resizeColumnsToContents()
        self.student_list_ui.label.setText("Список группы: №" + str(group_number))
        self.student_list_ui.group_number = str(group_number)
        self.student_list_window.show()

    def show_group_window(self):
        group = Group()
        ls_all = group.show_all(self.session)
        ls_all = np.array(ls_all)
        self.group_ui.tableWidget = set_items_to_table(self.group_ui.tableWidget, ls_all, DARK_THEME=self.dark_theme)
        self.group_ui.update(self.dark_theme)
        self.group_ui.tableWidget.resizeColumnsToContents()

        self.group_window.show()

    def close_window(self):
        self.comboBox.clear()
        self.group_choice_window.close()

    def update(self, dark_theme):
        if dark_theme:
            self.group_choice_window.setStyleSheet(window_css)
            self.comboBox.setStyleSheet(combobox_css)
            self.label.setStyleSheet(label_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.pushButton_4.setStyleSheet(button_css)
            self.pushButton_3.setStyleSheet(button_css)
            self.dark_theme = True
        else:
            self.group_choice_window.setStyleSheet("")
            self.comboBox.setStyleSheet("")
            self.label.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.pushButton_4.setStyleSheet("")
            self.pushButton_3.setStyleSheet("")
            self.dark_theme = False
