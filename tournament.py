import requests
import re
from urllib.parse import urlencode
import datetime

from _data_management import _prepare_params
from _enums import TournamentType, TournamentRankedBy, TournamentGrandFinalModifier, MatchState
from _errors import *
from match import Match
from participant import Participant


class Matches:
    def __init__(self, base_api_link, auth_info, tournament_id):
        self.base_api_link = base_api_link
        self.auth_info = auth_info
        self.tournament_id = tournament_id

    def get_all(self, state = None, participant_id = None):
        req_link = self.base_api_link + f"tournaments/{self.tournament_id}/matches.json"

        data = {}
        if participant_id:
            if isinstance(participant_id, Participant):
                participant_id = participant_id.id
            else:
                if not isinstance(participant_id, int):
                    raise BadArgument('Parameter `participant_id` must be of type int')
            data['participant_id'] = participant_id

        if state:
            if not isinstance(state, MatchState):
                try:
                    state = MatchState(state)
                except:
                    raise BadArgument(f"Parameter `state` is invalid, valid Types: {', '.join(['`{}`'.format(i.value) for i in list(MatchState)])}")

            data['state'] = state.name

        url_params = ""
        if len(data.keys()) > 0:
            url_params = "?" + urlencode(_prepare_params(data))

        req = requests.get(req_link + url_params, auth = self.auth_info)
        if not req.status_code == 200:
            raise HTTPException(req.status_code)
        else:
            return [Match(match_data, self.base_link, self.auth_info) for match_data in req.json()]

# A Tournament object. Contains all information on a tournament
# as well as methods relating to acting on a tournament.
class Tournament:
    def __init__(self, raw_tournament_data, base_link, auth_info):
        # There are 80 attributes here. This is getting out of hand.
        raw_tournament_data = raw_tournament_data['tournament']

        self.api_base_link = base_link
        self.auth_info = auth_info
        self.id = raw_tournament_data['id']
        self.name = raw_tournament_data['name']
        self.description = raw_tournament_data['description']
        self.tournament_type = TournamentType(raw_tournament_data['tournament_type'])

        if raw_tournament_data['started_at']:
            split_date = raw_tournament_data['started_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.started_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            self.started_at = raw_tournament_data['started_at']

        if raw_tournament_data['completed_at']:
            split_date = raw_tournament_data['completed_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.completed_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            self.completed_at = raw_tournament_data['completed_at']

        self.require_score_agreement = raw_tournament_data['require_score_agreement']
        self.notify_users_when_matches_open = raw_tournament_data['notify_users_when_matches_open']

        if raw_tournament_data['created_at']:
            split_date = raw_tournament_data['created_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.created_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            self.created_at = raw_tournament_data['created_at']

        if raw_tournament_data['updated_at']:
            split_date = raw_tournament_data['updated_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.updated_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            self.updated_at = raw_tournament_data['updated_at']

        self.state = raw_tournament_data['state']
        self.open_signup = raw_tournament_data['open_signup']
        self.notify_users_when_the_tournament_ends = raw_tournament_data['notify_users_when_the_tournament_ends']
        self.progress_meter = raw_tournament_data['progress_meter']
        self.quick_advance = raw_tournament_data['quick_advance']
        self.hold_third_place_match = raw_tournament_data['hold_third_place_match']
        self.pts_for_game_win = raw_tournament_data['pts_for_game_win']
        self.pts_for_game_tie = raw_tournament_data['pts_for_game_tie']
        self.pts_for_match_win = raw_tournament_data['pts_for_match_win']
        self.pts_for_match_tie = raw_tournament_data['pts_for_match_tie']
        self.pts_for_bye = raw_tournament_data['pts_for_bye']
        self.swiss_rounds = raw_tournament_data['swiss_rounds']
        self.private = raw_tournament_data['private']
        self.ranked_by = TournamentRankedBy(raw_tournament_data['ranked_by'])
        self.show_rounds = raw_tournament_data['show_rounds']
        self.hide_forum = raw_tournament_data['hide_forum']
        self.sequential_pairings = raw_tournament_data['sequential_pairings']
        self.accept_attachments = raw_tournament_data['accept_attachments']
        self.rr_pts_for_game_win = raw_tournament_data['rr_pts_for_game_win']
        self.rr_pts_for_game_tie = raw_tournament_data['rr_pts_for_game_tie']
        self.rr_pts_for_match_win = raw_tournament_data['rr_pts_for_match_win']
        self.rr_pts_for_match_tie = raw_tournament_data['rr_pts_for_match_tie']
        self.created_by_api = raw_tournament_data['created_by_api']
        self.credit_capped = raw_tournament_data['credit_capped']
        self.category = raw_tournament_data['category']
        self.hide_seeds = raw_tournament_data['hide_seeds']
        self.prediction_method = raw_tournament_data['prediction_method']
        self.predictions_opened_at = raw_tournament_data['predictions_opened_at']
        self.anonymous_voting = raw_tournament_data['anonymous_voting']
        self.max_predictions_per_user = raw_tournament_data['max_predictions_per_user']
        self.signup_cap = raw_tournament_data['signup_cap']
        self.game_id = raw_tournament_data['game_id']
        self.participants_count = raw_tournament_data['participants_count']
        self.group_stages_enabled = raw_tournament_data['group_stages_enabled']
        self.allow_participant_match_reporting = raw_tournament_data['allow_participant_match_reporting']
        self.teams = raw_tournament_data['teams']
        self.check_in_duration = raw_tournament_data['check_in_duration']

        if raw_tournament_data['start_at']:
            split_date = raw_tournament_data['start_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.start_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            self.start_at = raw_tournament_data['start_at']

        if raw_tournament_data['started_checking_in_at']:
            split_date = raw_tournament_data['started_checking_in_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.started_checking_in_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            self.started_checking_in_at = raw_tournament_data['started_checking_in_at']

        self.tie_breaks = raw_tournament_data['tie_breaks']

        if raw_tournament_data['locked_at']:
            split_date = raw_tournament_data['locked_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.locked_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            self.locked_at = raw_tournament_data['locked_at']

        self.event_id = raw_tournament_data['event_id']
        self.public_predictions_before_start_time = raw_tournament_data['public_predictions_before_start_time']
        self.ranked = raw_tournament_data['ranked']
        self.grand_finals_modifier = TournamentGrandFinalModifier(raw_tournament_data['grand_finals_modifier'])
        self.predict_the_losers_bracket = raw_tournament_data['predict_the_losers_bracket']
        self.spam = raw_tournament_data['spam']
        self.ham = raw_tournament_data['ham']
        self.rr_iterations = raw_tournament_data['rr_iterations']
        self.tournament_registration_id = raw_tournament_data['tournament_registration_id']
        self.donation_contest_enabled = raw_tournament_data['donation_contest_enabled']
        self.mandatory_donation = raw_tournament_data['mandatory_donation']
        self.non_elimination_tournament_data = raw_tournament_data['non_elimination_tournament_data']
        self.auto_assign_stations = raw_tournament_data['auto_assign_stations']
        self.only_start_matches_with_stations = raw_tournament_data['only_start_matches_with_stations']
        self.registration_fee = raw_tournament_data['registration_fee']
        self.registration_type = raw_tournament_data['registration_type']
        self.split_participants = raw_tournament_data['split_participants']
        self.description_source = raw_tournament_data['description_source']
        self.subdomain = raw_tournament_data['subdomain']
        self.url = raw_tournament_data['full_challonge_url']
        self.image_url = raw_tournament_data['live_image_url']
        self.sign_up_url = raw_tournament_data['sign_up_url']
        self.review_before_finalizing = raw_tournament_data['review_before_finalizing']
        self.accepting_predictions = raw_tournament_data['accepting_predictions']
        self.participants_locked = raw_tournament_data['participants_locked']
        self.game = raw_tournament_data['game_name']
        self.participants_swappable = raw_tournament_data['participants_swappable']
        self.team_convertable = raw_tournament_data['team_convertable']
        self.group_stages_were_started = raw_tournament_data['group_stages_were_started']

        self.tournament_matches = Matches(self.api_base_link, self.auth_info, self.id)
        self.matches = []
        if 'matches' in raw_tournament_data.keys():
            for match in raw_tournament_data['matches']:
                self.matches.append(Match(match, self.base_api_link, self.auth_info))

        if 'participants' in raw_tournament_data.keys():
            self.participants = raw_tournament_data['participants']
        else:
            self.participants = None

    def abort_check_in(self, include_participants = False, include_matches = False):
        data = {
            "include_participants": int(include_participants),
            "include_matches": int(include_matches)
        }

        url_params = '?' + urlencode(_prepare_params(data))

        req_link = self.api_base_link + f"/tournaments/{self.id}/abort_check_in.json"
        req = requests.post(req_link + url_params, auth = self.auth_info)
        if not req.status_code == 200:
            try:
                errors = req.json()
                raise HTTPException(f"{req.status_code} - {errors['errors'][0]}")
            except:
                raise HTTPException(req.status_code)

    def delete(self):
        req = requests.delete(self.api_base_link + f"tournaments/{self.id}.json", auth = self.auth_info)
        if not req.status_code == 200:
            try:
                errors = req.json()
                raise HTTPException(f"{req.status_code} - {errors['errors'][0]}")
            except:
                raise HTTPException(req.status_code)

    def finalize(self, include_participants = False, include_matches = False):
        data = {
            "include_participants": int(include_participants),
            "include_matches": int(include_matches)
        }

        url_params = '?' + urlencode(_prepare_params(data))

        req_link = self.api_base_link + f"/tournaments/{self.id}/finalize.json"
        req = requests.post(req_link + url_params, auth = self.auth_info)
        if not req.status_code == 200:
            try:
                errors = req.json()
                raise HTTPException(f"{req.status_code} - {errors['errors'][0]}")
            except:
                raise HTTPException(req.status_code)

    def open_for_predictions(self, include_participants = False, include_matches = False):
        data = {
            "include_participants": int(include_participants),
            "include_matches": int(include_matches)
        }

        url_params = '?' + urlencode(_prepare_params(data))

        req_link = self.api_base_link + f"/tournaments/{self.id}/open_for_predictions.json"
        req = requests.post(req_link + url_params, auth = self.auth_info)
        if not req.status_code == 200:
            try:
                errors = req.json()
                raise HTTPException(f"{req.status_code} - {errors['errors'][0]}")
            except:
                raise HTTPException(req.status_code)

    def process_check_ins(self, include_participants = False, include_matches = False):
        data = {
            "include_participants": int(include_participants),
            "include_matches": int(include_matches)
        }

        url_params = '?' + urlencode(_prepare_params(data))

        req_link = self.api_base_link + f"/tournaments/{self.id}/process_check_ins.json"
        req = requests.post(req_link + url_params, auth = self.auth_info)
        if not req.status_code == 200:
            try:
                errors = req.json()
                raise HTTPException(f"{req.status_code} - {errors['errors'][0]}")
            except:
                raise HTTPException(req.status_code)

    def reset(self, include_participants = False, include_matches = False):
        data = {
            "include_participants": int(include_participants),
            "include_matches": int(include_matches)
        }

        url_params = '?' + urlencode(_prepare_params(data))

        req_link = self.api_base_link + f"/tournaments/{self.id}/reset.json"
        req = requests.post(req_link + url_params, auth = self.auth_info)
        if not req.status_code == 200:
            try:
                errors = req.json()
                raise HTTPException(f"{req.status_code} - {errors['errors'][0]}")
            except:
                raise HTTPException(req.status_code)

    def start(self, include_participants = False, include_matches = False):
        data = {
            "include_participants": int(include_participants),
            "include_matches": int(include_matches)
        }

        url_params = '?' + urlencode(_prepare_params(data))

        req_link = self.api_base_link + f"/tournaments/{self.id}/start.json"
        req = requests.post(req_link + url_params, auth = self.auth_info)
        if not req.status_code == 200:
            try:
                errors = req.json()
                raise HTTPException(f"{req.status_code} - {errors['errors'][0]}")
            except:
                raise HTTPException(req.status_code)

    def update(self, name = None, url = None, tournament_type = None,
        subdomain = None, description = None, open_signup = None, hold_third_place_match = None,
        pts_for_match_win = None, pts_for_match_tie = None, pts_for_game_win = None, pts_for_game_tie = None,
        swiss_rounds = None, pts_for_bye = None, ranked_by = None, rr_pts_for_match_win = None,
        rr_pts_for_match_tie = None, rr_pts_for_game_win = None, rr_pts_for_game_tie = None,
        accept_attachments = None, hide_forum = None, show_rounds = None, private = None,
        notify_users_when_matches_open = None, notify_users_when_the_tournament_ends = None,
        sequential_pairings = None, signup_cap = None, start_at = None, check_in_duration = None,
        grand_finals_modifier = None):

        req_url = self.api_base_link + f"tournaments/{self.id}.json"

        data = {}

        if name is not None:
            if not isinstance(name, str):
                raise BadArgument('Parameter `name` must be of type str')
            if len(name) > 60:
                raise BadArgument('Parameter `name` cannot be more than 60 characters')
            data['name'] = name

        if url is not None:
            if not isinstance(url, str):
                raise BadArgument('Parameter `url` must be of type str')
            if len(url) > 60:
                raise BadArgument('Parameter `url` cannot be more than 60 characters')
            patterns = '^[a-zA-Z0-9_]*$'
            if not re.search(patterns,  url):
                raise BadArgument('Parameter `url` can only be letters, numbers, and underscores')
            data['url'] = url

        if tournament_type is not None:
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

        if len(data.keys()) > 0:
            url_params = '?' + urlencode(_prepare_params(data, 'tournament'))

            req = requests.put(req_url + url_params, auth = self.auth_info)
            if not req.status_code == 200:
                try:
                    errors = req.json()
                    raise HTTPException(f"{req.status_code} - {errors['errors'][0]}")
                except:
                    raise HTTPException(req.status_code)
            else:
                for i in data.keys():
                    if i == 'url':
                        setattr(self, i, "https://challonge.com/" + data[i])
                    else:
                        setattr(self, i, data[i])
        else:
            raise UserInputError()
