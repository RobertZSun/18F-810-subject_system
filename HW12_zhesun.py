#! C:\Users\Administrator\AppData\Local\Programs\Python\Python37
# -*- coding: utf-8 -*-
"""
Created  on Wednesday Nev 21 14:09:00 2018

@author: Zhe Sun

This file including two parts, Part 1: main page
                               Part 2: Instructor_summary
In part 2, which create a table to present Instructor's CWID, Name,
Dept, course_taught, and the number of students in that course                                
"""

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def main():

    @app.route('/')
    def hello():
        return "Hello World! This is a Flask!"


    @app.route('/instructor_courses')
    def instructors_summary():
        query = "select Ins_ID, Name, Dept, Course as course_taught, count(*)\
                as the_num_of_stu from grades join instructors on \
                instructors.Ins_ID = grades.Instructor_CWID group by Course"

        DB_FILE = "C:/Users/Administrator/Desktop/810/810_startup.db"
        db = sqlite3.connect(DB_FILE)
        results = db.execute(query)

        instructors = [{'CWID': cwid, 'Name': name, 'Department': dept,
                        'Courses': courses, 'Students': students} for cwid, name,
                    dept, courses, students in results]
        db.close()
        return render_template('instructor_courses.html',
                            title='Stevens Repository',
                            table_title='Number of students by '
                                        'courses and instructor',
                            rows=instructors)


    app.run(debug=True)


if __name__ == '__main__':
    main()
