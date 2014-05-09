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
        self._create_lookup_tables()

    def get_cell(self, batter_mlbid, pitcher_mlbid):
        """
        Gets a cell in the matrix given the mlbid of the batter
        and pitcher
        """
        bat_index = self.batter_lookup[batter_mlbid]
        pit_index = self.pitcher_lookup[pitcher_mlbid]
        if self.orientation == constants.BATTER:
            return self.matrix[bat_index][pit_index]
        return self.matrix[pit_index][bat_index]

    def _create_lookup_tables(self):
        self.batter_lookup = self._create_lookup_table(self.batters)
        self.pitcher_lookup = self._create_lookup_table(self.pitchers)

    def _create_lookup_table(self, players):
        lookup = dict()
        for i in xrange(len(players)):
            player = players[i]
            lookup[player.mlb_id] = i
        return lookup
