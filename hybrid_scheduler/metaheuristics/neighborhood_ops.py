import random
import ast
from collections import defaultdict


class NeighborhoodOperators:
    """
    Optimised neighbourhood operators with instructor-aware repair.
    Works on compact {(s,c):t} internally; accepts expanded form too.
    """

    def __init__(self, dataset):
        self._students  = list(dataset.students["student_id"])
        self._courses   = list(dataset.courses["course_id"])
        self._timeslots = list(dataset.timeslots["timeslot"])

        # course -> set of valid timeslots (instructor availability)
        ci = dict(zip(dataset.courses["course_id"], dataset.courses["instructor_id"]))
        ia = {}
        for row in dataset.instructors.itertuples():
            slots = row.available_timeslots
            if isinstance(slots, str):
                try: slots = ast.literal_eval(slots)
                except: slots = []
            ia[row.instructor_id] = set(slots)

        self._course_valid_ts = {}
        for c in self._courses:
            inst  = ci.get(c)
            valid = list(ia.get(inst, set()) & set(self._timeslots))
            self._course_valid_ts[c] = valid if valid else self._timeslots

    # ── compact helpers ──────────────────────────────────────────────────────
    @staticmethod
    def _is_compact(schedule):
        for k in schedule:
            return len(k) == 2
        return True

    def _to_compact(self, schedule):
        if self._is_compact(schedule):
            return dict(schedule)
        compact = {}
        for (s, c, t), v in schedule.items():
            if v == 1:
                compact[(s, c)] = t
        for s in self._students:
            for c in self._courses:
                if (s, c) not in compact:
                    compact[(s, c)] = random.choice(self._course_valid_ts[c])
        return compact

    @staticmethod
    def _to_expanded(compact):
        return {(s, c, t): 1 for (s, c), t in compact.items()}

    # ── destroy operators ────────────────────────────────────────────────────
    def destroy_random(self, schedule):
        compact = self._to_compact(schedule)
        keys    = list(compact.keys())
        n       = max(1, len(keys) // 10)
        for k in random.sample(keys, n):
            del compact[k]
        return compact

    def destroy_by_student(self, schedule):
        compact = self._to_compact(schedule)
        s = random.choice(self._students)
        for c in self._courses:
            compact.pop((s, c), None)
        return compact

    def destroy_by_timeslot(self, schedule):
        compact = self._to_compact(schedule)
        t = random.choice(self._timeslots)
        for key, val in list(compact.items()):
            if val == t:
                del compact[key]
        return compact

    # ── instructor-aware greedy repair ───────────────────────────────────────
    def repair_greedy(self, schedule):
        compact = self._to_compact(schedule) if not self._is_compact(schedule) else dict(schedule)

        # track which timeslot each student is already using
        student_ts_used: dict[str, set] = defaultdict(set)
        for (s, c), t in compact.items():
            student_ts_used[s].add(t)

        for s in self._students:
            for c in self._courses:
                if (s, c) not in compact:
                    # prefer a valid slot the student isn't already using
                    valid = self._course_valid_ts[c]
                    free  = [t for t in valid if t not in student_ts_used[s]]
                    chosen = random.choice(free) if free else random.choice(valid)
                    compact[(s, c)] = chosen
                    student_ts_used[s].add(chosen)

        return self._to_expanded(compact)
