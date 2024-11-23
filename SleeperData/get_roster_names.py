import requests


def get_roster_ids(league_id):
    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def get_roster_owner_players(roster_data):
    team_info = {}
    for roster in roster_data:
        co_owners = roster.get("co_owners")
        co_owner = co_owners[0] if co_owners else "None"

        team_info[roster.get("roster_id")] = {
            "owner": roster.get("owner_id"),
            "co_owner": co_owner,
            "players": roster.get("players")
        }
    return team_info


def main():
    league_id = "1062786980259520512"
    roster_data = get_roster_ids(league_id)
    team_info = get_roster_owner_players(roster_data)


if __name__ == "__main__":
    main()