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
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.orm import relationship

from settings import YEAR
from transform.errors import bd_error

Base = declarative_base()


def get_user_password(session, login):
    user = session.query(Users).filter_by(login=login).first()

    try:
        return user

    except:
        return None


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)


class Discipline(Base):
    __tablename__ = 'discipline'
    id_discipline = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    @staticmethod
    def all(session):
        try:
            list_name = session.query(Discipline.name).order_by(Discipline.name).all()
            return list_name
        except Exception as e:
            session.rollback()
            print(str(e))

    @staticmethod
    def add(session, name):
        try:
            new_discipline = Discipline(name=name)
            session.add(new_discipline)
            session.flush()
        except Exception as e:
            session.rollback()
            print(str(e))


    @staticmethod
    def all_for_table(session):
        try:
            list_name = session.query(Discipline.name).order_by(Discipline.name).all()
            ls = []
            for i in list_name:
                ls1 = []
                ls1.append(i.name)
                ls.append(ls1)

            return ls
        except Exception as e:
            session.rollback()
            print(str(e))

    @staticmethod
    def show_name(session):
        try:
            list_all = session.query(Discipline).order_by(Discipline.name).all()
            ls_name = []
            for i in list_all:
                ls_name.append(i.name)

            return ls_name

        except Exception as e:
            session.rollback()
            print(str(e))


class Specialty(Base):
    __tablename__ = 'specialty'
    id_specialty = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=False)
    name = Column(String(255), nullable=False)

    @staticmethod
    def show_name(session):
        try:
            list_all = session.query(Specialty).all()
            ls_name = []
            for i in list_all:
                ls_name.append(i.name)

            return ls_name

        except Exception as e:
            session.rollback()
            print(str(e))


class Group(Base):
    __tablename__ = 'group_table'
    id_group = Column(Integer, primary_key=True)
    number = Column(String(100), nullable=False)
    id_specialty = Column(Integer, ForeignKey('specialty.id_specialty'), nullable=False, primary_key=True)
    specialty = relationship(Specialty, primaryjoin=id_specialty == Specialty.id_specialty, backref="p_specialty")

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.number, self.specialty.name)

    @staticmethod
    def show_name(session):
        try:
            list_all = session.query(Group).all()
            ls = []
            for i in list_all:
                ls.append(i.number)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def show_all(session):
        try:
            list = session.query(Group).join(Specialty).order_by(Specialty.name).all()
            ls = []
            for i in list:
                ls1 = []
                ls1.append(i.specialty.name)
                ls1.append(i.number)

                ls.append(ls1)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def add(session, number, specialty):
        try:
            s = session.query(Specialty).filter_by(name=specialty).first()
            id_specialty = s.id_specialty
            new_group = Group(number=number, id_specialty=id_specialty)
            session.add(new_group)
            session.flush()
        except Exception as e:
            bd_error()

    @staticmethod
    def update(session, old_number, number, specialty):
        try:
            s = session.query(Specialty).filter_by(name=specialty).first()
            id_specialty = s.id_specialty
            g = session.query(Group).filter_by(number=old_number)
            g.update({Group.number: number, Group.id_specialty: id_specialty})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def delete(session, number):
        try:
            s = session.query(Group).filter_by(number=number)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()


class Student(Base):
    __tablename__ = 'student'
    id_student = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    record_book = Column(Integer, nullable=False)
    id_group = Column(Integer, ForeignKey('group_table.id_group'), nullable=False, primary_key=True)
    group = relationship(Group, primaryjoin=id_group == Group.id_group, backref="parent_group")

    @staticmethod
    def all(session, group_number: str):
        try:
            student_list: list = session.query(Student).order_by(Student.name).all()
            ls: list = []
            for i in student_list:
                if i.group.number == group_number:
                    ls1: list = []
                    ls1.append(i.name)
                    ls1.append(i.record_book)

                    ls.append(ls1)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def all_name(session, group_number: str):
        try:
            s = session.query(Student).join(Group).filter(Group.number == group_number).order_by(Student.name).all()
            ls = []
            for i in s:
                ls.append(i.name)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def add(session, name, record_book, group_number):
        try:
            g = session.query(Group).filter_by(number=group_number).first()
            id_group = g.id_group
            new_student = Student(name=name, record_book=record_book, id_group=id_group)
            session.add(new_student)
            session.flush()

        except Exception as e:
            bd_error()

    @staticmethod
    def update(session, old_record_book, new_name, new_record_book):
        try:
            s = session.query(Student).filter_by(record_book=old_record_book)
            s.update({Student.record_book: new_record_book, Student.name: new_name})
            session.commit()

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def delete(session, record_book):
        try:
            s = session.query(Student).filter_by(record_book=record_book)
            s.delete()
            session.commit()

        except Exception as e:
            session.rollback()


class Work(Base):
    __tablename__ = 'work'
    id_work = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    deadline = Column(Date, nullable=False)
    id_group = Column(Integer, ForeignKey('group_table.id_group'), nullable=False, primary_key=True)
    group = relationship(Group, primaryjoin=id_group == Group.id_group, backref="parent_work_group")
    id_discipline = Column(Integer, ForeignKey('discipline.id_discipline'), nullable=False, primary_key=True)
    discipline = relationship(Discipline, primaryjoin=id_discipline == Discipline.id_discipline,
                              backref="parent_work_group")

    @staticmethod
    def show_name(session, group_number: str, discipline_name: str, flag_header=False):
        try:
            work_all: list = session.query(Work).join(Group).join(Discipline).filter(
                Group.number == group_number).filter(
                Discipline.name == discipline_name).order_by(Work.id_work).all()

            work_count: int = len(work_all)

            if flag_header:
                ls = []
                ls.append('ФИО студента')
            else:
                ls = []

            # Заполняем шапку таблицы
            for i in range(work_count):
                ls.append(work_all[i].name)
                if flag_header:
                    ls.append('Дата защиты')
            return ls

        except Exception as e:
            session.rollback()
            bd_error()


class Grade(Base):
    __tablename__ = 'grade'
    id_grade = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    id_work = Column(Integer, ForeignKey('work.id_work'), nullable=False, primary_key=True)
    work = relationship(Work, primaryjoin=id_work == Work.id_work, backref="parent_grade_work")
    id_student = Column(Integer, ForeignKey('student.id_student'), nullable=False, primary_key=True)
    student = relationship(Student, primaryjoin=id_student == Student.id_student, backref="parent_grade_student")

    def all(self, session, discipline, group_number):
        try:
            student_all: list = session.query(Student).join(Group).filter(Group.number == group_number).order_by(
                Student.name).all()

            work_all: list = session.query(Work).join(Group).join(Discipline).filter(
                Group.number == group_number).filter(Discipline.name == discipline).order_by(Work.id_work).all()

            ls = []

            for i in student_all:
                row = []
                row.append(i.name)

                for j in work_all:
                    grade = session.query(Grade).join(Student).join(Work). \
                        filter(Student.id_student == i.id_student).filter(Work.id_work == j.id_work).first()

                    if grade:
                        row.append(str(grade.value))
                        row.append(str(grade.date))
                    else:
                        row.append('')
                        row.append('')

                ls.append(row)

            ls = np.array(ls)

            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    def lagging_students(self, session):
        try:
            final_grade_all = session.query(FinalGrade).join(SessionType).filter(SessionType.id_session_type == 2).all()
            ls = []
            for final_grade in final_grade_all:
                if final_grade.date.year == YEAR:
                    ls.append(final_grade)

            result = []
            for final_grade in ls:
                discipline_name = final_grade.discipline.name
                group_number = final_grade.group.number
                grade_all = self.all(session, discipline_name, group_number)

                work = Work()
                table_header: list = work.show_name(session, group_number, discipline_name, flag_header=True)

                flag = 0

                for grade in grade_all:
                    row = []
                    row.append(grade[0])
                    row.append(group_number)
                    row.append(discipline_name)
                    row.append('')
                    for g in range(1, len(grade), 2):
                        if grade[g] == '':
                            if row[3] == '':
                                row[3] = row[3] + table_header[g]
                            else:
                                row[3] = row[3] + ", " + table_header[g]
                            flag = 1
                    if flag:
                        result.append(row)
                    flag = 0

            result = np.array(result)
            return result
        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_student_average_rating(session, student, stud_session, period):
        try:
            ls = []
            average_value = 0
            year_begin = YEAR
            count = 0

            if period == "За последний год":
                period_all = 1
            elif period == 'За последние 2 года':
                period_all = 2
            elif period == 'За последние 3 года':
                period_all = 3
            else:
                period_all = 4

            average_all = []
            for i in range(period_all):
                average_all1 = []
                average_all1.append(str(year_begin))
                average_all1.append(average_value)
                average_all1.append(count)
                average_all.append(average_all1)
                year_begin -= 1

            student_grade_all = session.query(Grade).join(Student).filter(Student.name == student). \
                order_by(Grade.date).all()

            for j in average_all:
                for i in student_grade_all:
                    if stud_session == "Все сессии" and i.date.month < 7 and int(j[0]) == i.date.year:
                        j[1] = j[1] + i.value
                        j[2] = j[2] + 1
                    elif stud_session == "Все сессии" and i.date.month > 7 and int(j[0]) - 1 == i.date.year:
                        j[1] = j[1] + i.value
                        j[2] = j[2] + 1
                    elif stud_session == "Летняя" and i.date.month < 7 and int(j[0]) == i.date.year:
                        j[1] = j[1] + i.value
                        j[2] = j[2] + 1
                    elif stud_session == "Зимняя" and i.date.month > 7 and int(j[0]) - 1 == i.date.year:
                        j[1] = j[1] + i.value
                        j[2] = j[2] + 1

            for j in average_all:
                if j[2] != 0:
                    ls1 = []
                    year = int(j[0])
                    year_value = str(year - 1) + '-' + str(year)
                    ls1.append(year_value)
                    value = j[1] / j[2]
                    value = round(value,2)
                    ls1.append(value)
                    ls.append(ls1)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_student_average_rating_discipline(session, group_number, discipline):
        try:
            ls = []
            average_value = 0
            count = 0

            student_list_all = session.query(Student).join(Group).filter(Group.number == group_number).\
                order_by(Student.name).all()
            student_grade_all = session.query(Grade).join(Student).join(Group).join(Work).join(Discipline).\
                filter(Group.number == group_number).filter(Discipline.name == discipline).all()

            for j in student_list_all:
                for i in student_grade_all:
                    if j.id_student == i.id_student:
                        average_value += i.value
                        count += 1

                ls1 = []
                value = average_value / count
                value = round(value, 2)
                ls1.append(j.name)
                ls1.append(value)
                ls.append(ls1)
                average_value = 0
                count = 0

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_student_rating_semester(session, student, stud_session, period, max: bool = True):
        try:
            ls = []
            average_value = 0
            year_begin = YEAR

            if period == "За последний год":
                period_all = 1
            elif period == 'За последние 2 года':
                period_all = 2
            elif period == 'За последние 3 года':
                period_all = 3
            else:
                period_all = 4

            average_all = []
            for i in range(period_all):
                average_all1 = []
                average_all1.append(str(year_begin))
                average_all1.append(average_value)
                average_all.append(average_all1)
                year_begin -= 1

            student_grade_all = session.query(Grade).join(Student).filter(Student.name == student). \
                order_by(Grade.date).all()

            for j in average_all:
                for i in student_grade_all:
                    if stud_session == "Все сессии" and i.date.month < 7 and int(j[0]) == i.date.year:
                        if j[1] == 0:
                            j[1] = i.value
                        elif j[1] < i.value and max is True:
                            j[1] = i.value
                        elif j[1] > i.value and max is False:
                            j[1] = i.value
                    elif stud_session == "Все сессии" and i.date.month > 7 and int(j[0]) - 1 == i.date.year:
                        if j[1] == 0:
                            j[1] = i.value
                        elif j[1] < i.value and max is True:
                            j[1] = i.value
                        elif j[1] > i.value and max is False:
                            j[1] = i.value
                    elif stud_session == "Летняя" and i.date.month < 7 and int(j[0]) == i.date.year:
                        if j[1] == 0:
                            j[1] = i.value
                        elif j[1] < i.value and max is True:
                            j[1] = i.value
                        elif j[1] > i.value and max is False:
                            j[1] = i.value
                    elif stud_session == "Зимняя" and i.date.month > 7 and int(j[0]) - 1 == i.date.year:
                        if j[1] == 0:
                            j[1] = i.value
                        elif j[1] < i.value and max is True:
                            j[1] = i.value
                        elif j[1] > i.value and max is False:
                            j[1] = i.value

            for j in average_all:
                ls1 = []
                year = int(j[0])
                year_value = str(year - 1) + '-' + str(year)
                ls1.append(year_value)
                value = j[1]
                ls1.append(value)
                ls.append(ls1)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_student_rating_semester_discipline(session, group_number, discipline, max: bool=True):
        try:
            ls: list = []
            maxmin: int = 0

            student_list_all = session.query(Student).join(Group).filter(Group.number == group_number). \
                order_by(Student.name).all()
            student_grade_all = session.query(Grade).join(Student).join(Group).join(Work).join(Discipline). \
                filter(Group.number == group_number).filter(Discipline.name == discipline).all()

            for j in student_list_all:
                for i in student_grade_all:
                    if j.id_student == i.id_student:
                        if maxmin == 0:
                            maxmin: int = i.value
                        elif maxmin < i.value and max is True:
                            maxmin: int = i.value
                        elif maxmin > i.value and max is False:
                            maxmin: int = i.value

                ls1 = []
                value = maxmin
                value = round(value, 2)
                ls1.append(j.name)
                ls1.append(value)
                ls.append(ls1)
                maxmin = 0

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_student_number_works(session, student, stud_session, period):
        try:
            ls = []
            count_work = 0
            year_begin = YEAR
            count_works = 0

            if period == "За последний год":
                period_all = 1
            elif period == 'За последние 2 года':
                period_all = 2
            elif period == 'За последние 3 года':
                period_all = 3
            else:
                period_all = 4

            average_all = []
            for i in range(period_all):
                average_all1 = []
                average_all1.append(str(year_begin))
                average_all1.append(count_work)
                average_all1.append(count_works)
                average_all.append(average_all1)
                year_begin -= 1

            student_grade_all = session.query(Grade).join(Student).filter(Student.name == student). \
                order_by(Grade.date).all()

            for j in average_all:
                for i in student_grade_all:
                    if stud_session == "Все сессии" and i.date.month < 7 and int(j[0]) == i.date.year:
                        if i.value >= 25:
                            j[1] = j[1] + 1
                        j[2] = j[2] + 1
                    elif stud_session == "Все сессии" and i.date.month > 7 and int(j[0]) - 1 == i.date.year:
                        if i.value >= 25:
                            j[1] = j[1] + 1
                        j[2] = j[2] + 1
                    elif stud_session == "Летняя" and i.date.month < 7 and int(j[0]) == i.date.year:
                        if i.value >= 25:
                            j[1] = j[1] + 1
                        j[2] = j[2] + 1
                    elif stud_session == "Зимняя" and i.date.month > 7 and int(j[0]) - 1 == i.date.year:
                        if i.value >= 25:
                            j[1] = j[1] + 1
                        j[2] = j[2] + 1

            for j in average_all:
                ls1 = []
                year = int(j[0])
                year_value = str(year - 1) + '-' + str(year)
                ls1.append(year_value)
                value = j[1]
                ls1.append(value)
                value = j[2]
                ls1.append(value)
                ls.append(ls1)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_student_number_works_discipline(session, group_number, discipline):
        try:
            ls: list = []
            work: int = 0
            works: int = 0

            student_list_all = session.query(Student).join(Group).filter(Group.number == group_number). \
                order_by(Student.name).all()
            student_grade_all = session.query(Grade).join(Student).join(Group).join(Work).join(Discipline). \
                filter(Group.number == group_number).filter(Discipline.name == discipline).all()

            for j in student_list_all:
                for i in student_grade_all:
                    if j.id_student == i.id_student:
                        if i.value >= 25:
                            work += 1
                        works += 1

                ls1 = []
                ls1.append(j.name)
                ls1.append(work)
                ls1.append(works)
                ls.append(ls1)
                work = 0
                works = 0

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    # Анализ по дисциплинам по группам средняя оценка за семестр
    @staticmethod
    def analysis_group_average_rating_discipline(session, discipline):
        try:
            ls: list = []
            average_value: int = 0
            count: int = 0

            group_list = session.query(Group).all()
            student_grade_all = session.query(Grade).join(Student).join(Group).join(Work).join(Discipline).\
                filter(Discipline.name == discipline).all()

            for i in group_list:
                for j in student_grade_all:
                    if i.id_group == j.work.id_group:
                        average_value += j.value
                        count += 1
                if count != 0:
                    ls1 = []
                    value = average_value / count
                    value = round(value, 2)
                    ls1.append(i.number)
                    ls1.append(value)
                    ls.append(ls1)
                    average_value = 0
                    count = 0

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    # Анализ по дисциплинам по группам maxmin за семестр
    @staticmethod
    def analysis_group_rating_semester_discipline(session, discipline, max:bool=True):
        try:
            ls: list = []
            maxmin: int = 0

            group_list = session.query(Group).all()
            student_grade_all = session.query(Grade).join(Student).join(Group).join(Work).join(Discipline).\
                filter(Discipline.name == discipline).all()

            for i in group_list:
                for j in student_grade_all:
                    if i.id_group == j.work.id_group:
                        if maxmin == 0:
                            maxmin: int = j.value
                        elif maxmin < j.value and max is True:
                            maxmin: int = j.value
                        elif maxmin > j.value and max is False:
                            maxmin: int = j.value

                if maxmin != 0:
                    ls1 = []
                    ls1.append(i.number)
                    ls1.append(maxmin)
                    ls.append(ls1)
                    maxmin = 0

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

class SessionType(Base):
    __tablename__ = 'session_type'
    id_session_type = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


class TypeFinalGrade(Base):
    __tablename__ = 'type_final_grade'
    id_type_final_grade = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


class FinalGrade(Base):
    __tablename__ = 'final_grade'
    id_final_grade = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    id_type_final_grade = Column(Integer, ForeignKey('type_final_grade.id_type_final_grade'), nullable=False,
                                 primary_key=True)
    type_final_grade = relationship(TypeFinalGrade,
                                    primaryjoin=id_type_final_grade == TypeFinalGrade.id_type_final_grade,
                                    backref="parent_TypeFinalGrade_FinalGrade")
    id_session_type = Column(Integer, ForeignKey('session_type.id_session_type'), nullable=False, primary_key=True)
    session_type = relationship(SessionType, primaryjoin=id_session_type == SessionType.id_session_type,
                                backref="parent_SesstionType_FinalGrade")
    id_discipline = Column(Integer, ForeignKey('discipline.id_discipline'), nullable=False, primary_key=True)
    discipline = relationship(Discipline, primaryjoin=id_discipline == Discipline.id_discipline,
                              backref="parent_discipline_FinalGrade")
    id_group = Column(Integer, ForeignKey('group_table.id_group'), nullable=False, primary_key=True)
    group = relationship(Group, primaryjoin=id_group == Group.id_group, backref="parent_group_FinalGrade")


class Control(Base):
    __tablename__ = 'control'
    id_control = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    value = Column(Integer, nullable=False)
    set_off = Column(Boolean)
    id_final_grade = Column(Integer, ForeignKey('final_grade.id_final_grade'), nullable=False, primary_key=True)
    final_grade = relationship(FinalGrade, primaryjoin=id_final_grade == FinalGrade.id_final_grade,
                               backref="parent_FinalGrade_Control")
    id_student = Column(Integer, ForeignKey('student.id_student'), nullable=False, primary_key=True)
    student = relationship(Student, primaryjoin=id_student == Student.id_student, backref="parent_SesstionType_Control")

    @staticmethod
    def analysis_student_average_rating(session, student, stud_session, period):
        try:
            if stud_session == 'Все сессии':
                student_control_all = session.query(Control).join(Student).filter(Student.name == student). \
                    order_by(Control.date).all()
            else:
                student_control_all = session.query(Control).join(Student).join(FinalGrade).join(SessionType).filter(
                    Student.name == student). \
                    filter(SessionType.name == stud_session).order_by(Control.date).all()

            ls = []
            average_value = 0
            year_begin = YEAR
            count = 0

            if period == "За последний год":
                period_all = 1
            elif period == 'За последние 2 года':
                period_all = 2
            elif period == 'За последние 3 года':
                period_all = 3
            else:
                period_all = 4

            average_all = []
            for i in range(period_all):
                average_all1 = []
                average_all1.append(str(year_begin))
                average_all1.append(average_value)
                average_all1.append(count)
                average_all.append(average_all1)
                year_begin -= 1

            for j in average_all:
                for i in student_control_all:
                    if i.final_grade.type_final_grade.name == 'Экзамен':
                        if int(j[0]) == i.date.year:
                            j[1] = j[1] + i.value
                            j[2] = j[2] + 1

            for j in average_all:
                if j[2] != 0:
                    ls1 = []
                    year = int(j[0])
                    year_value = str(year - 1) + '-' + str(year)
                    ls1.append(year_value)
                    value = j[1] / j[2]
                    ls1.append(value)
                    ls.append(ls1)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_student_average_rating_discipline(session, group_number, discipline):
        try:
            student_list_all = session.query(Student).join(Group).filter(Group.number == group_number). \
                order_by(Student.name).all()
            discipline = session.query(Discipline).filter_by(name=discipline).first()
            id_discipline = discipline.id_discipline
            student_control_all = session.query(Control).join(Student).join(Group).join(FinalGrade).join(Discipline). \
                filter(Group.number == group_number).all()

            ls = []

            for i in student_list_all:
                for j in student_control_all:
                    if i.id_student == j.id_student and id_discipline == j.final_grade.id_discipline:
                        ls1 = []
                        ls1.append(i.name)
                        ls1.append(j.value)
                        ls.append(ls1)
                        break

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_student_proportional(session, student, stud_session, period):
        try:
            if stud_session == 'Все сессии':
                student_control_all = session.query(Control).join(Student). \
                    filter(Student.name == student).all()
            else:
                student_control_all = session.query(Control).join(Student).join(FinalGrade).join(SessionType). \
                    filter(Student.name == student).filter(SessionType.name == stud_session).all()

            ls = []
            year_begin = YEAR
            count = 0

            if period == "За последний год":
                period_all = 1
            elif period == 'За последние 2 года':
                period_all = 2
            elif period == 'За последние 3 года':
                period_all = 3
            else:
                period_all = 4

            average_all = []
            for i in range(period_all):
                average_all1 = []
                average_all1.append(str(year_begin))
                average_all1.append(count)
                average_all1.append(count)
                average_all1.append(count)
                average_all1.append(count)
                average_all.append(average_all1)
                year_begin -= 1

            for j in average_all:
                for i in student_control_all:
                    if i.final_grade.type_final_grade.name == 'Экзамен':
                        if int(j[0]) == i.date.year:
                            if i.value < 25:
                                j[1] = j[1] + 1
                            elif 25 <= i.value < 50:
                                j[2] = j[2] + 1
                            elif 50 <= i.value < 75:
                                j[3] = j[3] + 1
                            else:
                                j[4] = j[4] + 1

            for j in average_all:
                ls1 = []
                year = int(j[0])
                year_value = str(year - 1) + '-' + str(year)
                ls1.append(year_value)
                value = j[1]
                ls1.append(value)
                value = j[2]
                ls1.append(value)
                value = j[3]
                ls1.append(value)
                value = j[4]
                ls1.append(value)
                ls.append(ls1)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    # Максимальная/минимальная оценка по итогам сессии
    @staticmethod
    def analysis_student_rating(session, student, stud_session, period, max: bool = True):
        try:
            if stud_session == 'Все сессии':
                student_control_all = session.query(Control).join(Student).filter(Student.name == student). \
                    order_by(Control.date).all()
            else:
                student_control_all = session.query(Control).join(Student).join(FinalGrade).join(SessionType).filter(
                    Student.name == student). \
                    filter(SessionType.name == stud_session).order_by(Control.date).all()

            ls = []
            average_value = 0
            year_begin = YEAR

            if period == "За последний год":
                period_all = 1
            elif period == 'За последние 2 года':
                period_all = 2
            elif period == 'За последние 3 года':
                period_all = 3
            else:
                period_all = 4

            average_all = []
            for i in range(period_all):
                average_all1 = []
                average_all1.append(str(year_begin))
                average_all1.append(average_value)
                average_all.append(average_all1)
                year_begin -= 1

            for j in average_all:
                for i in student_control_all:
                    if i.final_grade.type_final_grade.name == 'Экзамен':
                        if int(j[0]) == i.date.year:
                            if j[1] == 0:
                                j[1] = i.value
                            elif j[1] < i.value and max is True:
                                j[1] = i.value
                            elif j[1] > i.value and max is False:
                                j[1] = i.value

            for j in average_all:
                if j[1] != 0:
                    ls1 = []
                    year = int(j[0])
                    year_value = str(year - 1) + '-' + str(year)
                    ls1.append(year_value)
                    ls1.append(j[1])
                    ls.append(ls1)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_group(session, group, stud_session, period):
        try:
            if stud_session == 'Все сессии':
                student_control_all = session.query(Control).join(Student).join(Group).join(FinalGrade). \
                    filter(Group.number == group).all()
            else:
                student_control_all = session.query(Control).join(Student).join(Group).join(FinalGrade).join(
                    SessionType). \
                    filter(Group.number == group).filter(SessionType.name == stud_session).all()

            ls = []
            average_value = 0
            year_begin = YEAR
            count = 0

            if period == "За последний год":
                period_all = 1
            elif period == 'За последние 2 года':
                period_all = 2
            elif period == 'За последние 3 года':
                period_all = 3
            else:
                period_all = 4

            average_all = []
            for i in range(period_all):
                average_all1 = []
                average_all1.append(str(year_begin))
                average_all1.append(average_value)
                average_all1.append(count)
                average_all.append(average_all1)
                year_begin -= 1

            for j in average_all:
                for i in student_control_all:
                    if i.final_grade.type_final_grade.name == 'Экзамен':
                        if int(j[0]) == i.date.year:
                            j[1] = j[1] + i.value
                            j[2] = j[2] + 1

            for j in average_all:
                if j[2] != 0:
                    ls1 = []
                    year = int(j[0])
                    year_value = str(year - 1) + '-' + str(year)
                    ls1.append(year_value)
                    value = j[1] / j[2]
                    value = round(value, 2)
                    ls1.append(value)
                    ls.append(ls1)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_group_proportional(session, group, stud_session, period):
        try:
            if stud_session == 'Все сессии':
                student_control_all = session.query(Control).join(Student).join(Group).join(FinalGrade). \
                    filter(Group.number == group).all()
            else:
                student_control_all = session.query(Control).join(Student).join(Group).join(FinalGrade).join(
                    SessionType). \
                    filter(Group.number == group).filter(SessionType.name == stud_session).all()

            ls = []
            year_begin = YEAR
            count = 0

            if period == "За последний год":
                period_all = 1
            elif period == 'За последние 2 года':
                period_all = 2
            elif period == 'За последние 3 года':
                period_all = 3
            else:
                period_all = 4

            average_all = []
            for i in range(period_all):
                average_all1 = []
                average_all1.append(str(year_begin))
                average_all1.append(count)
                average_all1.append(count)
                average_all1.append(count)
                average_all1.append(count)
                average_all.append(average_all1)
                year_begin -= 1

            for j in average_all:
                for i in student_control_all:
                    if i.final_grade.type_final_grade.name == 'Экзамен':
                        if int(j[0]) == i.date.year:
                            if i.value < 25:
                                j[1] = j[1] + 1
                            elif 25 <= i.value < 50:
                                j[2] = j[2] + 1
                            elif 50 <= i.value < 75:
                                j[3] = j[3] + 1
                            else:
                                j[4] = j[4] + 1

            for j in average_all:
                ls1 = []
                year = int(j[0])
                year_value = str(year - 1) + '-' + str(year)
                ls1.append(year_value)
                value = j[1]
                ls1.append(value)
                value = j[2]
                ls1.append(value)
                value = j[3]
                ls1.append(value)
                value = j[4]
                ls1.append(value)
                ls.append(ls1)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_group_maximin(session, group, stud_session, period, max: bool=True):
        try:
            if stud_session == 'Все сессии':
                student_control_all = session.query(Control).join(Student).join(Group).join(FinalGrade). \
                    filter(Group.number == group).all()
            else:
                student_control_all = session.query(Control).join(Student).join(Group).join(FinalGrade).join(
                    SessionType). \
                    filter(Group.number == group).filter(SessionType.name == stud_session).all()

            ls = []
            average_value = 0
            year_begin = YEAR

            if period == "За последний год":
                period_all = 1
            elif period == 'За последние 2 года':
                period_all = 2
            elif period == 'За последние 3 года':
                period_all = 3
            else:
                period_all = 4

            average_all = []
            for i in range(period_all):
                average_all1 = []
                average_all1.append(str(year_begin))
                average_all1.append(average_value)
                average_all.append(average_all1)
                year_begin -= 1

            for j in average_all:
                for i in student_control_all:
                    if i.final_grade.type_final_grade.name == 'Экзамен':
                        if int(j[0]) == i.date.year:
                            if j[1] == 0:
                                j[1] = i.value
                            elif j[1] < i.value and max is True:
                                j[1] = i.value
                            elif j[1] > i.value and max is False:
                                j[1] = i.value

            for j in average_all:
                if j[1] != 0:
                    ls1 = []
                    year = int(j[0])
                    year_value = str(year - 1) + '-' + str(year)
                    ls1.append(year_value)
                    ls1.append(j[1])
                    ls.append(ls1)

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_group_average_rating_discipline(session, discipline):
        try:
            group_list = session.query(Group).all()
            student_control_all = session.query(Control).join(Student).join(Group).join(FinalGrade).join(Discipline).\
                filter(Discipline.name == discipline).all()
            discipline = session.query(Discipline).filter_by(name=discipline).first()
            id_discipline = discipline.id_discipline

            ls = []
            average_value = 0
            count = 0

            for i in group_list:
                for j in student_control_all:
                    if i.id_group == j.final_grade.id_group and id_discipline == j.final_grade.id_discipline:
                        average_value += j.value
                        count += 1
                if count != 0:
                    ls1 = []
                    ls1.append(i.number)
                    value = average_value / count
                    value = round(value, 2)
                    ls1.append(value)
                    ls.append(ls1)
                    average_value = 0
                    count = 0

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()

    @staticmethod
    def analysis_group_maxmin_discipline(session, discipline, max: bool =True):
        try:
            group_list = session.query(Group).all()
            student_control_all = session.query(Control).join(Student).join(Group).join(FinalGrade).join(Discipline).\
                filter(Discipline.name == discipline).all()
            discipline = session.query(Discipline).filter_by(name=discipline).first()
            id_discipline = discipline.id_discipline

            ls = []
            maxmin = 0

            for i in group_list:
                for j in student_control_all:
                    if i.id_group == j.final_grade.id_group and id_discipline == j.final_grade.id_discipline:
                        if maxmin == 0:
                            maxmin: int = j.value
                        elif maxmin < j.value and max is True:
                            maxmin: int = j.value
                        elif maxmin > j.value and max is False:
                            maxmin: int = j.value
                if maxmin !=0:
                    ls1 = []
                    ls1.append(i.number)
                    ls1.append(maxmin)
                    ls.append(ls1)
                    maxmin = 0

            ls = np.array(ls)
            return ls

        except Exception as e:
            session.rollback()
            bd_error()
