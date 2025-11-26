import random

class NeighborhoodOperators:
    def __init__(self, dataset):
        self.dataset = dataset

# -----------------------------------------------------
    def destroy_random(self, schedule, percent=0.05):
        new_sch = schedule.copy()
        keys = list(new_sch.keys())
        to_remove = random.sample(keys, int(len(keys) * percent))
        for k in to_remove:
            new_sch[k] = 0
        return new_sch

# -----------------------------------------------------
    def destroy_by_student(self, schedule):
        new_sch = schedule.copy()
        s = random.choice(self.dataset.students['student_id'])
        for (stud, c, t) in new_sch:
            if stud == s:
                new_sch[(stud, c, t)] = 0
        return new_sch

# -----------------------------------------------------
    def destroy_by_timeslot(self, schedule):
        new_sch = schedule.copy()
        t = random.choice(self.dataset.timeslots['timeslot'])
        for (s, c, ts) in new_sch:
            if ts == t:
                new_sch[(s, c, ts)] = 0
        return new_sch

# -----------------------------------------------------
    def repair_greedy(self, schedule):
        new_sch = schedule.copy()
        for s in self.dataset.students['student_id']:
            for c in self.dataset.courses['course_id']:
                # If no assignment exists, assign randomly
                if not any(new_sch[(s, c, t)] == 1 for t in self.dataset.timeslots['timeslot']):
                    t = random.choice(self.dataset.timeslots['timeslot'])
                    new_sch[(s, c, t)] = 1
        return new_sch