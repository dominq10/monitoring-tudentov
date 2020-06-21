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
from PyQt5.QtWidgets import QMessageBox


def login_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Ошибка")
    msg.setInformativeText('Не правильная пара логин/пароль')
    msg.setWindowTitle("Ошибка")
    msg.exec_()


def bd_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Ошибка синхронизации с БД")
    msg.setInformativeText('Попробуйте открыть окно еще раз.')
    msg.setWindowTitle("Ошибка синхронизации с БД")
    msg.exec_()
