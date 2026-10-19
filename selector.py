from config import MAX_MATCHES_PER_DAY, MIN_OVER_15_RATIO, MIN_PROBABILITY
from statistics import StatisticsAnalyzer
from predictor import Over15Predictor
from football_api import FootballAPI

class MatchSelector:
    def __init__(self):
        self.api = FootballAPI()

    def select_daily_matches(self, date_str: str):
        fixtures = self.api.get_fixtures(date_str)
        selected_matches = []
        rejected_count = 0

        for fixture in fixtures:
            home = fixture["teams"]["home"]
            away = fixture["teams"]["away"]

            home_matches = self.api.get_team_last_matches(home["id"], last=10)
            away_matches = self.api.get_team_last_matches(away["id"], last=10)

            home_stats = StatisticsAnalyzer.analyze_team_form(home_matches, home["id"])
            away_stats = StatisticsAnalyzer.analyze_team_form(away_matches, away["id"])

            if not home_stats or not away_stats or home_stats["valid_matches"] < 5 or away_stats["valid_matches"] < 5:
                rejected_count += 1
                continue

            if home_stats["over_15_ratio"] < MIN_OVER_15_RATIO or away_stats["over_15_ratio"] < MIN_OVER_15_RATIO:
                rejected_count += 1
                continue

            prediction = Over15Predictor.estimate_probability(home_stats, away_stats)
            if prediction["probability"] < MIN_PROBABILITY:
                rejected_count += 1
                continue

            match_data = {
                "home_team": home["name"],
                "away_team": away["name"],
                "time": fixture["fixture"]["date"],
                "league": fixture["league"]["name"],
                "home_stats": home_stats,
                "away_stats": away_stats,
                "prediction": prediction
            }
            selected_matches.append(match_data)

            if len(selected_matches) >= MAX_MATCHES_PER_DAY:
                break

        selected_matches.sort(key=lambda x: x["prediction"]["probability"], reverse=True)

        return {
            "matches": selected_matches,
            "analyzed": len(fixtures),
            "retained": len(selected_matches),
            "rejected": rejected_count
        }
