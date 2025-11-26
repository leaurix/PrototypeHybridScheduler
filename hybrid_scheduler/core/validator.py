class Validator:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def validate(self, schedule: Dict):
        violations = {
            "hard": 0,
            "student_conflicts": 0,
            "room_capacity": 0,
            "instructor_conflict": 0,
            "prerequisite": 0,
        }

        # Student conflicts
        for s in self.dataset.students['student_id']:
            for t in self.dataset.timeslots['timeslot']:
                assigned = [c for (s2, c, t2), v in schedule.items() if s2 == s and t2 == t and v == 1]
                if len(assigned) > 1:
                    violations['student_conflicts'] += (len(assigned) - 1)

        # Room capacity violations
        for c in self.dataset.courses.itertuples():
            for t in self.dataset.timeslots['timeslot']:
                enrolled = sum(schedule.get((s, c.course_id, t), 0) for s in self.dataset.students['student_id'])
                room_capacity = max(self.dataset.rooms['capacity']) # Simplified
                if enrolled > room_capacity:
                    violations['room_capacity'] += (enrolled - room_capacity)

        violations['hard'] = sum(violations.values())
        return violations