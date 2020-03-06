import datetime
from _enums import MatchState

class Match:
    def __init__(self, raw_match_data, base_api_link, auth_info):
        raw_match_data = raw_match_data['match']

        self.base_api_link = base_api_link
        self.auth_info = auth_info

        self.attachment_count = raw_match_data['attachment_count']

        if raw_match_data['created_at']:
            split_date = raw_match_data['created_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.created_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
        else:
            self.created_at = raw_match_data['created_at']

        self.group_id = raw_match_data['group_id']
        self.has_attachment = raw_match_data['has_attachment']
        self.id = raw_match_data['id']
        self.identifier = raw_match_data['identifier']
        self.location = raw_match_data['location']
        self.loser_id = raw_match_data['loser_id']
        self.player1_id = raw_match_data['player1_id']
        self.player1_is_prereq_match_loser = raw_match_data['player1_is_prereq_match_loser']
        self.player1_prereq_match_id = raw_match_data['player1_prereq_match_id']
        self.player1_votes = raw_match_data['player1_votes']
        self.player2_id = raw_match_data['player2_id']
        self.player2_is_prereq_match_loser = raw_match_data['player2_is_prereq_match_loser']
        self.player2_prereq_match_id = raw_match_data['player2_prereq_match_id']
        self.player2_votes = raw_match_data['player2_votes']
        self.round = raw_match_data['round']

        if raw_match_data['scheduled_time']:
            split_date = raw_match_data['scheduled_time'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.scheduled_time = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
        else:
            self.scheduled_time = raw_match_data['scheduled_time']

        if raw_match_data['started_at']:
            split_date = raw_match_data['started_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.started_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
        else:
            self.started_at = raw_match_data['started_at']

        self.state = MatchState(raw_match_data['state'])

        self.tournament_id = raw_match_data['tournament_id']

        if raw_match_data['underway_at']:
            split_date = raw_match_data['underway_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.underway_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
        else:
            self.underway_at = raw_match_data['underway_at']

        if raw_match_data['updated_at']:
            split_date = raw_match_data['updated_at'].split(':')
            date_str = ":".join(split_date[:-1]) + split_date[-1]
            self.updated_at = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
        else:
            self.updated_at = raw_match_data['updated_at']

        self.winnder_id = raw_match_data['winnder_id']
        self.prerequisite_match_ids_csv = raw_match_data['prerequisite_match_ids_csv']
        self.scores_csv = raw_match_data['scores_csv']
