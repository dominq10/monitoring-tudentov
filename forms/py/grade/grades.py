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

from db.models import Grade, Work
from forms.py.teacher_journal import FormTeacherJournal
from style.dark_theme import button_css, combobox_css, label_css, window_css
from transform.items import set_items_to_table


class FormGrade(object):
    def __init__(self, main_window):
        self.dark_theme = False
        self.session = main_window.session
        self.grade_window = main_window.grade_window
        self.grade_window.setObjectName("MainWindow")
        self.grade_window.setFixedSize(458, 132)
        self.centralwidget = QtWidgets.QWidget(self.grade_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 70, 95, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.clicked.connect(self.show_teacher_journal_window)
        self.pushButton.setGeometry(QtCore.QRect(210, 70, 147, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 79, 16))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(5, 30, 221, 32))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 30, 221, 32))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(240, 10, 44, 16))
        self.label_2.setObjectName("label_2")
        self.grade_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.grade_window)
        self.statusbar.setObjectName("statusbar")
        self.grade_window.setStatusBar(self.statusbar)

        self.teacher_journal_window = QtWidgets.QMainWindow()
        self.teacher_journal_window_ui = FormTeacherJournal(self)

        self.retranslateUi(self.grade_window)
        QtCore.QMetaObject.connectSlotsByName(self.grade_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Оценки"))
        self.pushButton_2.setText(_translate("MainWindow", "Закрыть"))
        self.pushButton.setText(_translate("MainWindow", "Открыть журнал"))
        self.label.setText(_translate("MainWindow", "Дисциплина"))
        self.label_2.setText(_translate("MainWindow", "Группа"))

    def show_teacher_journal_window(self):
        work = Work()
        group_number: str = self.comboBox_2.currentText()
        discipline_name: str = self.comboBox.currentText()

        grade = Grade()
        table_content: np.ndarray = grade.all(self.session, discipline_name, group_number)
        self.teacher_journal_window_ui.tableWidget = set_items_to_table(self.teacher_journal_window_ui.tableWidget, table_content, DARK_THEME=self.dark_theme)

        table_header: list = work.show_name(self.session, group_number, discipline_name, flag_header=True)
        self.teacher_journal_window_ui.tableWidget.setHorizontalHeaderLabels(table_header)

        self.teacher_journal_window_ui.tableWidget.resizeColumnsToContents()
        self.teacher_journal_window_ui.update(self.dark_theme)

        self.teacher_journal_window.show()

    def close_window(self):
        self.grade_window.close()

    def update(self, dark_theme):
        if dark_theme:
            self.grade_window.setStyleSheet(window_css)
            self.pushButton_2.setStyleSheet(button_css)
            self.pushButton.setStyleSheet(button_css)
            self.comboBox_2.setStyleSheet(combobox_css)
            self.comboBox.setStyleSheet(combobox_css)
            self.label_2.setStyleSheet(label_css)
            self.label.setStyleSheet(label_css)
            self.dark_theme = True
        else:
            self.grade_window.setStyleSheet("")
            self.pushButton_2.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.comboBox_2.setStyleSheet("")
            self.comboBox.setStyleSheet("")
            self.label_2.setStyleSheet("")
            self.label.setStyleSheet("")
            self.dark_theme = False
