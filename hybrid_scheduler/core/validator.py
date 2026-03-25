from __future__ import annotations
from typing import Dict, Any
from hybrid_scheduler.utils.dataset_loader import Dataset


class Validator:
    """
    Thesis-aligned validator:
    - counts hard constraint violations
    - counts soft constraint violations
    - computes weighted score
    Lower score = better schedule
    """

    def __init__(self, dataset: Dataset):
        self.dataset = dataset

        # Aligned with thesis weights (adjust anytime if needed)
        self.weights = {
            "room_capacity": 10,
            "instructor_conflict": 10,
            "student_conflicts": 10,
            "room_time_uniqueness": 9,
            "prerequisite": 8,
            "instructor_availability": 7,
            "soft_balance": 4,
            "soft_room_preference": 3,
            "soft_instructor_preference": 2,
            "soft_section_preference": 1,
        }

        # Assign a room per course for simplified checking
        self.course_room_map = self._assign_default_rooms()

    def _assign_default_rooms(self):
        """
        Simplified room assignment:
        assigns each course a room in round-robin order.
        """
        rooms = list(self.dataset.rooms["room_id"])
        course_room = {}
        if not rooms:
            return course_room
        for idx, c in enumerate(self.dataset.courses["course_id"]):
            course_room[c] = rooms[idx % len(rooms)]
        return course_room

    def _course_instructor(self, course_id):
        row = self.dataset.courses[self.dataset.courses["course_id"] == course_id]
        if row.empty:
            return None
        return row.iloc[0]["instructor_id"]

    def _instructor_available(self, instructor_id):
        row = self.dataset.instructors[self.dataset.instructors["instructor_id"] == instructor_id]
        if row.empty:
            return []
        return row.iloc[0]["available_timeslots"]

    def _room_capacity(self, room_id):
        row = self.dataset.rooms[self.dataset.rooms["room_id"] == room_id]
        if row.empty:
            return 0
        return int(row.iloc[0]["capacity"])

    def _course_prerequisite(self, course_id):
        row = self.dataset.courses[self.dataset.courses["course_id"] == course_id]
        if row.empty:
            return None
        prereq = row.iloc[0]["prerequisite"]
        if str(prereq) == "nan" or prereq is None:
            return None
        return prereq

    def validate(self, schedule: Dict[Any, int]):
        """
        schedule: dict {(student_id, course_id, timeslot): 0/1}
        Returns a dictionary of violations + weighted score.
        """
        violations = {
            "hard": 0,
            "score": 0,
            "student_conflicts": 0,
            "room_capacity": 0,
            "instructor_conflict": 0,
            "room_time_uniqueness": 0,
            "prerequisite": 0,
            "instructor_availability": 0,
            "soft_balance": 0,
            "soft_room_preference": 0,
            "soft_instructor_preference": 0,
            "soft_section_preference": 0,
        }

        students = list(self.dataset.students["student_id"])
        courses = list(self.dataset.courses["course_id"])
        timeslots = list(self.dataset.timeslots["timeslot"])

        # -------------------------
        # HARD 1: Student conflicts
        # -------------------------
        for s in students:
            for t in timeslots:
                assigned = [
                    c for (s2, c, t2), v in schedule.items()
                    if s2 == s and t2 == t and v == 1
                ]
                if len(assigned) > 1:
                    violations["student_conflicts"] += (len(assigned) - 1)

        # -------------------------
        # HARD 2: Room capacity
        # -------------------------
        for c in courses:
            room_id = self.course_room_map.get(c)
            cap = self._room_capacity(room_id)
            for t in timeslots:
                enrolled = sum(schedule.get((s, c, t), 0) for s in students)
                if enrolled > cap:
                    violations["room_capacity"] += (enrolled - cap)

        # -------------------------
        # HARD 3: Instructor conflict
        # same instructor teaching >1 course at same timeslot
        # -------------------------
        for t in timeslots:
            instructor_courses = {}
            for c in courses:
                instructor = self._course_instructor(c)
                active = sum(schedule.get((s, c, t), 0) for s in students) > 0
                if active:
                    instructor_courses.setdefault(instructor, 0)
                    instructor_courses[instructor] += 1
            for instructor, count in instructor_courses.items():
                if count > 1:
                    violations["instructor_conflict"] += (count - 1)

        # -------------------------
        # HARD 4: Room-time uniqueness
        # one room cannot host multiple active courses at same timeslot
        # -------------------------
        for t in timeslots:
            room_usage = {}
            for c in courses:
                room_id = self.course_room_map.get(c)
                active = sum(schedule.get((s, c, t), 0) for s in students) > 0
                if active:
                    room_usage.setdefault(room_id, 0)
                    room_usage[room_id] += 1
            for room_id, count in room_usage.items():
                if count > 1:
                    violations["room_time_uniqueness"] += (count - 1)

        # -------------------------
        # HARD 5: Prerequisite
        # simplified: if student is assigned to course, prerequisite must also exist
        # somewhere in the schedule
        # -------------------------
        for s in students:
            student_courses = set()
            for (s2, c, t), v in schedule.items():
                if s2 == s and v == 1:
                    student_courses.add(c)

            for c in student_courses:
                prereq = self._course_prerequisite(c)
                if prereq and prereq not in student_courses:
                    violations["prerequisite"] += 1

        # -------------------------
        # HARD 6: Instructor availability
        # -------------------------
        for c in courses:
            instructor = self._course_instructor(c)
            available = self._instructor_available(instructor)
            for t in timeslots:
                active = sum(schedule.get((s, c, t), 0) for s in students) > 0
                if active and t not in available:
                    violations["instructor_availability"] += 1

        # -------------------------
        # SOFT 1: Balance
        # too many courses for a student overall
        # -------------------------
        for s in students:
            total_assigned = sum(
                v for (s2, c, t), v in schedule.items() if s2 == s and v == 1
            )
            if total_assigned > 5:
                violations["soft_balance"] += (total_assigned - 5)

        # -------------------------
        # SOFT 2: Room preference
        # simplified placeholder
        # penalize small room assignment for higher-level courses
        # -------------------------
        for c in courses:
            room_id = self.course_room_map.get(c)
            cap = self._room_capacity(room_id)
            if str(c).startswith("CS2") and cap < 30:
                violations["soft_room_preference"] += 1

        # -------------------------
        # SOFT 3: Instructor preference
        # simplified placeholder: prefer AM for I1 and I3
        # -------------------------
        preferred_am = {"I1", "I3"}
        for c in courses:
            instructor = self._course_instructor(c)
            for t in timeslots:
                active = sum(schedule.get((s, c, t), 0) for s in students) > 0
                if active and instructor in preferred_am and "PM" in t:
                    violations["soft_instructor_preference"] += 1

        # -------------------------
        # SOFT 4: Section preference
        # simplified placeholder: PM scheduling penalty for all students
        # -------------------------
        for (s, c, t), v in schedule.items():
            if v == 1 and "PM" in t:
                violations["soft_section_preference"] += 1

        # Hard sum
        violations["hard"] = (
            violations["student_conflicts"] +
            violations["room_capacity"] +
            violations["instructor_conflict"] +
            violations["room_time_uniqueness"] +
            violations["prerequisite"] +
            violations["instructor_availability"]
        )

        # Weighted score
        weighted_score = 0
        for k, w in self.weights.items():
            weighted_score += w * violations[k]
        violations["score"] = weighted_score

        return violations