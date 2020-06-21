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
import time
from random import randint

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from db.models import Discipline, Group, Student


def parser_moodle(address, login, password, session) -> int:
    # address = 'https://cp29191-wordpress-8.tw1.ru'
    # login = "molchanova"
    # password = "C*SG#MiE1"

    login_address = address + "/login/index.php"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    try:
        driver.get(login_address)
        username = driver.find_element_by_id('username')
        username.click()
        username.send_keys(login)
        password_ = driver.find_element_by_id("password")
        password_.click()
        password_.send_keys(password)
        submit = driver.find_element_by_id("loginbtn")
        submit.click()
        time.sleep(1)

        number_course = 0

        while number_course != -1:
            courses = driver.find_elements_by_class_name('list-group-item-action')
            flag = 0
            this_number_course = 0
            flag_number_course = 0
            for course in courses:
                if flag == 1 and this_number_course == number_course:

                    # Синхронизация дисциплин
                    c = course
                    c.click()
                    title = driver.title
                    name_course = title.split('Курс: ')[1]
                    d = Discipline()
                    discipline = d.all(session)

                    flag_d = 0
                    for d in discipline:
                        if d.name == name_course:
                            flag_d = 1
                            break
                    if not flag_d:
                        d.add(session, discipline)
                    driver.find_element_by_partial_link_text("Участники").click()
                    time.sleep(5)

                    # Синхронизация групп и студентов
                    i = 0
                    flag_e = 0
                    id_template = "user-index-participants-4_r"
                    while flag_e == 0:
                        try:
                            id = id_template + str(i)
                            tr = driver.find_element_by_id(id)
                            i += 1
                            name = tr.find_elements_by_class_name('c1')
                            name = name[0].text
                            role = tr.find_elements_by_class_name('c3')
                            role = role[0].text
                            group = tr.find_elements_by_class_name('c4')
                            group = group[0].text
                            if role == 'Студент':
                                g = Group()
                                g_names = g.show_name(session)
                                g_flag = 0
                                for g_name in g_names:
                                    if g_name == group:
                                        g_flag = 1
                                        break
                                if g_flag == 0:
                                    g.add(session, group, 'Информационная безопасность')

                                s = Student()
                                s_names = s.all(session, group)
                                s_flag = 0
                                for s_name in s_names:
                                    if s_name == name:
                                        s_flag = 1
                                        break
                                if s_flag == 0:
                                    record_book = randint(100000, 999999)
                                    s.add(session, name, record_book, group)
                        except:
                            flag_e = 1
                    driver.back()
                    time.sleep(3)
                    driver.back()
                    time.sleep(3)
                    number_course += 1
                    flag_number_course = 1
                    break

                elif flag == 1:
                    this_number_course += 1
                if course.text == "Личные файлы":
                    flag = 1
            if flag_number_course == 0:
                number_course = -1

        driver.close()
        return 0

    except:
        driver.close()
        return 1
