1. Get the matchup for a week
  - the matchup api returns the following relevant data:
    - roster_ids in the matchup
    - the starter_ids
    - the bench_ids
2. Convert the roster_ids into team names
  - use the get rosters api endpoint to return roster_id and user_id
  - use the get users api endpoint to return username for given user_id
  - output is an object that has 
    - roster_id
        - user_id
        - user_name
        - co_owner_id
        - co_owner_name
3. Convert the starter_ids and the roster_ids into player names
4. Output should be an object like the following:
    - Matchup Id
        - Roster_id
            - team_name
            - Owner_user_name
            - Co-Owner_user_name
            - starter_points [{starter_name, points}}
            - bench_points [{bench_name, points}] *will need some fanciness to deduce this information since there is not a bench points field
        - Roster_id
