import random
import copy
from concurrent.futures import ThreadPoolExecutor


class GeneticAlgorithm:
    """
    Optimised GA:
    - Compact schedule representation {(s,c): t}  (~70x smaller than sparse matrix)
    - Parallel fitness evaluation across population using threads
    - Converts to expanded form only for validator hand-off
    """

    def __init__(self, dataset, validator, population_size=10, generations=5,
                 mutation_rate=0.1, log_callback=None):
        self.dataset         = dataset
        self.validator       = validator
        self.population_size = population_size
        self.generations     = generations
        self.mutation_rate   = mutation_rate
        self.log             = log_callback or print

        # cache lists once
        self._students  = list(dataset.students["student_id"])
        self._courses   = list(dataset.courses["course_id"])
        self._timeslots = list(dataset.timeslots["timeslot"])

        # worker pool — reused across generations
        self._pool = ThreadPoolExecutor(max_workers=4)

    # ── compact schedule helpers ─────────────────────────────────────────────
    def _create_compact(self):
        ts = self._timeslots
        return {(s, c): random.choice(ts)
                for s in self._students
                for c in self._courses}

    @staticmethod
    def _expand(compact):
        """Compact {(s,c):t} → sparse {(s,c,t):1} for validator."""
        return {(s, c, t): 1 for (s, c), t in compact.items()}

    # ── GA operators ─────────────────────────────────────────────────────────
    def _fitness(self, compact):
        return -self.validator.validate(self._expand(compact))["score"]

    def _eval_population(self, population):
        """Evaluate entire population in parallel."""
        fits = list(self._pool.map(self._fitness, population))
        return list(zip(fits, population))

    def _mutate(self, compact):
        new = compact.copy()
        if random.random() < self.mutation_rate:
            s = random.choice(self._students)
            c = random.choice(self._courses)
            new[(s, c)] = random.choice(self._timeslots)
        return new

    def _crossover(self, p1, p2):
        child = {}
        for key in p1:
            child[key] = p1[key] if random.random() < 0.5 else p2[key]
        return child

    def _select(self, scored, k=3):
        candidates = random.sample(scored, min(k, len(scored)))
        return max(candidates, key=lambda x: x[0])[1]

    # ── main loop ────────────────────────────────────────────────────────────
    def run(self):
        self.log("      Initialising population...\n")
        population = [self._create_compact() for _ in range(self.population_size)]

        for g in range(self.generations):
            scored = self._eval_population(population)
            best_f = max(scored, key=lambda x: x[0])[0]
            self.log(f"      gen {g+1}/{self.generations}  fitness={best_f}\n\n")

            elite   = max(scored, key=lambda x: x[0])[1]
            new_pop = [elite.copy()]

            while len(new_pop) < self.population_size:
                child = self._crossover(self._select(scored), self._select(scored))
                child = self._mutate(child)
                new_pop.append(child)

            population = new_pop

        scored     = self._eval_population(population)
        best       = max(scored, key=lambda x: x[0])[1]
        self.log("      GA complete.\n\n")
        return self._expand(best)
