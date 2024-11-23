import requests

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

def convert_player_names(matchup):
    players_points = matchup.get("players_points")
    #for player in players_points:
        #match_id_name(player)
    with open("/Users/jacobself/Github/DynastyBrosAI/SleeperData/players.json", "r") as f:
        player_data = json.load(f)
    enriched_player_points = {
        player_id: {
            "player_name": player_data.get(player_id, {}).get("player_name", "Unknown Player"),
            "points": points,
            "position": player_data.get(player_id, {}).get("player_position", "Unkown Player")
        }
        for player_id, points in players_points.items()
    }
    return enriched_player_points
    

def match_id_name(player):
    with open("players.json", "r") as f:
        player_data = json.load(f)
    enriched_player_points = {
        player_id: {
            "player_name": player_data["player_name"],
            "points": points,
            "position": player_data["player_position"]
        }
        for player_id, points in player
    }

def main():
    league_id = "1062786980259520512"
    week = "11"
    matchup_data = get_matchup_data(league_id, week)

    for matchup in matchup_data:
        convert_player_names(matchup)

if __name__ == "__main__":
    main()