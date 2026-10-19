import httpx
from config import FOOTBALL_API_KEY

BASE_URL = "https://v3.football.api-sports.io"

class FootballAPI:
    def __init__(self):
        self.headers = {
            "x-rapidapi-key": FOOTBALL_API_KEY,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }

    def get_fixtures(self, date_str: str):
        url = f"{BASE_URL}/fixtures"
        params = {"date": date_str}
        try:
            with httpx.Client(timeout=25.0) as client:
                response = client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("response", [])
        except Exception as e:
            print(f"Erreur API fixtures: {e}")
            return []

    def get_team_last_matches(self, team_id: int, last: int = 10):
        url = f"{BASE_URL}/fixtures"
        params = {"team": team_id, "last": last}
        try:
            with httpx.Client(timeout=25.0) as client:
                response = client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("response", [])
        except Exception as e:
            print(f"Erreur API team matches: {e}")
            return []
