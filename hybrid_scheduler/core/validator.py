from __future__ import annotations
import ast
from collections import defaultdict
from typing import Dict, Any
from hybrid_scheduler.utils.dataset_loader import Dataset


class Validator:
    """
    Optimised validator — pre-caches all lookups so validate() never
    touches pandas DataFrames at runtime.
    Lower score = better schedule.
    """

    def __init__(self, dataset: Dataset):
        self.dataset = dataset

        self.weights = {
            "room_capacity":          10,
            "instructor_conflict":    10,
            "student_conflicts":      10,
            "room_time_uniqueness":    9,
            "prerequisite":            8,
            "instructor_availability": 7,
            "soft_balance":            4,
            "soft_room_preference":    3,
            "soft_instructor_preference": 2,
            "soft_section_preference": 1,
        }

        # pre-build all caches once
        self.students  = list(dataset.students["student_id"])
        self.courses   = list(dataset.courses["course_id"])
        self.timeslots = list(dataset.timeslots["timeslot"])

        # course -> instructor_id
        self._course_instructor = dict(
            zip(dataset.courses["course_id"], dataset.courses["instructor_id"])
        )

        # instructor_id -> set of available timeslots
        self._inst_available: dict[str, set] = {}
        for row in dataset.instructors.itertuples():
            slots = row.available_timeslots
            if isinstance(slots, str):
                try:
                    slots = ast.literal_eval(slots)
                except Exception:
                    slots = []
            self._inst_available[row.instructor_id] = set(slots)

        # room_id -> capacity
        self._room_cap = dict(
            zip(dataset.rooms["room_id"].astype(str),
                dataset.rooms["capacity"].astype(int))
        )

        # course -> room (round-robin)
        rooms = list(dataset.rooms["room_id"].astype(str))
        self.course_room_map = {
            c: rooms[i % len(rooms)] for i, c in enumerate(self.courses)
        } if rooms else {}

        # course -> prerequisite (or None)
        self._prereq: dict[str, str | None] = {}
        for row in dataset.courses.itertuples():
            p = str(row.prerequisite)
            self._prereq[row.course_id] = None if p in ("nan", "None", "") else p

    def validate(self, schedule: Dict[Any, int]) -> dict:
        v = defaultdict(int)

        # Build sparse index once from schedule — O(|schedule|)
        st_courses  = defaultdict(list)  # (s,t) -> [c]
        ct_students = defaultdict(int)   # (c,t) -> count
        s_courses   = defaultdict(set)   # s     -> {c}
        inst_t      = defaultdict(set)   # (inst,t) -> {c}
        room_t      = defaultdict(set)   # (room,t) -> {c}

        for (s, c, t), val in schedule.items():
            if val != 1:
                continue
            st_courses[(s, t)].append(c)
            ct_students[(c, t)] += 1
            s_courses[s].add(c)
            inst = self._course_instructor.get(c)
            if inst:
                inst_t[(inst, t)].add(c)
            room = self.course_room_map.get(c)
            if room:
                room_t[(room, t)].add(c)

        # HARD 1: Student conflicts
        for cs in st_courses.values():
            if len(cs) > 1:
                v["student_conflicts"] += len(cs) - 1

        # HARD 2: Room capacity
        for (c, t), count in ct_students.items():
            room = self.course_room_map.get(c)
            cap  = self._room_cap.get(str(room), 0)
            if count > cap:
                v["room_capacity"] += count - cap

        # HARD 3: Instructor conflict
        for cs in inst_t.values():
            if len(cs) > 1:
                v["instructor_conflict"] += len(cs) - 1

        # HARD 4: Room-time uniqueness
        for cs in room_t.values():
            if len(cs) > 1:
                v["room_time_uniqueness"] += len(cs) - 1

        # HARD 5: Prerequisites
        for s, cs in s_courses.items():
            for c in cs:
                prereq = self._prereq.get(c)
                if prereq and prereq not in cs:
                    v["prerequisite"] += 1

        # HARD 6: Instructor availability
        for (c, t), count in ct_students.items():
            if count > 0:
                inst = self._course_instructor.get(c)
                if inst and t not in self._inst_available.get(inst, set()):
                    v["instructor_availability"] += 1

        # SOFT 1: Balance
        for cs in s_courses.values():
            if len(cs) > 5:
                v["soft_balance"] += len(cs) - 5

        # SOFT 2: Room preference
        for c in self.courses:
            room = self.course_room_map.get(c)
            if room and str(c).startswith("CS2"):
                if self._room_cap.get(str(room), 999) < 30:
                    v["soft_room_preference"] += 1

        # SOFT 3: Instructor preference
        preferred_am = {"I1", "I3"}
        for (inst, t), cs in inst_t.items():
            if inst in preferred_am and ("PM" in t or t[-4:] in ("1300","1400","1500","1600","1700")):
                v["soft_instructor_preference"] += len(cs)

        # SOFT 4: Section preference — PM penalty
        for (s, t), cs in st_courses.items():
            if "PM" in t or t[-4:] in ("1300","1400","1500","1600","1700"):
                v["soft_section_preference"] += len(cs)

        # Totals
        hard_keys = ["student_conflicts","room_capacity","instructor_conflict",
                     "room_time_uniqueness","prerequisite","instructor_availability"]
        v["hard"]  = sum(v[k] for k in hard_keys)
        v["score"] = sum(self.weights.get(k, 1) * v[k] for k in self.weights)

        return dict(v)
