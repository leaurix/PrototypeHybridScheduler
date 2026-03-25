import random
import copy


class GeneticAlgorithm:
    def __init__(self, dataset, validator, population_size=30, generations=50, mutation_rate=0.1):
        self.dataset = dataset
        self.validator = validator
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def create_random_schedule(self):
        """
        One student-course gets exactly one timeslot.
        """
        schedule = {}
        timeslots = list(self.dataset.timeslots["timeslot"])

        for s in self.dataset.students["student_id"]:
            for c in self.dataset.courses["course_id"]:
                chosen_slot = random.choice(timeslots)
                for t in timeslots:
                    schedule[(s, c, t)] = 1 if t == chosen_slot else 0
        return schedule

    def fitness(self, schedule):
        violations = self.validator.validate(schedule)
        # Lower score is better, so fitness is negative score
        return -violations["score"]

    def mutate(self, schedule):
        """
        Mutation that preserves one-timeslot-per-student-course.
        """
        new_sch = copy.deepcopy(schedule)
        s = random.choice(list(self.dataset.students["student_id"]))
        c = random.choice(list(self.dataset.courses["course_id"]))
        timeslots = list(self.dataset.timeslots["timeslot"])

        if random.random() < self.mutation_rate:
            for t in timeslots:
                new_sch[(s, c, t)] = 0
            chosen = random.choice(timeslots)
            new_sch[(s, c, chosen)] = 1

        return new_sch

    def crossover(self, parent1, parent2):
        """
        Crossover by student-course block to preserve structure.
        """
        child = {}
        timeslots = list(self.dataset.timeslots["timeslot"])

        for s in self.dataset.students["student_id"]:
            for c in self.dataset.courses["course_id"]:
                source = parent1 if random.random() < 0.5 else parent2
                for t in timeslots:
                    child[(s, c, t)] = source[(s, c, t)]
        return child

    def select_parent(self, population, tournament_size=3):
        candidates = random.sample(population, min(tournament_size, len(population)))
        return max(candidates, key=self.fitness)

    def run(self):
        population = [self.create_random_schedule() for _ in range(self.population_size)]

        for _ in range(self.generations):
            new_population = []

            elite = max(population, key=self.fitness)
            new_population.append(copy.deepcopy(elite))

            while len(new_population) < self.population_size:
                p1 = self.select_parent(population)
                p2 = self.select_parent(population)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        best = max(population, key=self.fitness)
        return best