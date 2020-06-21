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
from PyQt5 import QtGui, QtWidgets


def set_items_to_table(table, items: np.ndarray, DARK_THEME=False):
    try:
        rows, columns = items.shape
    except:
        return table

    table.setRowCount(rows)
    table.setColumnCount(columns)
    flag = 0
    for i in range(rows):
        if i%2 == 0:
            flag = 1
        for j in range(columns):
            newitem = QtWidgets.QTableWidgetItem(items[i][j])
            if flag == 0 and DARK_THEME is True:
                newitem.setBackground(QtGui.QColor(36, 48, 63))
            table.setItem(i, j, QtWidgets.QTableWidgetItem(newitem))
        flag = 0

    return table
