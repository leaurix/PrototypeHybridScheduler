import pandas as pd
from typing import List, Dict

class Dataset:
    def __init__(self, students, courses, rooms, instructors, timeslots):
        self.students = students
        self.courses = courses
        self.rooms = rooms
        self.instructors = instructors
        self.timeslots = timeslots


def load_dataset(student_file, course_file, room_file, instructor_file, timeslot_file):
    students = pd.read_csv(student_file)
    courses = pd.read_csv(course_file)
    rooms = pd.read_csv(room_file)
    instructors = pd.read_csv(instructor_file)
    timeslots = pd.read_csv(timeslot_file)

    return Dataset(students, courses, rooms, instructors, timeslots)