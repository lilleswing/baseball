from analyze.draftkings.scorer import Scorer
import constants
from model import session
from model.batterpitchermatrix import BatterPitcherMatrix
from model.batter import Batter
from model.event import Event
from model.pitcher import Pitcher
import numpy

__author__ = 'karl'


class Naive:
    def create_matrix(self, scorer=Scorer()):
        self.scorer = scorer
        batters = session.query(Batter).all()
        pitchers = session.query(Pitcher).all()
        matrix_data = numpy.zeros((len(batters), len(pitchers)))

        for i in xrange(0, len(batters)):
            batter = batters[i]
            batter_events = session.query(Event).filter(Event.batter == batter.mlb_id).all()
            for j in xrange(0, len(pitchers)):
                pitcher = pitchers[j]
                sub_score = self.score(batter_events, pitcher.mlb_id)
                matrix_data[i][j] = sub_score
        return BatterPitcherMatrix(matrix_data, batters, pitchers, constants.BATTER)

    def score(self, batter_events, pitcher_id):
        """
        TODO(Leswing) figure out how to add a constant for stolen bases/getting caught stealing bases
        """
        #events = session.query(Event).filter(Event.batter == batter_id) \
        #    .filter(Event.pitcher == pitcher_id).all()
        events = filter(lambda x: x.pitcher == pitcher_id, batter_events)
        if not events:
            return 0
        total = 0
        for event in events:
            total += self.scorer.score_batter(event.event)
        return float(total) / float(len(events))

