from ortools.sat.python import cp_model

class CSPModel:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.model = cp_model.CpModel()
        self.assignment_vars = {}


    def build_variables(self):
        for s in self.dataset.students['student_id']:
            for c in self.dataset.courses['course_id']:
                for t in self.dataset.timeslots['timeslot']:
                    name = f"A_{s}_{c}_{t}"
                    self.assignment_vars[(s, c, t)] = self.model.NewBoolVar(name)


    def add_student_no_overlap_constraint(self):
        for s in self.dataset.students['student_id']:
            for t in self.dataset.timeslots['timeslot']:
                self.model.Add(
                    sum(self.assignment_vars[(s, c, t)] for c in self.dataset.courses['course_id']) <= 1
                )


    def add_room_capacity_constraints(self):
        for c in self.dataset.courses.itertuples():
            for r in self.dataset.rooms.itertuples():
                for t in self.dataset.timeslots['timeslot']:
                    enrolled = sum(self.assignment_vars[(s, c.course_id, t)] for s in self.dataset.students['student_id'])
                    self.model.Add(enrolled <= r.capacity)


    def add_instructor_availability_constraints(self):
        for c in self.dataset.courses.itertuples():
            instructor = c.instructor_id
            available_slots = self.dataset.instructors[self.dataset.instructors['instructor_id'] == instructor]['available_timeslots'].iloc[0]
            available_slots = eval(available_slots)

            for t in self.dataset.timeslots['timeslot']:
                if t not in available_slots:
                    for s in self.dataset.students['student_id']:
                        self.model.Add(self.assignment_vars[(s, c.course_id, t)] == 0)


    def add_prerequisite_constraints(self):
        for c in self.dataset.courses.itertuples():
            if str(c.prerequisite) != 'nan':
                prereq = c.prerequisite
                for s in self.dataset.students['student_id']:
                    for t in self.dataset.timeslots['timeslot']:
                        self.model.Add(self.assignment_vars[(s, c.course_id, t)] <= sum(
                            self.assignment_vars[(s, prereq, t2)] for t2 in self.dataset.timeslots['timeslot']
                    ))


    def build(self):
        self.build_variables()
        self.add_student_no_overlap_constraint()
        self.add_room_capacity_constraints()
        self.add_instructor_availability_constraints()
        self.add_prerequisite_constraints()
        return self.model, self.assignment_vars