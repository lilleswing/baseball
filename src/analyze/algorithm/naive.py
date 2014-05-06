from analyze.draftkings.scorer import Scorer
from model import session
from model.batter import Batter
from model.batterpitchermatrix import BatterPitcherMatrix
from model.event import Event
from model.pitcher import Pitcher
import cPickle as pickle
import constants
import numpy
import os

__author__ = 'karl'

scorer = Scorer()

event_data = None


class Naive:
    """
    Returns a raw matrix using a naive average of all interactions between a pitcher and a batter
    """

    def __init__(self, force_recalculate=False):
        """
        force_recalculate to force a recalculation from DB instead of cached value
        """
        self.base_name = "naive"
        self.force_recalculate = force_recalculate
        self.batter_file_name = os.path.join(constants.raw_matrix_folder, "%s_batter.pickle" % self.base_name)
        self.pitcher_file_name = os.path.join(constants.raw_matrix_folder, "%s_pitcher.pickle" % self.base_name)

    def get_batter_matrix(self):
        if self.has_cache(self.batter_file_name):
            return self.get_cache(self.batter_file_name)
        global event_data
        if event_data is None:
            event_data = session.query(Event).all()
        batters = session.query(Batter).all()
        pitchers = session.query(Pitcher).all()

        matrix_data = numpy.zeros((len(batters), len(pitchers)))

        for i in xrange(0, len(batters)):
            batter = batters[i]
            batter_events = filter(lambda x: x.batter == batter.mlb_id, event_data)
            for j in xrange(0, len(pitchers)):
                pitcher = pitchers[j]
                sub_score = self.score_batter(batter_events, pitcher.mlb_id)
                matrix_data[i][j] = sub_score
        final_matrix = BatterPitcherMatrix(matrix_data, batters, pitchers)
        self.cache_matrix(final_matrix, self.batter_file_name)
        return final_matrix

    def score_batter(self, batter_events, pitcher_id):
        events = filter(lambda x: x.pitcher == pitcher_id, batter_events)
        if not events:
            return -1
        total = 0
        for event in events:
            total += scorer.score_batter(event.event)
        return float(total) / float(len(events))

    def cache_matrix(self, matrix, filename):
        fout = open(filename, 'wb')
        pickle.dump(matrix, fout)
        fout.close()

    def has_cache(self, filename):
        return not self.force_recalculate and os.path.isfile(filename)

    def get_cache(self, filename):
        fin = open(filename, 'rb')
        pickle.load(fin)
        fin.close()
