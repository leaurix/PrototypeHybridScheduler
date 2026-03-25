import random
import copy


class NeighborhoodOperators:
    def __init__(self, dataset):
        self.dataset = dataset

    def destroy_random(self, schedule, percent=0.05):
        new_sch = copy.deepcopy(schedule)
        keys = list(new_sch.keys())
        remove_count = max(1, int(len(keys) * percent))
        to_remove = random.sample(keys, remove_count)

        for k in to_remove:
            new_sch[k] = 0

        return new_sch

    def destroy_by_student(self, schedule):
        new_sch = copy.deepcopy(schedule)
        s = random.choice(list(self.dataset.students['student_id']))

        for (stud, c, t) in list(new_sch.keys()):
            if stud == s:
                new_sch[(stud, c, t)] = 0

        return new_sch

    def destroy_by_timeslot(self, schedule):
        new_sch = copy.deepcopy(schedule)
        t = random.choice(list(self.dataset.timeslots['timeslot']))

        for (s, c, ts) in list(new_sch.keys()):
            if ts == t:
                new_sch[(s, c, ts)] = 0

        return new_sch

    def repair_greedy(self, schedule):
        new_sch = copy.deepcopy(schedule)
        timeslots = list(self.dataset.timeslots['timeslot'])

        for s in self.dataset.students['student_id']:
            for c in self.dataset.courses['course_id']:

                # Check if assigned
                assigned = [t for t in timeslots if new_sch[(s, c, t)] == 1]

                if len(assigned) == 0:
                    chosen = random.choice(timeslots)
                    new_sch[(s, c, chosen)] = 1

                elif len(assigned) > 1:
                    keep = random.choice(assigned)
                    for t in timeslots:
                        new_sch[(s, c, t)] = 1 if t == keep else 0

        return new_sch