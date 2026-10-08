"""Quick regression tests. Run from the project folder:  python -m pytest -q"""
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from hybrid_scheduler.core.validator import Validator
from hybrid_scheduler.fgasp.pipeline import HybridSchedulingPipeline
from hybrid_scheduler.utils.dataset_loader import Dataset, load_dataset

DUMMY = os.path.join(ROOT, "dummy_dataset")
CSVS = ["students.csv", "courses.csv", "rooms.csv", "instructors.csv", "timeslots.csv"]


def _tiny(inst_slots):
    return Dataset(
        students=pd.DataFrame({"student_id": ["SEC_A"]}),
        courses=pd.DataFrame({"course_id": ["CS111"], "instructor_id": ["I001"],
                              "prerequisite": [None]}),
        rooms=pd.DataFrame({"room_id": ["101"], "capacity": [40]}),
        instructors=pd.DataFrame({"instructor_id": ["I001"], "name": ["X"],
                                  "available_timeslots": [inst_slots]}),
        timeslots=pd.DataFrame({"timeslot": ["TSMon_0700", "TSMon_0800"]}),
    )


def test_empty_availability_means_unrestricted():
    r = Validator(_tiny([])).validate({("SEC_A", "CS111", "TSMon_0800"): 1})
    assert r["instructor_availability"] == 0


def test_availability_still_enforced_when_listed():
    r = Validator(_tiny(["TSMon_0700"])).validate({("SEC_A", "CS111", "TSMon_0800"): 1})
    assert r["instructor_availability"] == 1


def test_same_seed_same_result():
    ds = load_dataset(*[os.path.join(DUMMY, f) for f in CSVS])
    quiet = lambda m: None
    a = HybridSchedulingPipeline(ds, 6, 3, 0.1, 10, log_callback=quiet, seed=42).run()
    b = HybridSchedulingPipeline(ds, 6, 3, 0.1, 10, log_callback=quiet, seed=42).run()
    assert a["best_result"] == b["best_result"]
    assert a["best_solution"] == b["best_solution"]


def test_every_student_course_pair_scheduled_once():
    ds = load_dataset(*[os.path.join(DUMMY, f) for f in CSVS])
    out = HybridSchedulingPipeline(ds, 6, 3, 0.1, 10, log_callback=lambda m: None, seed=1).run()
    pairs = [(s, c) for (s, c, t), v in out["best_solution"].items() if v == 1]
    assert len(pairs) == len(set(pairs)) == len(ds.students) * len(ds.courses)
