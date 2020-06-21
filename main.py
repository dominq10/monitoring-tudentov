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
import sys

from PyQt5 import QtWidgets
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

from connecting import my_databases
from forms.py.mainwindow import FormMainwindow

engine = create_engine(my_databases, pool_size=10, max_overflow=20)

Session = sessionmaker(bind=engine)

Base = declarative_base()


def main():
    app = QtWidgets.QApplication(sys.argv)

    session = Session()

    main_window = QtWidgets.QMainWindow()
    main_window_ui = FormMainwindow(main_window, session)
    main_window_ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
