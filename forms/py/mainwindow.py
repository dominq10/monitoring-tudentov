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

from db.models import Discipline, Grade, Group
from forms.py.grade.grades import FormGrade
from forms.py.login import FormLogin
from forms.py.not_submitted_work import form_not_submitted_work
from forms.py.report import FormReport
from forms.py.settings import FormSettings
from forms.py.student.group_choice import FormGroupChoice
from forms.py.subject.subject_list import FormSubjectList
from forms.py_analytics.choice_analytics import FormChoiceAnalyticsWindow
from report import list_of_report_name
from transform.items import set_items_to_table


class FormMainwindow(object):
    def __init__(self, main_window, session):
        self.dark_theme = False
        self.session = session
        self.main_window = main_window
        self.main_window.setObjectName("MainWindow")
        self.main_window.setFixedSize(1120, 800)
        self.centralwidget = QtWidgets.QWidget(self.main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 7)
        self.pushButton_student = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_student.setObjectName("pushButton_student")
        self.pushButton_student.clicked.connect(self.show_group_choice_window)
        self.gridLayout.addWidget(self.pushButton_student, 0, 1, 1, 1)
        self.pushButton_analytics = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_analytics.setObjectName("pushButton_analytics")
        self.pushButton_analytics.clicked.connect(self.show_choice_analytics_window)
        self.gridLayout.addWidget(self.pushButton_analytics, 0, 3, 1, 1)
        self.pushButton_close = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_close.sizePolicy().hasHeightForWidth())
        self.pushButton_close.setSizePolicy(sizePolicy)
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.clicked.connect(self.close_window)
        self.gridLayout.addWidget(self.pushButton_close, 0, 6, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 7)
        self.pushButton_grade = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_grade.setObjectName("pushButton_grade")
        self.pushButton_grade.clicked.connect(self.show_grade_window)
        self.gridLayout.addWidget(self.pushButton_grade, 0, 2, 1, 1)
        self.pushButton_reports = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reports.setObjectName("pushButton_reports")
        self.pushButton_reports.clicked.connect(self.show_report_window)
        self.gridLayout.addWidget(self.pushButton_reports, 0, 4, 1, 1)
        self.pushButton_lesson = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_lesson.setObjectName("pushButton_lesson")
        self.pushButton_lesson.clicked.connect(self.show_subject_window)
        self.gridLayout.addWidget(self.pushButton_lesson, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 7)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_settings_window)
        self.gridLayout.addWidget(self.pushButton, 0, 5, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.main_window)
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)

        # Инициализируем окна
        self.login_window = QtWidgets.QMainWindow()
        self.login_ui = FormLogin(self)

        self.subject_window = QtWidgets.QMainWindow()
        self.subject_ui = FormSubjectList(self)

        self.group_choice_window = QtWidgets.QMainWindow()
        self.group_choice_ui = FormGroupChoice(self)

        self.grade_window = QtWidgets.QMainWindow()
        self.grade_ui = FormGrade(self)

        self.choice_analytics_window = QtWidgets.QMainWindow()
        self.choice_analytics_ui = FormChoiceAnalyticsWindow(self)

        self.report_window = QtWidgets.QMainWindow()
        self.report_ui = FormReport(self)

        self.not_submitted_work_window = QtWidgets.QMainWindow()
        self.not_submitted_work_ui = form_not_submitted_work(self)

        self.settings_window = QtWidgets.QMainWindow()
        self.settings_ui = FormSettings(self)

        self.retranslateUi(self.main_window)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Личный кабинет"))
        self.pushButton_student.setText(_translate("MainWindow", "Студенты"))
        self.pushButton_analytics.setText(_translate("MainWindow", "Аналитика"))
        self.pushButton_close.setText(_translate("MainWindow", "Выход"))
        self.pushButton_grade.setText(_translate("MainWindow", "Оценки"))
        self.pushButton_reports.setText(_translate("MainWindow", "Отчеты"))
        self.pushButton_lesson.setText(_translate("MainWindow", "Дисциплины"))
        self.label.setText(_translate("MainWindow", "Cписок отстающих студентов"))
        self.pushButton.setText(_translate("MainWindow", "Параметры"))

    def show(self):
        grade = Grade()
        result = grade.lagging_students(self.session)
        self.tableWidget = set_items_to_table(self.tableWidget, result, DARK_THEME=self.dark_theme)
        self.tableWidget.setHorizontalHeaderLabels(["ФИО", "Группа", "Дисциплина", "Список не сданных работ"])
        self.tableWidget.resizeColumnsToContents()
        self.main_window.show()

    def show_login_window(self):
        self.login_window.show()

    def show_subject_window(self):
        self.subject_ui.update(self.dark_theme)
        self.subject_window.show()

    def show_group_choice_window(self):
        group = Group()
        ls_name = group.show_name(self.session)
        self.group_choice_ui.comboBox.addItems(ls_name)
        self.group_choice_ui.update(self.dark_theme)
        self.group_choice_window.show()

    def show_grade_window(self):
        group = Group()
        ls_name = group.show_name(self.session)
        self.grade_ui.comboBox_2.clear()
        self.grade_ui.comboBox_2.addItems(ls_name)

        discipline = Discipline
        d_name = discipline.show_name(self.session)
        self.grade_ui.comboBox.clear()
        self.grade_ui.comboBox.addItems(d_name)

        self.grade_ui.update(self.dark_theme)
        self.grade_window.show()

    def show_choice_analytics_window(self):
        self.choice_analytics_ui.update(self.dark_theme)
        self.choice_analytics_window.show()

    def show_report_window(self):
        self.report_ui.comboBox.clear()
        self.report_ui.comboBox.addItems(list_of_report_name)
        self.report_window.show()

    def show_settings_window(self):
        self.settings_ui.update(self.dark_theme)
        self.settings_window.show()

    def update(self, dark_theme):
        if dark_theme is True:
            self.main_window.setStyleSheet("background-color: #1a222c; border-color: #24303f; border-width: 1px;")
            self.pushButton_reports.setStyleSheet(
                "background-color: #24303f; border-width: 1px; border-radius: 10px; border-color: #24303f; font: 12px; min-width: 8em; padding: 6px; margin:5px; color: #c2cdd9;")
            self.pushButton_close.setStyleSheet(
                "background-color: #24303f; border-width: 1px; border-radius: 10px; border-color: #24303f; font: 12px; min-width: 8em; padding: 6px; margin:5px; color: #c2cdd9;")
            self.pushButton_analytics.setStyleSheet(
                "background-color: #24303f; border-width: 1px; border-radius: 10px; border-color: #24303f; font: 12px; min-width: 8em; padding: 6px; margin:5px; color: #c2cdd9;")
            self.pushButton_student.setStyleSheet(
                "background-color: #24303f; border-width: 1px; border-radius: 10px; border-color: #24303f; font: 12px; min-width: 8em; padding: 6px; margin:5px; color: #c2cdd9;")
            self.tableWidget.setStyleSheet("color: #8199b3; font: 12px;")
            self.tableWidget.horizontalHeader().setStyleSheet("background-color: #344c68; font: 14px;")
            self.tableWidget.verticalHeader().setStyleSheet("background-color: #344c68; font: 14px; ")
            self.line.setStyleSheet('background-color: #24303f;')
            self.pushButton_lesson.setStyleSheet(
                "background-color: #24303f; border-width: 1px; border-radius: 10px; border-color: #24303f; font: 12px; min-width: 8em; padding: 6px; margin:5px; color: #c2cdd9;")
            self.pushButton_grade.setStyleSheet(
                "background-color: #24303f; border-width: 1px; border-radius: 10px; border-color: #24303f; font: 12px; min-width: 8em; padding: 6px; margin:5px; color: #c2cdd9;")
            self.pushButton.setStyleSheet(
                "background-color: #24303f; border-width: 1px; border-radius: 10px; border-color: #24303f; font: 12px; min-width: 8em; padding: 6px; margin:5px; color: #c2cdd9;")
            self.label.setStyleSheet("font: 12px; color: #c2cdd9;")
            self.dark_theme = True
        else:
            self.main_window.setStyleSheet("")
            self.pushButton_reports.setStyleSheet("")
            self.pushButton_close.setStyleSheet("")
            self.pushButton_analytics.setStyleSheet("")
            self.pushButton_student.setStyleSheet("")
            self.tableWidget.setStyleSheet("")
            self.tableWidget.horizontalHeader().setStyleSheet("")
            self.tableWidget.verticalHeader().setStyleSheet("")
            self.line.setStyleSheet('')
            self.pushButton_lesson.setStyleSheet("")
            self.pushButton_grade.setStyleSheet("")
            self.pushButton.setStyleSheet("")
            self.label.setStyleSheet("")
            self.dark_theme = False

        self.main_window.hide()
        self.main_window.show()

    def close_window(self):
        self.main_window.close()
