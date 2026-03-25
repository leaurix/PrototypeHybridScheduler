import os
import sys
import time
import pandas as pd

from hybrid_scheduler.utils.dataset_loader import load_dataset
from hybrid_scheduler.core.validator import Validator
from hybrid_scheduler.core.csp_model import CSPModel
from hybrid_scheduler.metaheuristics.ga import GeneticAlgorithm
from hybrid_scheduler.metaheuristics.neighborhood_ops import NeighborhoodOperators
from hybrid_scheduler.metaheuristics.alns import ALNS


def export_schedule_csv(schedule, output_file="output_schedule.csv"):
    rows = []
    for (s, c, t), v in schedule.items():
        if v == 1:
            rows.append({
                "student_id": s,
                "course_id": c,
                "timeslot": t
            })
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    return output_file


def print_schedule_sample(dataset, schedule, n_students=5):
    print("\n===== SCHEDULE SAMPLE =====")
    for s in dataset.students["student_id"].head(n_students):
        print(f"\nSchedule for {s}:")
        for c in dataset.courses["course_id"]:
            assigned = [
                t for t in dataset.timeslots["timeslot"]
                if schedule.get((s, c, t), 0) == 1
            ]
            if assigned:
                print(f"  {c} -> {assigned}")


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

    print("3) Building CSP feasibility layer...")
    csp = CSPModel(ds)
    csp_model, csp_vars = csp.build()
    print("4) CSP model built successfully.")

    validator = Validator(ds)
    print("5) Validator created.")

    print("6) Starting GA...")
    start_ga = time.time()
    ga = GeneticAlgorithm(
        ds,
        validator,
        population_size=20,
        generations=20,
        mutation_rate=0.10
    )
    ga_best = ga.run()
    ga_time = time.time() - start_ga
    ga_result = validator.validate(ga_best)
    print("7) GA finished.")

    print("8) Starting ALNS...")
    start_alns = time.time()
    ops = NeighborhoodOperators(ds)
    alns = ALNS(ds, validator, operators=ops, iterations=100)
    alns_best = alns.run(ga_best)
    alns_time = time.time() - start_alns
    alns_result = validator.validate(alns_best)
    print("9) ALNS finished.")

    print("\n===== VALIDATION RESULTS =====")
    print("GA result:", ga_result)
    print("ALNS result:", alns_result)

    print("\n===== EXECUTION TIME =====")
    print(f"GA runtime: {ga_time:.4f} seconds")
    print(f"ALNS runtime: {alns_time:.4f} seconds")
    print(f"Total runtime: {ga_time + alns_time:.4f} seconds")

    print_schedule_sample(ds, alns_best, n_students=5)

    output_file = export_schedule_csv(alns_best, "output_schedule.csv")
    print(f"\nSaved schedule to {output_file}")

    print("\nDONE.")


if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "dummy_dataset"
    main(data_dir)