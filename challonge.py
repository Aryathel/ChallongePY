import requests
import re
from urllib.parse import urlencode
import datetime

from tournament import Tournament
from _data_management import _prepare_params
from _enums import TournamentType, TournamentRankedBy, TournamentGrandFinalModifier
from _errors import *


BASE_LINK = "https://api.challonge.com/v1/"


# A wrapper for all tournament related API calls.
class Tournaments:
    def __init__(self, auth_info):
        self.auth_info = auth_info
        self.base_link = BASE_LINK

    # Retrieves all tournaments visible to an account.
    def get_all(self, state = None, tournament_type = None, created_after = None, created_before = None, subdomain = None):
        req_url = self.base_link + f"tournaments.json"

        data = {}

        if state:
            if not isinstance(state, TournamentState):
                try:
                    state = TournamentState(state)
                except:
                    raise BadArgument(f"Parameter `state` is invalid, valid Types: {', '.join(['`{}`'.format(i.value) for i in list(TournamentState)])}")

            data['state'] = state.name

        if tournament_type:
            if not isinstance(tournament_type, TournamentType):
                try:
                    tournament_type = TournamentType(tournament_type)
                except:
                    raise BadArgument(f"Parameter `tournament_type` is invalid, valid Types: {', '.join(['`{}`'.format(i.value) for i in list(TournamentType)])}")

            data['state'] = state.name

        if created_after:
            if isinstance(created_after, datetime.datetime):
                created_after = created_after.strftime('%Y-%m-%d')
            else:
                try:
                    datetime.datetime.strptime(created_after, '%Y-%m-%d')
                    created_after = created_after.strftime('%Y-%m-%d')
                except:
                    raise BadArgument(f"Parameter `created_after` must be a `datetime.datetime` object or a string in the format `YYYY-MM-DD`")
            data['created_after'] = created_after

        if created_before:
            if isinstance(created_before, datetime.datetime):
                created_before = created_before.strftime('%Y-%m-%d')
            else:
                try:
                    datetime.datetime.strptime(created_before, '%Y-%m-%d')
                    created_before = created_before.strftime('%Y-%m-%d')
                except:
                    raise BadArgument(f"Parameter `created_before` must be a `datetime.datetime` object or a string in the format `YYYY-MM-DD`")
            data['created_before'] = created_before

        if subdomain:
            if not isinstance(subdomain, str):
                raise BadArgument(f"Parameter `subdomain` must be of type str")
            if len(subdomain) > 60:
                raise BadArgument('Parameter `subdomain` cannot be more than 60 characters')
            patterns = '^[a-zA-Z0-9_]*$'
            if not re.search(patterns,  subdomain):
                raise BadArgument('Parameter `subdomain` can only be letters, numbers, and underscores')
            data['subdomain'] = subdomain

        url_params = ""
        if len(data.keys()) > 0:
            url_params = "?" + urlencode(_prepare_params(data))

        req = requests.get(req_url, auth = self.auth_info)
        if not req.status_code == 200:
            raise HTTPException(req.status_code)
        else:
            return [Tournament(tournament_data, self.base_link, self.auth_info) for tournament_data in req.json()]

    # Retrieves a specific tournament by ID
    def get(self, id, include_participants = False, include_matches = False):
        req_url = self.base_link + f"tournaments/{id}.json"

        data = {
            "include_participants": int(include_participants),
            "include_matches": int(include_matches)
        }

        url_params = '?' + urlencode(_prepare_params(data))

        req = requests.get(req_url + url_params, auth = self.auth_info)
        if not req.status_code == 200:
            raise HTTPException(req.status_code)
        else:
            return Tournament(req.json(), self.base_link, self.auth_info)

    # Create a tournament.
    def create(self, name, url, tournament_type = TournamentType('single elimination'),
        subdomain = None, description = None, open_signup = None, hold_third_place_match = None,
        pts_for_match_win = None, pts_for_match_tie = None, pts_for_game_win = None, pts_for_game_tie = None,
        swiss_rounds = None, pts_for_bye = None, ranked_by = None, rr_pts_for_match_win = None,
        rr_pts_for_match_tie = None, rr_pts_for_game_win = None, rr_pts_for_game_tie = None,
        accept_attachments = None, hide_forum = None, show_rounds = None, private = None,
        notify_users_when_matches_open = None, notify_users_when_the_tournament_ends = None,
        sequential_pairings = None, signup_cap = None, start_at = None, check_in_duration = None,
        grand_finals_modifier = None):
        req_url = self.base_link + "tournaments.json"

        data = {}

        if not isinstance(name, str):
            raise BadArgument('Parameter `name` must be of type str')
        if len(name) > 60:
            raise BadArgument('Parameter `name` cannot be more than 60 characters')
        data['name'] = name

        if not isinstance(url, str):
            raise BadArgument('Parameter `url` must be of type str')
        if len(url) > 60:
            raise BadArgument('Parameter `url` cannot be more than 60 characters')
        patterns = '^[a-zA-Z0-9_]*$'
        if not re.search(patterns,  url):
            raise BadArgument('Parameter `url` can only be letters, numbers, and underscores')
        data['url'] = url

        if not isinstance(tournament_type, TournamentType):
            try:
                tournament_type = TournamentType(tournament_type)
            except:
                raise BadArgument(f"Parameter `tournament_type` is invalid, valid Types: {', '.join(['`{}`'.format(i.value) for i in list(TournamentType)])}")
        data['tournament_type'] = tournament_type

        if subdomain is not None:
            patterns = '^[a-zA-Z0-9_]*$'
            if not re.search(patterns,  subdomain):
                raise BadArgument('Parameter `subdomain` can only be letters, numbers, and underscores')
            else:
                data['subdomain'] = subdomain

        if description is not None:
            if not isinstance(description, str):
                raise BadArgument('Parameter `description` must be of type str')
            else:
                data['description'] = description

        if open_signup is not None:
            if not isinstance(open_signup, bool):
                raise BadArgument('Parameter `open_signup` must be of type bool')
            else:
                data['open_signup'] = open_signup

        if hold_third_place_match is not None:
            if not isinstance(hold_third_place_match, bool):
                raise BadArgument('Parameter `hold_third_place_match` must be of type bool')
            else:
                data['hold_third_place_match'] = hold_third_place_match

        if pts_for_match_win is not None:
            if not (isinstance(pts_for_match_win, int) or isinstance(pts_for_match_win, float)):
                raise BadArgument('Parameter `hold_third_place_match` must be of type int or float')
            else:
                pts_for_match_win = round(float(pts_for_match_win), 1)
                data['pts_for_match_win'] = pts_for_match_win

        if pts_for_match_tie is not None:
            if not (isinstance(pts_for_match_tie, int) or isinstance(pts_for_match_tie, float)):
                raise BadArgument('Parameter `hold_third_place_match` must be of type int or float')
            else:
                pts_for_match_tie = round(float(pts_for_match_tie), 1)
                data['pts_for_match_tie'] = pts_for_match_tie

        if pts_for_game_win is not None:
            if not (isinstance(pts_for_game_win, int) or isinstance(pts_for_game_win, float)):
                raise BadArgument('Parameter `hold_third_place_match` must be of type int or float')
            else:
                pts_for_game_win = round(float(pts_for_game_win), 1)
                data['pts_for_game_win'] = pts_for_game_win

        if pts_for_game_tie is not None:
            if not (isinstance(pts_for_game_tie, int) or isinstance(pts_for_game_tie, float)):
                raise BadArgument('Parameter `hold_third_place_match` must be of type int or float')
            else:
                pts_for_game_tie = round(float(pts_for_game_tie), 1)
                data['pts_for_game_tie'] = pts_for_game_tie

        if rr_pts_for_match_win is not None:
            if not (isinstance(rr_pts_for_match_win, int) or isinstance(rr_pts_for_match_win, float)):
                raise BadArgument('Parameter `hold_third_place_match` must be of type int or float')
            else:
                rr_pts_for_match_win = round(float(rr_pts_for_match_win), 1)
                data['rr_pts_for_match_win'] = rr_pts_for_match_win

        if rr_pts_for_match_tie is not None:
            if not (isinstance(rr_pts_for_match_tie, int) or isinstance(rr_pts_for_match_tie, float)):
                raise BadArgument('Parameter `hold_third_place_match` must be of type int or float')
            else:
                rr_pts_for_match_tie = round(float(rr_pts_for_match_tie), 1)
                data['rr_pts_for_match_tie'] = rr_pts_for_match_tie

        if rr_pts_for_game_win is not None:
            if not (isinstance(rr_pts_for_game_win, int) or isinstance(rr_pts_for_game_win, float)):
                raise BadArgument('Parameter `hold_third_place_match` must be of type int or float')
            else:
                rr_pts_for_game_win = round(float(rr_pts_for_game_win), 1)
                data['rr_pts_for_game_win'] = rr_pts_for_game_win

        if rr_pts_for_game_tie is not None:
            if not (isinstance(rr_pts_for_game_tie, int) or isinstance(rr_pts_for_game_tie, float)):
                raise BadArgument('Parameter `hold_third_place_match` must be of type int or float')
            else:
                rr_pts_for_game_tie = round(float(rr_pts_for_game_tie), 1)
                data['rr_pts_for_game_tie'] = rr_pts_for_game_tie

        if pts_for_bye is not None:
            if not (isinstance(pts_for_bye, int) or isinstance(pts_for_bye, float)):
                raise BadArgument('Parameter `pts_for_bye` must be of type int or float')
            else:
                pts_for_bye = round(float(pts_for_bye), 1)
                data['pts_for_bye'] = pts_for_bye

        if swiss_rounds is not None:
            if not isinstance(swiss_rounds, int):
                raise BadArgument('Parameter `swiss_rounds` must be of type int')
            else:
                data['swiss_rounds'] = swiss_rounds

        if ranked_by is not None:
            if not isinstance(ranked_by, TournamentRankedBy):
                try:
                    ranked_by = TournamentRankedBy(ranked_by)
                except:
                    raise BadArgument(f"Parameter `ranked_by` is invalid, valid Types: {', '.join(['`{}`'.format(i.value) for i in list(TournamentRankedBy)])}")
                else:
                    data['ranked_by'] = ranked_by
            else:
                data['ranked_by'] = ranked_by

        if accept_attachments is not None:
            if not isinstance(accept_attachments, bool):
                raise BadArgument('Parameter `accept_attachments` must be of type bool')
            else:
                data['accept_attachments'] = accept_attachments

        if hide_forum is not None:
            if not isinstance(hide_forum, bool):
                raise BadArgument('Parameter `hide_forum` must be of type bool')
            else:
                data['hide_forum'] = hide_forum

        if show_rounds is not None:
            if not isinstance(show_rounds, bool):
                raise BadArgument('Parameter `show_rounds` must be of type bool')
            else:
                data['show_rounds'] = show_rounds

        if private is not None:
            if not isinstance(private, bool):
                raise BadArgument('Parameter `private` must be of type bool')
            else:
                data['private'] = private

        if notify_users_when_matches_open is not None:
            if not isinstance(notify_users_when_matches_open, bool):
                raise BadArgument('Parameter `notify_users_when_matches_open` must be of type bool')
            else:
                data['notify_users_when_matches_open'] = notify_users_when_matches_open

        if notify_users_when_the_tournament_ends is not None:
            if not isinstance(notify_users_when_the_tournament_ends, bool):
                raise BadArgument('Parameter `notify_users_when_the_tournament_ends` must be of type bool')
            else:
                data['notify_users_when_the_tournament_ends'] = notify_users_when_the_tournament_ends

        if sequential_pairings is not None:
            if not isinstance(sequential_pairings, bool):
                raise BadArgument('Parameter `sequential_pairings` must be of type bool')
            else:
                data['sequential_pairings'] = sequential_pairings

        if signup_cap is not None:
            if isinstance(signup_cap, int):
                raise BadArgument('Parameter `signup_cap` must be of type int')
            elif signup_cap > 256 or signup_cap < 1:
                raise BadArgument('Parameter `signup_cap` must be between the values 1 and 256')
            else:
                data['signup_cap'] = signup_cap

        if check_in_duration is not None:
            if not isinstance(check_in_duration, int):
                raise BadArgument('Parameter `check_in_duration` must be of type int')
            else:
                data['check_in_duration'] = check_in_duration

        if grand_finals_modifier is not None:
            if not isinstance(grand_finals_modifier, TournamentGrandFinalModifier):
                try:
                    grand_finals_modifier = TournamentGrandFinalModifier(grand_finals_modifier)
                except:
                    raise BadArgument(f"Parameter `grand_finals_modifier` is invalid, valid Types: {', '.join(['`{}`'.format(i.value) for i in list(TournamentGrandFinalModifier)])}")
                else:
                    data['grand_finals_modifier'] = grand_finals_modifier
            else:
                data['grand_finals_modifier'] = grand_finals_modifier


        url_params = '?' + urlencode(_prepare_params(data, 'tournament'))

        req = requests.post(req_url + url_params, auth = self.auth_info)
        if not req.status_code == 200:
            try:
                errors = req.json()
                raise HTTPException(f"{req.status_code} - {errors['errors'][0]}")
            except:
                raise HTTPException(req.status_code)
        else:
            return Tournament(req.json(), self.base_link, self.auth_info)

# An ovararching Challonge account object.
class Challonge:
    def __init__(self, username, api_key):
        self.auth_info = (username, api_key)
        self.base_link = BASE_LINK
        self.tournaments = Tournaments(self.auth_info)
