#! C:\Users\Administrator\AppData\Local\Programs\Python\Python37
# -*- coding: utf-8 -*-
"""
Created  on Wednesday Nev 7 14:09:00 2018

@author: zhe sun

This file including there parts, Part 1: class Student
                                 Part 2: class Instructor
                                 Part 3: class University
                                 Part 4: class Major
                                 Part 5：make prettytable of Part 1&2
"""
import os
import unittest
import sqlite3
from HW08_zhesun import file_reader
from prettytable import PrettyTable
from collections import defaultdict


class Homework09Test(unittest.TestCase):

    def test_PrintTables_test(self):

        stevens = University("C:\\Users\Administrator\Desktop\810",
                             ptables=True)
        sdetail = [tuple(student.returnlist())
                   for student in stevens._students.values()]
        idetail = {tuple(row) for instructor in stevens._instructors.values()
                   for row in instructor.returnlist()}
        mdetail = [major.returnlist() for major in stevens._majors.values()]

        sresult = [('10103', 'Baldwin, C', 'SFEN', {'SSW 564', 'CS 501',
                                                    'SSW 687', 'SSW 567'},
                                           {'SSW 540', 'SSW 555'}, None),
                   ('10115', 'Wyatt, X', 'SFEN', {'SSW 564', 'SSW 687',
                                                  'CS 545', 'SSW 567'},
                    {'SSW 540', 'SSW 555'}, None),
                   ('10172', 'Forbes, I', 'SFEN', {'SSW 555', 'SSW 567'},
                    {'SSW 564', 'SSW 540'}, {'CS 545', 'CS 501', 'CS 513'}),
                   ('10175', 'Erickson, D', 'SFEN', {'SSW 564', 'SSW 687',
                                                     'SSW 567'},
                    {'SSW 540', 'SSW 555'}, {'CS 545', 'CS 501', 'CS 513'}),
                   ('10183', 'Chapman, O', 'SFEN', {'SSW 689'},
                    {'SSW 564', 'SSW 540', 'SSW 555', 'SSW 567'},
                    {'CS 545', 'CS 501', 'CS 513'}),
                   ('11399', 'Cordova, I', 'SYEN', {'SSW 540'},
                    {'SYS 800', 'SYS 671', 'SYS 612'}, None),
                   ('11461', 'Wright, U', 'SYEN',
                    {'SYS 800', 'SYS 750', 'SYS 611'}, {'SYS 671', 'SYS 612'},
                    {'SSW 540', 'SSW 565', 'SSW 810'}),
                   ('11658', 'Kelly, P', 'SYEN', None,
                    {'SYS 800', 'SYS 671', 'SYS 612'},
                    {'SSW 540', 'SSW 565', 'SSW 810'}),
                   ('11714', 'Morton, A', 'SYEN', {'SYS 645', 'SYS 611'},
                    {'SYS 800', 'SYS 671', 'SYS 612'},
                    {'SSW 540', 'SSW 565', 'SSW 810'}),
                   ('11788', 'Fuller, E', 'SYEN', {'SSW 540'},
                    {'SYS 800', 'SYS 671', 'SYS 612'}, None)]

        mresult = [['SFEN', {'SSW 567', 'SSW 564', 'SSW 540', 'SSW 555'},
                    {'CS 501', 'CS 545', 'CS 513'}],
                   ['SYEN', {'SYS 800', 'SYS 671', 'SYS 612'},
                    {'SSW 565', 'SSW 810', 'SSW 540'}]]

        iresult = {('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                   ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                   ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                   ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                   ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                   ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                   ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                   ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                   ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                   ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                   ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                   ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)}

        self.assertEqual(sdetail, sresult)
        self.assertEqual(idetail, iresult)


class Student:
    pt_labels = ["CWID", "Name", "Major", "Completed Courses",
                 "Remaining Required", "Remaining Electives"]

    def __init__(self, cwid, name, major, class_major):
        self._cwid = cwid
        self._name = name
        self._major = major
        self._class_major = class_major

        self._courses = defaultdict(str)  # _courses[course] = grade
        self._remaining_req = set()
        self._remaining_ele = set()

    def add_course(self, course, grade=""):
        """ student earns grade in course """
        self._courses[course] = grade

    def __str__(self):
        return (f"StudentID: {self._cwid} Name: {self._name}"
                f" Major: {self._major} Courses: "
                f"{sorted(self._courses.keys())}")

    def returnlist(self):
        """return a list of values to populate the prettytable
           for this student """
        completed_courses, remain_required, remain_electives \
            = self._class_major.grade_check(self._courses)
        return [self._cwid, self._name, self._major,
                completed_courses, remain_required, remain_electives]


class Major:
    pt_labels = ["Dept", "Required Courses", "Electives Courses"]

    def __init__(self, dept, passed_grades=None):
        self._dept = dept
        # _electives = {"SSW 810", "SSW 690", "SSW 564"}
        self._required = set()
        # _electives = {"SSW 810", "SSW 690", "SSW 564"}
        self._electives = set()
        if passed_grades is None:
            self._pass_grades = {'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        else:
            self._pass_grades = set(passed_grades)

    def add_course(self, flag, course):
        """ addd courses from the file majors.txt"""
        if flag == 'R':
            self._required.add(course)  # add course to required courses list
        elif flag == 'E':
            self._electives.add(course)  # add course to elective courses list
        else:
            raise ValueError(
                f"This {flag} {course} is not our expected course")

    def grade_check(self, courses):
        """ to calculate completed_courses, remain_required, remain_electives
            from a dict[course] = grade from a class Student instance
        """
        completed_courses = {
            course for course, grade in courses.items(
            ) if grade in self._pass_grades}
        remain_required = self._required - completed_courses
        if self._electives.intersection(completed_courses):
            remain_electives = None
        else:
            remain_electives = self._electives
        if completed_courses == set():
            completed_courses = None
        return completed_courses, remain_required, remain_electives

    def __str__(self):
        return (f"Dept: {self._dept} Required Courses: {self._required}"
                f" Electives Courses: {self._electives}")

    def returnlist(self):
        return [self._dept,
                self._required,
                self._electives]


class Instructor:
    pt_labels = ["CWID", "Name", "Dept", "Course", "Students"]

    def __init__(self, cwid, name, dept):
        self._cwid = cwid
        self._name = name
        self._dept = dept

        # _classes[course] = number of students
        self._classes = defaultdict(int)

    def add_classes(self, course):
        """ add number of student to the course """
        self._classes[course] += 1

    def returnlist(self):
        ilist = [[self._cwid, self._name, self._dept, key, value]
                 for key, value in self._classes.items()]
        return ilist

    def __str__(self):
        return (f"Instructor: {self._cwid} Name: {self._name}"
                f" Dept: {self._dept}")


class University:

    def __init__(self, path_dir, ptables=True):
        self._path_dir = path_dir  # directory of all the files to be read
        self._students = dict()  # key: cwid value: class Student
        self._instructors = dict()  # key: cwid value: class Instructor
        self._grades = list()
        self._majors = dict()  # key: name of the major value: class Major

        self._read_majors(os.path.join(path_dir, "majors.txt"))
        self._read_students(os.path.join(path_dir, "students.txt"))
        self._read_instructors(os.path.join(path_dir, "instructors.txt"))
        self._read_grades(os.path.join(path_dir, "grades.txt"))

        if ptables:
            print("\nMajor Summary")
            self.major_prettytable()

            print("\nStudent Summary")
            self.student_prettytable()

            print("\nInstructor Summary")
            self.instructor_prettytable()

    def _read_majors(self, path):
        """ read the majors files and store
            the data in self._majors """
        try:
            for major, flag, course in file_reader(path, 3,
                                                   sep='\t', header=False):
                if major not in self._majors:
                    self._majors[major] = Major(major)
                self._majors[major].add_course(flag, course)
        except ValueError as error:
            print(error)

    def _read_instructors(self, path):
        """ read the instructors files and
            store the data in self._instructors """
        try:
            for cwid, name, dept in file_reader(path,
                                                3, sep='\t', header=False):
                if cwid in self._instructors:
                    print(
                        f"Warning: cwid {cwid} already read from the file")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as error:
            print(error)

    def _read_students(self, path):
        """ read the students files and store
            the data in self._students """
        try:
            for cwid, name, major in file_reader(path, 3,
                                                 sep='\t', header=False):
                if cwid in self._students:
                    print(
                        f"Warning: cwid {cwid} already read from the file")
                else:
                    self._students[cwid] = Student(
                        cwid, name, major, self._majors[major])
        except ValueError as error:
            print(error)

    def _read_grades(self, path):
        """ read the grades file with student_cwid, course, grade,
            instructor_cwid tell student about the course and grade
            tell instructor about a new course and student
        """
        for student_cwid, course, grade, instructor_cwid in (
                file_reader(path, 4, sep='\t', header=False)):
            if student_cwid in self._students:
                # tell the student about a new course and grade
                self._students[student_cwid].add_course(course, grade)
            else:
                print(f"Warning : student_cwid {cwid} is "
                      "not in the student file")

            # tell instructor about teaching one more student this course
            if instructor_cwid in self._instructors:
                # tell the student about a new course and grade
                self._instructors[instructor_cwid].add_classes(course)
            else:
                print(f"Warning: instructor cwid {instructor_cwid}"
                      " is not in the instructor file")

    def major_prettytable(self):
        pt = PrettyTable(field_names=Major.pt_labels)
        for major in self._majors.values():
            pt.add_row(major.returnlist())
        print(pt)

    def student_prettytable(self):
        pt = PrettyTable(field_names=Student.pt_labels)
        for student in self._students.values():
            pt.add_row(student.returnlist())
        # sdetail = [tuple(student.returnlist())
        #            for student in self._students.values()]
        # print(f"sdetail: {sdetail}")
        print(pt)

    def instructor_prettytable(self):
        """ adjusted instructor prettytable"""
        pt = PrettyTable(field_names=Instructor.pt_labels)
        DB_FILE1 = "C:/Users/Administrator/Desktop/Week11_810/810_startup.db"
        query6 = "select Ins_ID, Name, Dept, Course as course_taught, count(*)\
              as the_num_of_stu from grades join instructors on \
              instructors.Ins_ID = grades.Instructor_CWID group by Course"
        db = sqlite3.connect(DB_FILE1)
        for line in [row for row in db.execute(query6)]:
            pt.add_row(line)
        print(pt)


def sql_exe(db_file_path, query_statement, query_label, title_number):
    """ execute the query statement under the path of database system
        and print the result in a pretty table """
    db = sqlite3.connect(db_file_path)
    print(f"{title_number} summary table: {query_statement}")
    pt = PrettyTable(field_names=query_label)
    for line in [row for row in db.execute(query_statement)]:
        pt.add_row(line)
    print(pt)


def main():
    unittest.main(exit=False, verbosity=2)

    university_path = "C:/Users/Administrator/Desktop/810"
    DB_FILE = "C:/Users/Administrator/Desktop/Week11_810/810_startup.db"

    query1 = "select Name from students where Stu_ID='11461'"
    query1_label = ["Name"]
    query2 = "select Major, count(*) as cnt from students group by Major"
    query2_label = ["Major", "cnt"]
    query3 = "select Grade, max(cnt) from (select Grade, count(*) as cnt \
              from grades group by Grade)"
    query3_label = ["Grade", "max(cnt)"]
    query4 = "select name, Stu_ID, Major, Course, Grade from grades join \
              students on grades.Student_CWID = students.Stu_ID"
    query4_label = ["Name", "Stu_ID", "Major", "Course", "Grade"]
    query5 = "select name from grades join students on \
              grades.Student_CWID = students.Stu_ID where Course = 'SSW 540'"
    query5_label = ["Name"]
    # query6 = "select Ins_ID, Name, Dept, Course as course_taught, count(*)\
    #           as the_num_of_stu from grades join instructors on \
    #           instructors.Ins_ID = grades.Instructor_CWID group by Course"
    # query6_label = ["Ins_ID", "Name", "Dept", "course_taught",
    #                 "the_num_of_stu"]

    stevens = University(university_path, ptables=True)

    sql_exe(DB_FILE, query1, query1_label, "4.1")
    sql_exe(DB_FILE, query2, query2_label, "4.2")
    sql_exe(DB_FILE, query3, query3_label, "4.3")
    sql_exe(DB_FILE, query4, query4_label, "4.4")
    sql_exe(DB_FILE, query5, query5_label, "4.5")
    # sql_exe(DB_FILE, query6, query6_label, "4.6")


if __name__ == '__main__':
    main()
