import requests
from challonge import Challonge
from time import sleep
import os

API_KEY = os.environ['CHALLONGE_API_KEY']
API_USER = os.environ['CHALLONGE_API_USER']

TRIALS_TOURNEY_ID = 8158700

# Prepare a Challonge connection given a Username and API Key.
challonge_account = Challonge(username = API_USER, api_key = API_KEY)

# Get all tournaments on an account.
# tournament_list = challonge_account.tournaments.get_all()

# Get a specific tournament by ID or url
trials_tourney = challonge_account.tournaments.get(TRIALS_TOURNEY_ID, include_matches = True, include_participants = True)

# Create a tournament
#new_tournament = challonge_account.tournaments.create("Personal Tournament Test", 'api_tournament_test', pts_for_game_win = 1, pts_for_game_tie = 0.5, pts_for_match_win = 4, pts_for_match_tie = 2)

# Update a tournament's settings
# tournament.update(tournament_type = 'single elimination', grand_finals_modifier = "")

# Delete a tournament
# new_tournament.delete()

# Process check ins for a tournament
# tournament.process_check_ins()
print(trials_tourney.tournament_matches.get_all())
