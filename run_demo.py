import os
import sys

from hybrid_scheduler.utils.dataset_loader import load_dataset
from hybrid_scheduler.core.validator import Validator
from hybrid_scheduler.metaheuristics.ga import GeneticAlgorithm
from hybrid_scheduler.metaheuristics.neighborhood_ops import NeighborhoodOperators
from hybrid_scheduler.metaheuristics.alns import ALNS


def main(data_dir="dummy_dataset"):

    print("RUN_DEMO STARTED")

    print("1) About to load dataset...")
    ds = load_dataset(
        os.path.join(data_dir, "students.csv"),
        os.path.join(data_dir, "courses.csv"),
        os.path.join(data_dir, "rooms.csv"),
        os.path.join(data_dir, "instructors.csv"),
        os.path.join(data_dir, "timeslots.csv"),
    )
    print("2) Dataset loaded OK.")

    validator = Validator(ds)
    print("3) Validator created.")

    print("4) Starting GA...")
    ga = GeneticAlgorithm(
        ds,
        validator,
        population_size=10,
        generations=3,
        mutation_rate=0.05
    )
    ga_best = ga.run()
    print("5) GA finished.")

    print("6) Starting ALNS...")
    ops = NeighborhoodOperators(ds)
    alns = ALNS(ds, validator, operators=ops, iterations=20)
    alns_best = alns.run(ga_best)
    print("7) ALNS finished.")

    print("\n===== VALIDATION RESULTS =====")
    print("GA violations:", validator.validate(ga_best))
    print("ALNS violations:", validator.validate(alns_best))

    print("\n===== SAMPLE SCHEDULE (First student) =====")
    sample_student = ds.students['student_id'].iloc[0]
    for c in ds.courses['course_id']:
        assigned = [
            t for t in ds.timeslots['timeslot']
            if alns_best.get((sample_student, c, t), 0) == 1
        ]
        print(f"{sample_student} -> {c}: {assigned}")
        
    print("DONE.")


if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "dummy_dataset"
    main(data_dir)