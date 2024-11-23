import requests
import json

url = "https://api.sleeper.app/v1/players/nfl?active=true"

def get_all_players():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def format_player_data(data):
    # create a json file with First Name, Last Name, Position
    player_dict = {}
    for player_id, player_data in data.items():
        first_name = player_data.get("first_name", "Unknown")
        last_name = player_data.get("last_name", "Unknown")
        fantasy_positions = player_data.get("fantasy_positions", [])
        
        # Safely handle missing or empty fantasy_positions
        player_position = fantasy_positions[0] if fantasy_positions else "Unknown"
        
        # Build the dictionary
        player_dict[player_data["player_id"]] = {
            "player_name": f"{first_name} {last_name}",
            "player_position": player_position
        }

    return player_dict



def main ():
    data = get_all_players()
    player_dict = format_player_data(data)

    # Save to a JSON file
    with open("players.json", "w") as json_file:
        json.dump(player_dict, json_file, indent=4)

if __name__ == "__main__":
    main()