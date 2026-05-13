class FGASPController:
    def __init__(self, dataset, validator, ga, alns, feedback_engine, log_callback=None):
        self.dataset            = dataset
        self.validator          = validator
        self.ga                 = ga
        self.alns               = alns
        self.feedback_engine    = feedback_engine
        self.performance_history = []
        self.log                = log_callback or print

    def run(self):
        self.log("── GA global search ──────────────────────────\n")
        ga_solution = self.ga.run()
        ga_result   = self.validator.validate(ga_solution)
        self.log(f"   GA score={ga_result['score']}  hard={ga_result['hard']}\n\n")

        self.log("── ALNS local refinement ─────────────────────\n")
        alns_solution = self.alns.run(ga_solution)
        alns_result   = self.validator.validate(alns_solution)
        self.log(f"   ALNS score={alns_result['score']}  hard={alns_result['hard']}\n\n")

        self.log("── FGASP decision ────────────────────────────\n")
        decision = self.feedback_engine.compare(ga_result, alns_result)

        if decision["chosen"] == "ALNS":
            best_solution, best_result = alns_solution, alns_result
        else:
            best_solution, best_result = ga_solution, ga_result

        self.log(f"   Chosen: {decision['chosen']}  final score={best_result['score']}\n")

        record = {
            "ga_result":   ga_result,
            "alns_result": alns_result,
            "decision":    decision["chosen"],
            "best_result": best_result,
        }
        self.performance_history.append(record)

        return {
            "ga_solution":   ga_solution,
            "ga_result":     ga_result,
            "alns_solution": alns_solution,
            "alns_result":   alns_result,
            "best_solution": best_solution,
            "best_result":   best_result,
            "decision":      decision,
            "history":       self.performance_history,
        }
