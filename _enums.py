from aenum import MultiValueEnum

class TournamentType(MultiValueEnum):
    single_elimination = "single elimination", None
    double_elimination = "double elimination"
    round_robin = "round robin"
    swiss = "swiss"

class TournamentRankedBy(MultiValueEnum):
    match_wins = "match wins", None
    game_wins = "game wins"
    points_scored = "points scored"
    points_difference = "points difference"
    custom = "custom"

class TournamentGrandFinalModifier(MultiValueEnum):
    default = "", None
    single_match = 'single match'
    skip = 'skip'

class TournamentState(MultiValueEnum):
    all = "all", None
    pending = "pending"
    in_progress = "in progress"
    ended = 'ended'

class MatchState(MultiValueEnum):
    all = "all", None
    pending = 'pending'
    open = 'open'
    complete = 'complete'
