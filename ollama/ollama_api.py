import json
import requests

def load_matchup_data(file_path):
    """Load matchup data from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_matchup_recap(matchup, ollama_model='llama3.2', max_tokens=100):
    """
    Write a super short, punchy fantasy football recap in one short paragraph.
    
    Args:
        matchup (dict): Matchup data containing team information
        ollama_model (str): Ollama model to use for generating recaps
    
    Returns:
        str: Humorous matchup recap
    """
    # Extract team details
    team1, team2 = matchup['teams']
    team1_name = team1['team_name']
    team2_name = team2['team_name']
    team1_score = team1['points_for']
    team2_score = team2['points_for']

    # Find top performers
    team1_top_player = max(team1['starters'], key=lambda x: list(x.values())[0]['points'])
    team1_bottom_player = min(team1['starters'], key=lambda x: list(x.values())[0]['points'])
    team1_top_bench = max(team1['bench'], key=lambda x: list(x.values())[0]['points'])
    team2_top_player = max(team2['starters'], key=lambda x: list(x.values())[0]['points'])
    team2_bottom_player = min(team2['starters'], key=lambda x: list(x.values())[0]['points'])
    team2_top_bench = max(team2['bench'], key=lambda x: list(x.values())[0]['points'])

    prompt = f"""Write a super short, punchy fantasy football recap in one tweet-length paragraph.
{team1_name} vs {team2_name}:
- {team1_name} scored {team1_score} pts. Their key players were (MVP: {list(team1_top_player.values())[0]['player_name']} - {list(team1_top_player.values())[0]['points']}), (Player that should have been benched: {list(team1_bottom_player.values())[0]['player_name']} - {list(team1_bottom_player.values())[0]['points']}), (Player that should have been started: {list(team1_top_bench.values())[0]['player_name']} - {list(team1_top_bench.values())[0]['points']} )
- {team2_name} scored {team2_score} pts. Their key players were (MVP: {list(team2_top_player.values())[0]['player_name']} - {list(team2_top_player.values())[0]['points']}), (Player that should have been benched: {list(team2_bottom_player.values())[0]['player_name']} - {list(team2_bottom_player.values())[0]['points']}), (Player that should have been started: {list(team2_top_bench.values())[0]['player_name']} - {list(team2_top_bench.values())[0]['points']})

Make it funny and dramatic!"""
    
    #print(prompt)

    # Send request to Ollama
    try:
        response = requests.post('http://localhost:11434/api/generate', 
                                 json={
                                     'model': ollama_model,
                                     'prompt': prompt,
                                     'stream': False
                                 })
        return response.json()['response']
    except Exception as e:
        return f"Error generating recap: {str(e)}"

def main():
    # Load matchup data
    matchup_data = load_matchup_data('matchup_results.json')

    # Generate and print recaps for each matchup
    for matchup in matchup_data:
        recap = generate_matchup_recap(matchup)
        print(f"{matchup['teams'][0]['team_name']} vs {matchup['teams'][1]['team_name']} Recap:\n{recap}\n{'='*50}\n")

if __name__ == "__main__":
    main()