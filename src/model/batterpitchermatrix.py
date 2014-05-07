import constants

__author__ = 'leswing'


class BatterPitcherMatrix:
    BATTER_ORIENTATION = "batter"
    PITCHER_ORIENTATION = "pitcher"

    def __init__(self, matrix, batters, pitchers, orientation, algorithm=None, matrix_filter=None):
        """
        NOTE(LESWING) eventually put in algorithm and filters here
        """
        self.orientation = orientation
        self.algorithm = algorithm
        self.matrix_filter = matrix_filter
        self.matrix = matrix
        self.batters = batters
        self.pitchers = pitchers

    def get_cell(self, batter_mlbid, pitcher_mlbid):
        """
        Gets a cell in the matrix given the mlbid of the batter
        and pitcher
        TODO(LESWING) rewrite with a hash lookup for speed
        TODO(LESWING) this is really really bad
        """
        bat_index = 0
        pit_index = 0
        while self.batters[bat_index].mlb_id != batter_mlbid:
            bat_index += 1
        while self.pitchers[pit_index].mlb_id != pitcher_mlbid:
            pit_index += 1
        if self.orientation == constants.BATTER:
            return self.matrix[bat_index][pit_index]
        return self.matrix[pit_index][bat_index]
