import os
import sys
import time
import pandas as pd

from hybrid_scheduler.utils.dataset_loader import load_dataset
from hybrid_scheduler.fgasp.pipeline import HybridSchedulingPipeline


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

    print("3) Starting FGASP pipeline...")
    start_total = time.time()

    pipeline = HybridSchedulingPipeline(
        ds,
        ga_population_size=10,
        ga_generations=5,
        ga_mutation_rate=0.10,
        alns_iterations=20,
    )

    output = pipeline.run()
    total_time = time.time() - start_total

    ga_result = output["ga_result"]
    alns_result = output["alns_result"]
    best_result = output["best_result"]
    best_schedule = output["best_solution"]
    decision = output["decision"]["chosen"]

    print("4) FGASP pipeline finished.")

    print("\n===== VALIDATION RESULTS =====")
    print("GA result:", ga_result)
    print("ALNS result:", alns_result)
    print("FGASP chosen method:", decision)
    print("FGASP best result:", best_result)

    print("\n===== EXECUTION TIME =====")
    print(f"Total runtime: {total_time:.4f} seconds")

    print_schedule_sample(ds, best_schedule, n_students=5)

    output_file = export_schedule_csv(best_schedule, "output_schedule.csv")
    print(f"\nSaved schedule to {output_file}")

    print("\nDONE.")


if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "dummy_dataset"
    main(data_dir)