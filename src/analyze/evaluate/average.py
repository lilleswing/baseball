import os
from analyze.evaluate import split_events_by_game
from model import session
from analyze import pickleutil
import constants
from model.batter import Batter
from model.calculator import Calculator
from model.event import Event
from model.gameresult import GameResult

__author__ = 'karl'

event_data = None
batters = None


class AverageEvaluator:
    def __init__(self):
        self.matrices = self.__get_pickles()

    def evaluate(self):
        for matrix in self.matrices:
            self.__evaluate_matrix(matrix)

    def __evaluate_matrix(self, matrix):
        global event_data
        global batters
        if event_data is None:
            event_data = session.query(Event).all()
        if batters is None:
            batters = session.query(Batter).all()
        calculator = self.__get_calculator(matrix)
        game_results = list()
        for batter in batters:
            batter_results = self.get_batter_results(matrix, calculator, batter)
            game_results.extend(batter_results)
            if len(game_results) > constants.batch_size:
                session.add_all(game_results)
                game_results = list()
        session.add_all(game_results)
        session.commit()

    def __get_calculator(self, matrix):
        calculator = Calculator()
        calculator.algorithm_name = matrix.algorithm
        calculator.filter_name = matrix.matrix_filter
        session.add(calculator)
        session.commit()
        return calculator

    def get_batter_results(self, matrix, calculator, batter):
        batter_events = filter(lambda x: x.batter == batter.mlb_id, event_data)
        batter_events = split_events_by_game(batter_events)
        batter_results = list()
        for event_list in batter_events:
            total = 0
            for event in event_list:
                total += matrix.get_cell(event.batter, event.pitcher)
            game_results = GameResult()
            game_results.calculator = calculator.id
            game_results.mlb_id = batter.mlb_id
            game_results.player_type = constants.BATTER
            game_results.actions = len(event_list)
            game_results.score = total
            game_results.game = event_list[0].game_id
            batter_results.append(game_results)
        return batter_results

    def __get_pickles(self):
        folder = constants.raw_matrix_folder
        pickle_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        pickle_files = filter(lambda x: "average" in x, pickle_files)
        pickle_files = [os.path.join(folder, f) for f in pickle_files]
        return [pickleutil.get_cache(x) for x in pickle_files]


if __name__ == "__main__":
    a = AverageEvaluator()
    a.evaluate()
