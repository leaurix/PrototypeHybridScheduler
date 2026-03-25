from __future__ import annotations
import random
import copy
from hybrid_scheduler.metaheuristics.neighborhood_ops import NeighborhoodOperators


class ALNS:
    def __init__(self, dataset, validator, operators: NeighborhoodOperators, iterations=200):
        self.dataset = dataset
        self.validator = validator
        self.operators = operators
        self.iterations = iterations

        self.weights = {
            "random": 1.0,
            "student": 1.0,
            "timeslot": 1.0,
        }

    def select_operator(self):
        ops = list(self.weights.keys())
        probs = list(self.weights.values())
        return random.choices(ops, weights=probs, k=1)[0]

    def apply_destroy(self, schedule, op):
        if op == "random":
            return self.operators.destroy_random(schedule)
        if op == "student":
            return self.operators.destroy_by_student(schedule)
        if op == "timeslot":
            return self.operators.destroy_by_timeslot(schedule)
        return schedule

    def repair(self, schedule):
        return self.operators.repair_greedy(schedule)

    def score(self, schedule):
        v = self.validator.validate(schedule)
        return -v["score"]

    def update_weights(self, op, old_score, new_score):
        """
        FGASP-like adaptive feedback:
        if improved, increase operator weight; else reduce slightly
        """
        if new_score > old_score:
            self.weights[op] *= 1.20
        else:
            self.weights[op] *= 0.95

    def run(self, initial_schedule):
        current = copy.deepcopy(initial_schedule)
        current_score = self.score(current)

        for _ in range(self.iterations):
            op = self.select_operator()
            destroyed = self.apply_destroy(current, op)
            repaired = self.repair(destroyed)
            new_score = self.score(repaired)

            if new_score > current_score:
                self.update_weights(op, current_score, new_score)
                current = repaired
                current_score = new_score
            else:
                self.update_weights(op, current_score, new_score)

        return current