class FeedbackEngine:
    """
    Feasibility-Guided feedback engine.

    Purpose:
    - analyze validator results
    - compare GA and ALNS outcomes
    - provide adaptive signals to the controller
    """

    def __init__(self):
        self.history = []

    def summarize_result(self, result_dict):
        return {
            "hard": result_dict.get("hard", 0),
            "score": result_dict.get("score", 0),
            "student_conflicts": result_dict.get("student_conflicts", 0),
            "room_capacity": result_dict.get("room_capacity", 0),
            "instructor_conflict": result_dict.get("instructor_conflict", 0),
            "room_time_uniqueness": result_dict.get("room_time_uniqueness", 0),
            "prerequisite": result_dict.get("prerequisite", 0),
            "instructor_availability": result_dict.get("instructor_availability", 0),
            "soft_balance": result_dict.get("soft_balance", 0),
            "soft_room_preference": result_dict.get("soft_room_preference", 0),
            "soft_instructor_preference": result_dict.get("soft_instructor_preference", 0),
            "soft_section_preference": result_dict.get("soft_section_preference", 0),
        }

    def compare(self, ga_result, alns_result):
        """
        Lower score is better.
        Hard violations have priority.
        """
        if alns_result["hard"] < ga_result["hard"]:
            chosen = "ALNS"
        elif alns_result["hard"] > ga_result["hard"]:
            chosen = "GA"
        else:
            chosen = "ALNS" if alns_result["score"] <= ga_result["score"] else "GA"

        decision = {
            "chosen": chosen,
            "ga_summary": self.summarize_result(ga_result),
            "alns_summary": self.summarize_result(alns_result),
        }
        self.history.append(decision)
        return decision

    def get_history(self):
        return self.history