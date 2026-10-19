class StatisticsAnalyzer:
    @staticmethod
    def analyze_team_form(fixtures, team_id):
        over_15_count = 0
        total_goals_scored = 0
        total_goals_conceded = 0
        valid_matches = 0

        for match in fixtures:
            status = match["fixture"]["status"]["short"]
            if status != "FT":
                continue

            home = match["teams"]["home"]
            away = match["teams"]["away"]
            goals_home = match["goals"]["home"]
            goals_away = match["goals"]["away"]

            if goals_home is None or goals_away is None:
                continue

            total_match_goals = goals_home + goals_away
            if total_match_goals >= 2:
                over_15_count += 1

            if home["id"] == team_id:
                total_goals_scored += goals_home
                total_goals_conceded += goals_away
            else:
                total_goals_scored += goals_away
                total_goals_conceded += goals_home

            valid_matches += 1

        if valid_matches == 0:
            return None

        return {
            "valid_matches": valid_matches,
            "over_15_ratio": over_15_count / valid_matches,
            "over_15_count": over_15_count,
            "avg_scored": total_goals_scored / valid_matches,
            "avg_conceded": total_goals_conceded / valid_matches
        }
