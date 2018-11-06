#! C:\Users\Administrator\AppData\Local\Programs\Python\Python37
# -*- coding: utf-8 -*-
"""
Created  on Wednesday Oct 31 14:09:00 2018

@author: zhe sun

This file including there parts, Part 1: class Student
                                 Part 2: class Instructor
                                 Part 3: class University
                                 Part 4：make prettytable of Part 1&2
"""

import os
import unittest
from HW08_zhesun import file_reader
from prettytable import PrettyTable
from collections import defaultdict


class Homework09Test(unittest.TestCase):

    def test_Student_test(self):

        stevens = University("C:\\Users\Administrator\Desktop\810self",
                             ptables=True)
        sdetail = {tuple(student.returnlist())
                   for student in stevens._students.values()}
        idetail = {tuple(row) for instructor in stevens._instructors.values()
                   for row in instructor.returnlist()}
        sresult = {('10103', 'Baldwin, C', 'SFEN', ('CS 501', 'SSW 564',
                                                    'SSW 567', 'SSW 687')),
                   ('10115', 'Wyatt, X', 'SFEN', (
                       'CS 545', 'SSW 564', 'SSW 567', 'SSW 687')),
                   ('10172', 'Forbes, I', 'SFEN', ('SSW 555', 'SSW 567')),
                   ('10175', 'Erickson, D', 'SFEN', (
                       'SSW 564', 'SSW 567', 'SSW 687')),
                   ('10183', 'Chapman, O', 'SFEN', ('SSW 689',)),
                   ('11399', 'Cordova, I', 'SYEN', ('SSW 540',)),
                   ('11461', 'Wright, U', 'SYEN', (
                       'SYS 611', 'SYS 750', 'SYS 800')),
                   ('11658', 'Kelly, P', 'SYEN', ('SSW 540',)),
                   ('11714', 'Morton, A', 'SYEN', ('SYS 611', 'SYS 645')),
                   ('11788', 'Fuller, E', 'SYEN', ('SSW 540',))}

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
    pt_labels = ["CWID", "Name", "Majo", "Completed Courses"]

    def __init__(self, cwid, name, major):
        self._cwid = cwid
        self._name = name
        self._major = major

        self._courses = defaultdict(str)  # _courses[course] = grade

    def add_course(self, course, grade=""):
        """ student earns grade in course """
        self._courses[course] = grade

    def __str__(self):
        return (f"StudentID: {self._cwid} Name: {self._name}"
                f" Major: {self._major} Courses: "
                f"{sorted(self._courses.keys())}")

    def returnlist(self):
        return [self._cwid,
                self._name,
                self._major,
                tuple(sorted(self._courses.keys()))]


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
        self._students = dict()
        self._instructors = dict()
        self._grades = list()

        self._read_students(os.path.join(path_dir, "students.txt"))
        self._read_instructors(os.path.join(path_dir, "instructors.txt"))
        self._read_grades(os.path.join(path_dir, "grades.txt"))

        if ptables:
            print("\nStudent Summary")
            self.student_prettytable()

            print("\nInstructor Summary")
            self.instructor_prettytable()

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
                    self._students[cwid] = Student(cwid, name, major)
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

    def student_prettytable(self):
        pt = PrettyTable(field_names=Student.pt_labels)
        for student in self._students.values():
            pt.add_row(student.returnlist())
        print(pt)

    def instructor_prettytable(self):
        pt = PrettyTable(field_names=Instructor.pt_labels)
        for instructor in self._instructors.values():
            for row in instructor.returnlist():
                pt.add_row(row)
        print(pt)


def main():
    unittest.main(exit=False, verbosity=2)
    stevens = University("C:\\Users\Administrator\Desktop\810self"
                         ptables=True)


if __name__ == '__main__':
    main()
