import requests
from collections import defaultdict
import json

def get_matchup_data(league_id, week):
    """
    Fetches matchup data from the Sleeper API for a specific league and week.
    
    :param league_id: The Sleeper league ID (string).
    :param week: The week number (int).
    :return: Matchup data as a JSON object.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

    
def get_roster_owner(roster_id):
    with open("owners.json", "r") as f:
        roster_owners = json.load(f)
    roster_id_string = str(roster_id)
    team_name = roster_owners.get(roster_id_string, {}).get("team_name", "not found")

    return team_name

def convert_player_names(matchup):
    players_points = matchup.get("players_points")

    with open("players.json", "r") as f:
        player_data = json.load(f)
    enriched_player_points = {
        player_id: {
            "player_name": player_data.get(player_id, {}).get("player_name", "Unknown Player"),
            "points": points,
            "position": player_data.get(player_id, {}).get("player_position", "Unknown Player")
        }
        for player_id, points in players_points.items()
    }
    return enriched_player_points

def get_matchup_info(matchup):
    roster_id = matchup.get("roster_id")
    matchup_id = matchup.get("matchup_id")

    return roster_id, matchup_id

def starter_vs_bench(matchup, enriched_players_points):
    starters = []
    bench = []
    for key, value in enriched_players_points.items():
        if key in matchup.get("starters"):
            starters.append({key: value})
        else:
            bench.append({key: value})
    return starters, bench

def main():
    league_id = ""
    week = "13"
    matchup_data = get_matchup_data(league_id, week)

    starters_bench_data = []

    for matchup in matchup_data:
        roster_id, matchup_id = get_matchup_info(matchup)
        team_name = get_roster_owner(roster_id)
        enriched_players_points = convert_player_names(matchup)
        starters, bench = starter_vs_bench(matchup, enriched_players_points)
        starters_bench_data.append(
            {
                "team_name": team_name,
                "matchup_id": matchup_id,
                "points_for": matchup["points"],
                "starters": starters,
                "bench": bench
            }
            )
    grouped_matchups = defaultdict(list)

    for entry in starters_bench_data:
        grouped_matchups[entry['matchup_id']].append(entry)

    grouped_matchups = dict(grouped_matchups)

    matchup_results = [
        {"matchup_id": matchup_id, "teams": teams}
        for matchup_id, teams in grouped_matchups.items()
    ]
    with open("matchup_results.json", "w") as json_file:
        json.dump(matchup_results, json_file, indent=4)


if __name__ == "__main__":
    main()