__author__ = 'karl'

score_key = {
    "Strikeout": 0,
    "Groundout": 0,
    "Pop Out": 0,
    "Flyout": 0,
    "Single": 3,
    "Double": 5,
    "Walk": 2,
    "Forceout": 0,
    "Home Run": 10,
    "Grounded Into DP": 0,
    "Sac Bunt": 0,
    "Sac Fly": 0,
    "Lineout": 0,
    "Triple": 8,
    "Hit By Pitch": 2,
    "Strikeout - DP": 0,
    "Field Error": 0,
    "Bunt Groundout": 0,
    "Runner Out": 0,
    "Fielders Choice Out": 0,
    "Intent Walk": 2,
    "Double Play": 0,
    "Fielders Choice": 0,
    "Fan interference": 0,
    "Catcher Interference": 0
}


class Scorer:
    def score(self, event_string):
        if event_string not in score_key:
            return 0
        return score_key[event_string]


