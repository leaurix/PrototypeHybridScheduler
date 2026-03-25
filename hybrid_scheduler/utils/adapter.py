class Adapter:
    @staticmethod
    def flatten_schedule(schedule):
        rows = []
        for (s, c, t), v in schedule.items():
            if v == 1:
                rows.append({"student": s, "course": c, "timeslot": t})
        return rows

    @staticmethod
    def expand_schedule(entries, dataset):
        sch = {}
        for s in dataset.students["student_id"]:
            for c in dataset.courses["course_id"]:
                for t in dataset.timeslots["timeslot"]:
                    sch[(s, c, t)] = 0

        for e in entries:
            sch[(e["student"], e["course"], e["timeslot"])] = 1
        return sch