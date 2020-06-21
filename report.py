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
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

list_of_report_object = []
list_of_report_name = []


class Report:
    def __init__(self):
        self.name = None
        self.header_table = None
        self.body_table = None
        self.discipline = None
        self.group_number = None
        self.period = None
        self.student = None
        self.session = None
        self.type_analysis = None
        self.proportional_result = None

    def make_report(self, path_to_save_file) -> None:
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'font/DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(200, 10, txt="Отчет", ln=1, align="C")
        pdf.cell(0, 5, '', ln=2)
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(0, 5, 'Тип анализа: ' + self.type_analysis, ln=1)
        pdf.cell(0, 5, '', ln=1)
        y_bar = 40
        if self.group_number is not None:
            pdf.cell(0, 5, 'Группа: ' + self.group_number, ln=1)
            pdf.cell(0, 5, '', ln=1)
            y_bar += 10
        if self.discipline is not None:
            pdf.cell(0, 5, 'Дисциплина: ' + self.discipline, ln=1)
            pdf.cell(0, 5, '', ln=1)
            y_bar += 10
        if self.period is not None:
            pdf.cell(0, 5, 'Период: ' + self.period, ln=1)
            pdf.cell(0, 5, '', ln=1)
            y_bar += 10
        if self.student is not None:
            pdf.cell(0, 5, 'Студент: ' + self.student, ln=1)
            pdf.cell(0, 5, '', ln=1)
            y_bar += 10
        if self.session is not None:
            pdf.cell(0, 5, 'Сессия: ' + self.session, ln=1)
            pdf.cell(0, 5, '', ln=1)
            y_bar += 10

        col_width = pdf.w / 2.2
        row_height = pdf.font_size
        spacing = 2

        pdf.set_font('DejaVu', '', 14)
        for item in self.header_table:
            pdf.cell(col_width, row_height * spacing,
                     txt=item, border=1)
        pdf.ln(row_height * spacing)
        y_bar += 10

        pdf.set_font('DejaVu', '', 12)

        name_student = []
        flag_name = 0

        count = self.name.count('Дисциплина')
        if count == 1 and self.student == None:
            flag_students = 1
        else:
            flag_students = 0

        for row in self.body_table:
            for item in row:
                if flag_students == 1 and flag_name == 0:
                    value = item.split(' ')[0]
                    pdf.cell(col_width, row_height * spacing,
                             txt=value, border=1)
                    name_student.append(value)
                    flag_name = 1
                else:
                    pdf.cell(col_width, row_height * spacing,
                             txt=item, border=1)
                    flag_name = 0
            pdf.ln(row_height * spacing)
            y_bar += 10

        name = []
        value = []
        for i in self.body_table:
            name.append(str(i[0]))
            value.append(float(i[1]))

        x_len = len(self.body_table)
        x = np.arange(0, x_len)

        fig, ax = plt.subplots()
        ax.bar(x, value)
        ax.set_ylabel(self.header_table[1])
        ax.set_xlabel(self.header_table[0])
        ax.set_xticks(x)
        if flag_students == 1:
            ax.set_xticklabels(name_student)
        else:
            ax.set_xticklabels(name)

        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2

            space = spacing
            va = 'bottom'

            if y_value < 0:
                space *= -1
                va = 'top'

            label = "{:.1f}".format(y_value)

            ax.annotate(
                label,
                (x_value, y_value),
                xytext=(0, space),
                textcoords="offset points",
                ha='center',
                va=va)

        fig.tight_layout()
        image_path = 'temp/bar.png'
        plt.savefig(image_path)

        #  pdf.add_page()
        pdf.cell(0, 5, '', ln=1)
        pdf.cell(0, 5, 'Столбчатая диаграмма:', ln=1)
        pdf.cell(0, 5, '', ln=1)
        pdf.image(image_path, x=7, y=y_bar, w=150)

        try:
            pdf.add_page()
            y = 26
            flag_pie = 0
            i = 0
            for row in self.proportional_result:
                if flag_pie == 2:
                    pdf.add_page()
                    y = 26
                if flag_pie == 1 or flag_pie == 3:
                    for i in range(0, 15):
                        pdf.cell(0, 5, '', ln=10)

                value = []
                name = []
                if row[1] != '0':
                    value.append(row[1])
                    name.append('0-24')
                if row[2] != '0':
                    value.append(row[2])
                    name.append('25-49')
                if row[3] != '0':
                    value.append(row[3])
                    name.append('50-74')
                if row[4] != '0':
                    value.append(row[4])
                    name.append('75-100')
                # fig, ax = plt.subplots()
                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)
                ax.pie(value,  # Значения сколько раз встречается определенная степень образования
                          labels=name,  # title для частей
                          shadow=1,  # Тень
                          startangle=90,  # Угол с которого будет начинаться первая доля
                          autopct='%1.1f%%'  # Указываем, что необходимо отобраджать проценты
                        )
                image_path = "temp/pie" + str(i) + ".png"
                i += 1

                plt.savefig(image_path)
                pdf.cell(0, 5, 'Анализ оценок, полученных за ' + row[0] + ' год.', ln=1)
                pdf.cell(0, 5, '', ln=1)
                pdf.cell(0, 5, 'Круговая диаграмма:', ln=1)
                pdf.cell(0, 5, '', ln=1)
                pdf.image(image_path, x=5, y=y, w=100)
                y += 100
                flag_pie += 1
                fig.clf()


        except:
            pass

        pdf.output(path_to_save_file)
