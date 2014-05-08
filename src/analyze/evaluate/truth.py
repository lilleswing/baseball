from analyze.draftkings.scorer import Scorer
from analyze.evaluate import split_events_by_game
import constants
from model.batter import Batter
from model.calculator import Calculator
from model import session
from model.event import Event
from model.gameresult import GameResult

__author__ = 'karl'


class TruthEvaluator:
    name = "truth"

    def __init__(self, scorer=Scorer()):
        self.scorer = scorer
        self.calculator = self.__get_calculator()

    def evaluate(self):
        batters = session.query(Batter).all()
        game_results = list()
        for batter in batters:
            batter_results = self.get_batter_results(batter)
            game_results.extend(batter_results)
            if len(game_results) > constants.batch_size:
                session.add_all(game_results)
                game_results = list()
        session.add_all(game_results)
        session.commit()

    def get_batter_results(self, batter):
        batter_events = session.query(Event).filter(Event.batter == batter.mlb_id).order_by(Event.game_id).all()
        batter_events = split_events_by_game(batter_events)
        batter_results = list()
        for event_list in batter_events:
            total = 0
            for event in event_list:
                total += self.scorer.score_batter(event)
            game_results = GameResult()
            game_results.calculator = self.calculator.id
            game_results.mlb_id = batter.mlb_id
            game_results.player_type = constants.BATTER
            game_results.actions = len(event_list)
            game_results.score = total
            game_results.game = event_list[0].game_id  # guaranteed to have one element
            batter_results.append(game_results)
        return batter_results

    def __get_calculator(self):
        calculator = session.query(Calculator).filter(Calculator.algorithm_name == TruthEvaluator.name).first()
        if calculator is not None:
            return calculator
        calculator = Calculator()
        calculator.algorithm_name = TruthEvaluator.name
        calculator.filter_name = "none"
        session.add(calculator)
        session.commit()
        return calculator


if __name__ == "__main__":
    t = TruthEvaluator()
    t.evaluate()
