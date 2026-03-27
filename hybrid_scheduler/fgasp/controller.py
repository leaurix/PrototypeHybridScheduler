class FGASPController:
    """
    Feasibility-Guided Adaptive Search Protocol (FGASP)

    Responsibilities:
    - run GA for global search
    - evaluate GA schedule
    - run ALNS for local refinement
    - compare results through feedback engine
    - return best solution
    """

    def __init__(self, dataset, validator, ga, alns, feedback_engine):
        self.dataset = dataset
        self.validator = validator
        self.ga = ga
        self.alns = alns
        self.feedback_engine = feedback_engine
        self.performance_history = []

    def run(self):
        # Step 1: GA global search
        ga_solution = self.ga.run()
        ga_result = self.validator.validate(ga_solution)

        # Step 2: ALNS local refinement
        alns_solution = self.alns.run(ga_solution)
        alns_result = self.validator.validate(alns_solution)

        # Step 3: Feasibility-guided comparison
        decision = self.feedback_engine.compare(ga_result, alns_result)

        if decision["chosen"] == "ALNS":
            best_solution = alns_solution
            best_result = alns_result
        else:
            best_solution = ga_solution
            best_result = ga_result

        record = {
            "ga_result": ga_result,
            "alns_result": alns_result,
            "decision": decision["chosen"],
            "best_result": best_result,
        }
        self.performance_history.append(record)

        return {
            "ga_solution": ga_solution,
            "ga_result": ga_result,
            "alns_solution": alns_solution,
            "alns_result": alns_result,
            "best_solution": best_solution,
            "best_result": best_result,
            "decision": decision,
            "history": self.performance_history,
        }