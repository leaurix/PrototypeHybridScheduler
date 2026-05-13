from hybrid_scheduler.core.validator import Validator
from hybrid_scheduler.metaheuristics.ga import GeneticAlgorithm
from hybrid_scheduler.metaheuristics.neighborhood_ops import NeighborhoodOperators
from hybrid_scheduler.metaheuristics.alns import ALNS
from hybrid_scheduler.fgasp.feedback import FeedbackEngine
from hybrid_scheduler.fgasp.controller import FGASPController


class HybridSchedulingPipeline:
    """
    Optimised pipeline — CSP build skipped (it was building 200k variables
    but never solving them, wasting several seconds before GA even starts).
    """

    def __init__(self, dataset, ga_population_size=10, ga_generations=5,
                 ga_mutation_rate=0.10, alns_iterations=20, log_callback=None):
        self.dataset            = dataset
        self.ga_population_size = ga_population_size
        self.ga_generations     = ga_generations
        self.ga_mutation_rate   = ga_mutation_rate
        self.alns_iterations    = alns_iterations
        self.log                = log_callback or print

    def build(self):
        validator = Validator(self.dataset)

        ga = GeneticAlgorithm(
            self.dataset, validator,
            population_size=self.ga_population_size,
            generations=self.ga_generations,
            mutation_rate=self.ga_mutation_rate,
            log_callback=self.log,
        )
        ops  = NeighborhoodOperators(self.dataset)
        alns = ALNS(
            self.dataset, validator,
            operators=ops,
            iterations=self.alns_iterations,
            log_callback=self.log,
        )
        feedback_engine = FeedbackEngine()
        controller = FGASPController(
            self.dataset, validator, ga, alns, feedback_engine,
            log_callback=self.log,
        )
        return {
            "csp_model": None, "csp_vars": {},
            "validator": validator, "ga": ga,
            "alns": alns, "feedback_engine": feedback_engine,
            "controller": controller,
        }

    def run(self):
        components = self.build()
        output = components["controller"].run()
        output["csp_model"] = components["csp_model"]
        output["csp_vars"]  = components["csp_vars"]
        output["validator"] = components["validator"]
        return output
