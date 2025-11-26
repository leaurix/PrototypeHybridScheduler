class Adapter:
    @staticmethod
    def flatten_schedule(schedule):
        # Convert (s,c,t) → 1 into [{student, course, timeslot}] entries
        rows = []
        for (s, c, t), v in schedule.items():
            if v == 1:
                rows.append({"student": s, "course": c, "timeslot": t})
        return rows

    @staticmethod
    def expand_schedule(entries, dataset):
        # Convert list of {s,c,t} → full dict of 0/1
        sch = {}
        for s in dataset.students['student_id']:
            for c in dataset.courses['course_id']:
                for t in dataset.timeslots['timeslot']:
                    sch[(s, c, t)] = 0
        for e in entries:
            sch[(e['student'], e['course'], e['timeslot'])] = 1
        return sch