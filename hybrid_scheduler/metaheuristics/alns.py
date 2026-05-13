from __future__ import annotations
import random
from hybrid_scheduler.metaheuristics.neighborhood_ops import NeighborhoodOperators


class ALNS:
    """
    Optimised ALNS — avoids deepcopy, tracks global best separately,
    accepts log_callback for GUI integration.
    """

    def __init__(self, dataset, validator, operators: NeighborhoodOperators,
                 iterations=20, log_callback=None):
        self.validator  = validator
        self.operators  = operators
        self.iterations = iterations
        self.log        = log_callback or print
        self.weights    = {"random": 1.0, "student": 1.0, "timeslot": 1.0}

    def _select_op(self):
        ops, probs = zip(*self.weights.items())
        return random.choices(ops, weights=probs, k=1)[0]

    def _destroy(self, schedule, op):
        if op == "random":   return self.operators.destroy_random(schedule)
        if op == "student":  return self.operators.destroy_by_student(schedule)
        if op == "timeslot": return self.operators.destroy_by_timeslot(schedule)
        return schedule

    def _score(self, schedule):
        return -self.validator.validate(schedule)["score"]

    def run(self, initial_schedule):
        current       = initial_schedule
        current_score = self._score(current)
        best          = current
        best_score    = current_score
        log_every     = max(1, self.iterations // 5)

        for i in range(self.iterations):
            op        = self._select_op()
            destroyed = self._destroy(current, op)
            repaired  = self.operators.repair_greedy(destroyed)
            new_score = self._score(repaired)

            # adaptive weight update
            if new_score > current_score:
                self.weights[op] = min(self.weights[op] * 1.20, 10.0)
                current, current_score = repaired, new_score
                if new_score > best_score:
                    best, best_score = repaired, new_score
            else:
                self.weights[op] = max(self.weights[op] * 0.95, 0.1)

            if (i + 1) % log_every == 0:
                self.log(f"      ALNS iter {i+1}/{self.iterations}  score={-best_score}\n\n")

        return best
