import random
import copy


class GeneticAlgorithm:
    def __init__(self, dataset, validator, population_size=10, generations=5, mutation_rate=0.1):
        self.dataset = dataset
        self.validator = validator
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def create_random_schedule(self):
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
        return -violations["score"]

    def mutate(self, schedule):
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
        child = {}
        timeslots = list(self.dataset.timeslots["timeslot"])

        for s in self.dataset.students["student_id"]:
            for c in self.dataset.courses["course_id"]:
                source = parent1 if random.random() < 0.5 else parent2
                for t in timeslots:
                    child[(s, c, t)] = source[(s, c, t)]
        return child

    def select_parent(self, scored_population, tournament_size=3):
        candidates = random.sample(scored_population, min(tournament_size, len(scored_population)))
        # each item is (fitness, schedule)
        return max(candidates, key=lambda x: x[0])[1]

    def run(self):
        print("GA: initializing population...")
        population = [self.create_random_schedule() for _ in range(self.population_size)]

        for g in range(self.generations):
            scored_population = [(self.fitness(sch), sch) for sch in population]
            best_fitness = max(scored_population, key=lambda x: x[0])[0]
            print(f"GA: generation {g + 1}/{self.generations}, best fitness = {best_fitness}")

            new_population = []

            # elitism
            elite = max(scored_population, key=lambda x: x[0])[1]
            new_population.append(copy.deepcopy(elite))

            while len(new_population) < self.population_size:
                p1 = self.select_parent(scored_population)
                p2 = self.select_parent(scored_population)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        scored_population = [(self.fitness(sch), sch) for sch in population]
        best = max(scored_population, key=lambda x: x[0])[1]
        print("GA: finished.")
        return best