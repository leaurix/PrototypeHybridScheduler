import ast
import pandas as pd


class Dataset:
    def __init__(self, students, courses, rooms, instructors, timeslots):
        self.students = students
        self.courses = courses
        self.rooms = rooms
        self.instructors = instructors
        self.timeslots = timeslots


def _parse_timeslot_list(value):
    if pd.isna(value):
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
        except (ValueError, SyntaxError):
            pass
        return [x.strip() for x in value.split(",") if x.strip()]
    return []


def load_dataset(student_file, course_file, room_file, instructor_file, timeslot_file):
    students = pd.read_csv(student_file)
    courses = pd.read_csv(course_file)
    rooms = pd.read_csv(room_file)
    instructors = pd.read_csv(instructor_file)
    timeslots = pd.read_csv(timeslot_file)

    # Normalize required columns
    students.columns = [c.strip() for c in students.columns]
    courses.columns = [c.strip() for c in courses.columns]
    rooms.columns = [c.strip() for c in rooms.columns]
    instructors.columns = [c.strip() for c in instructors.columns]
    timeslots.columns = [c.strip() for c in timeslots.columns]

    if "prerequisite" not in courses.columns:
        courses["prerequisite"] = pd.NA

    if "available_timeslots" in instructors.columns:
        instructors["available_timeslots"] = instructors["available_timeslots"].apply(_parse_timeslot_list)
    else:
        instructors["available_timeslots"] = [[] for _ in range(len(instructors))]

    return Dataset(students, courses, rooms, instructors, timeslots)