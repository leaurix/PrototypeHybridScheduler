import random
import copy

class GeneticAlgorithm:
    def __init__(self, dataset, validator, population_size=30, generations=50, mutation_rate=0.1):
        self.dataset = dataset
        self.validator = validator
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

# ----------------------------------------------------
# Chromosome representation: dict {(s,c,t): 0/1}
# ----------------------------------------------------
    def create_random_schedule(self):
        schedule = {}
        for s in self.dataset.students['student_id']:
            for c in self.dataset.courses['course_id']:
                # Randomly assign student to ONLY ONE timeslot of the course
                chosen_slot = random.choice(self.dataset.timeslots['timeslot'])
                for t in self.dataset.timeslots['timeslot']:
                    schedule[(s, c, t)] = 1 if t == chosen_slot else 0
        return schedule

# ----------------------------------------------------
    def fitness(self, schedule):
        violations = self.validator.validate(schedule)
        # Heavy penalty for hard constraint violations
        penalty = 10000 * violations['hard']
        return -(penalty)
    
# ----------------------------------------------------
    def mutate(self, schedule):
        new_sch = copy.deepcopy(schedule)
        for key in new_sch:
            if random.random() < self.mutation_rate:
                new_sch[key] = 1 - new_sch[key]
        return new_sch

# ----------------------------------------------------
    def crossover(self, parent1, parent2):
        child = {}
        for key in parent1:
            child[key] = parent1[key] if random.random() < 0.5 else parent2[key]
        return child

# ----------------------------------------------------
    def select_parent(self, population):
        return max(population, key=lambda sch: self.fitness(sch))

# ----------------------------------------------------
    def run(self):
        # Initialize population
        population = [self.create_random_schedule() for _ in range(self.population_size)]

        for g in range(self.generations):
            new_population = []

            for _ in range(self.population_size):
                p1 = self.select_parent(population)
                p2 = self.select_parent(population)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        best = max(population, key=lambda sch: self.fitness(sch))
        return best