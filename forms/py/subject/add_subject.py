from PyQt5 import QtCore, QtWidgets


class form_add_subject(object):
    def __init__(self, MainWindow):
        self.dark_theme = False
        self.add_subject_window = MainWindow.add_subject_window
        self.add_subject_window.setObjectName("MainWindow")
        self.add_subject_window.resize(493, 285)
        self.centralwidget = QtWidgets.QWidget(self.add_subject_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 471, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 220, 131, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(350, 220, 131, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.close_window)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 58, 16))
        self.label_2.setObjectName("label_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 90, 471, 121))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 469, 119))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setGeometry(QtCore.QRect(10, 10, 86, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 40, 86, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.add_subject_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.add_subject_window)
        self.statusbar.setObjectName("statusbar")
        self.add_subject_window.setStatusBar(self.statusbar)

        self.retranslateUi(self.add_subject_window)
        QtCore.QMetaObject.connectSlotsByName(self.add_subject_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Добавить дисциплину"))
        self.label.setText(_translate("MainWindow", "Наименование дисциплины"))
        self.pushButton_2.setText(_translate("MainWindow", "Сохранить"))
        self.pushButton_3.setText(_translate("MainWindow", "Закрыть"))
        self.label_2.setText(_translate("MainWindow", "Группы"))
        self.checkBox.setText(_translate("MainWindow", "78678"))
        self.checkBox_2.setText(_translate("MainWindow", "54365"))

    def close_window(self):
        self.add_subject_window.close()

    def update(self, dark_theme):
        if dark_theme:

            self.dark_theme = True
        else:

            self.dark_theme = False
