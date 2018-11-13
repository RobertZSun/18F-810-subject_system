#! C:\Users\Administrator\AppData\Local\Programs\Python\Python37
# -*- coding: utf-8 -*-
"""
Created  on Monday Oct 16 14:09:00 2018

@author: zhe sun

This file including there parts, Part 1: Date Arithmetic
                                 Part 2: Field separated file reader
                                 Part 3: Scanning directories and files
"""
import unittest
import datetime
import os
import re
from prettytable import PrettyTable


class Homework08Test(unittest.TestCase):

    def test_file_reader(self):
        path1 = "C:/Users/Administrator/Desktop/810/test.txt"
        path2 = "C:/Users/Administrator/Desktop/810/test1.txt"
        path3 = "C:/Users/Administrator/Desktop/810/test2.txt"
        self.assertEqual(list(file_reader(path1, 3, header=True)),
                         [('Noah', '32631502', 'Sociology'),
                          ('Liam', '63958924', 'Demography'),
                          ('Sophia', '98861293', 'International Trade'),
                          ('Mike', '84859752', 'Journalism')])
        self.assertEqual(list(file_reader(path2, 3, sep='|', header=False)),
                         [('Emma', '31873107', 'Philosophy'),
                          ('Noah', '32631502', 'Sociology'),
                          ('Liam', '63958924', 'Demography'),
                          ('Sophia', '98861293', 'International Trade'),
                          ('Mike', '84859752', 'Journalism')])


def date_arithmetic():
    """ This function uses python's datetime module to
        answer the following questions:
        1.1 What is the date three days after Feb 27, 2000?
        1.2 What is the date three days after Feb 27, 2017?
        1.3 How many days passed between Jan 1, 2017 and Oct 31, 2017?"""

    """ process 1.1 three days after Feb 27, 2000 """
    print("1.1 What is the date three days after Feb 27, 2000?")
    date1 = "Feb 27, 2000"
    dt1 = datetime.datetime.strptime(date1, '%b %d, %Y')
    num_days = 3
    dt11 = dt1 + datetime.timedelta(days=num_days)
    print(f"{num_days} days after {date1} is {dt11.strftime('%b %d, %Y')}")

    """ process 1.2 What is the date three days after Feb 27, 2017 """
    print("1.2 What is the date three days after Feb 27, 2017?")
    date2 = "Feb 27, 2017"
    dt2 = datetime.datetime.strptime(date2, '%b %d, %Y')
    num_days2 = 3
    dt22 = dt2 + datetime.timedelta(days=num_days2)
    print(f"{num_days2} days after {date2} is {dt22.strftime('%b %d, %Y')}")

    """process1.3 How many days passed between Jan 1, 2017 and Oct 31, 2017?"""
    print("1.3 How many days passed between Jan 1, 2017 and Oct 31, 2017?")
    date3 = "Jan 11, 2017"
    date4 = "Oct 31, 2017"
    dt3 = datetime.datetime.strptime(date3, '%b %d, %Y')
    dt4 = datetime.datetime.strptime(date4, '%b %d, %Y')
    delta = dt4 - dt3
    print(f"{delta.days} days passed between Jan 1, 2017 and Oct 31, 2017")


def file_reader(path, num, sep=',', header=False):
    """ This function is a generator read text files
        and return all of the values on a single line
        on each call to next().
    """
    try:
        fp = open(path, 'r', encoding='utf-8')
    except FileNotFoundError as error:
        raise error("Can't open ", path)    # what if not able to open
    else:
        with fp:
            # check if this is an empty file
            if os.path.getsize(path) == 0:
                print("The file is empty, try to reload another file")
            else:
                lines = 0
                for line in fp:
                    line = line.rstrip("\n\r")
                    words = line.split(sep)
                    lines += 1
                    # if the parameter header is True, then skip the first line
                    if header is True and lines == 1:
                        continue
                    else:
                        if len(words) != num:
                            raise ValueError(f"ValueError: {path} "
                                             f"has {len(words)}"
                                             f" fields on line {lines}"
                                             f" but expected {num}")
                        yield tuple(words)


def def_valid(line):
    if re.match(r'^\s*def[\s][\_]*[\w]+([\_]*[\w]*)*[\(].*[\)][\:]$', line):
        return True
    else:
        return False


def class_valid(line):
    if line.startswith("class "):
        if re.match(r'^class[\s][A-Z][\w]*[\:]$', line):
            return True
        else:
            return False
    else:
        return False


def summary_file(path):
    # This function takes a directory name, searches that directory for Python
    # files. For each .py file, open each file and calculate a summary of the
    # file including:'File Name', 'Classes', 'Functions', 'Lines', 'Characters'
    py_files = [file_name for file_name in os.listdir(path)
                if file_name.endswith(".py")]
    pt = PrettyTable(field_names=['File Name', 'Classes',
                                  'Functions', 'Lines', 'Characters'])
    result_match = []  # set the result which helps to return
    for file_name in py_files:
        final_path = os.path.join(path, file_name)
        try:
            fp = open(final_path, 'r', encoding='utf-8')
        except FileNotFoundError as error:
            # what if not able to open
            raise error("Can't open ", final_path)
        else:
            with fp:
                classes, functions, lines, characters = 0, 0, 0, 0
                for line in fp:
                    lines += 1
                    if def_valid(line):
                        functions += 1
                    if class_valid(line):
                        classes += 1
                    characters += len(list(line))
                pt.add_row([final_path, classes, functions,
                            lines, characters])
                result_match.append([classes, functions, lines,
                                     characters])
    print(pt)
    return result_match


def main():
    date_arithmetic()
    unittest.main(exit=False, verbosity=2)


if __name__ == '__main__':
    main()
