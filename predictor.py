import math

class Over15Predictor:
    @staticmethod
    def estimate_probability(home_stats, away_stats):
        if not home_stats or not away_stats:
            return {"probability": 0.0, "status": "insuffisantes"}

        lambda_goals = (home_stats["avg_scored"] + away_stats["avg_conceded"] +
                        away_stats["avg_scored"] + home_stats["avg_conceded"]) / 2.0

        poisson_prob = 1.0 - math.exp(-lambda_goals) * (1.0 + lambda_goals)
        poisson_percentage = poisson_prob * 100.0

        history_ratio = (home_stats["over_15_ratio"] + away_stats["over_15_ratio"]) / 2.0 * 100.0

        final_score = (poisson_percentage * 0.4) + (history_ratio * 0.6)

        return {
            "probability": round(final_score, 1),
            "lambda": round(lambda_goals, 2),
            "status": "observées"
        }
