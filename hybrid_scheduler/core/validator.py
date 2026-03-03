from __future__ import annotations
from typing import Dict, Any
from hybrid_scheduler.utils.dataset_loader import Dataset

class Validator:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def validate(self, schedule: Dict[Any, int]):
        violations = {
            "hard": 0,
            "student_conflicts": 0,
            "room_capacity": 0,
            "instructor_conflict": 0,
            "prerequisite": 0,
        }

        # Student conflicts: a student cannot take 2+ courses in same timeslot
        for s in self.dataset.students['student_id']:
            for t in self.dataset.timeslots['timeslot']:
                assigned = [
                    c for (s2, c, t2), v in schedule.items()
                    if s2 == s and t2 == t and v == 1
                ]
                if len(assigned) > 1:
                    violations['student_conflicts'] += (len(assigned) - 1)

        # Room capacity (simplified): compare to max capacity among rooms
        max_cap = int(self.dataset.rooms['capacity'].max())
        for c in self.dataset.courses['course_id']:
            for t in self.dataset.timeslots['timeslot']:
                enrolled = sum(
                    schedule.get((s, c, t), 0) for s in self.dataset.students['student_id']
                )
                if enrolled > max_cap:
                    violations['room_capacity'] += (enrolled - max_cap)

        violations['hard'] = (
            violations['student_conflicts'] + violations['room_capacity']
            + violations['instructor_conflict'] + violations['prerequisite']
        )
        return violations