from analyze.algorithm.naive import Naive
from analyze.matrixfilter.average import AverageFilter
from model.batterpitchermatrix import BatterPitcherMatrix

__author__ = 'karl'


def create_naive_matrix():
    naive = Naive()
    matrix_filter = AverageFilter()
    bp_matrix = naive.get_batter_matrix()
    bp_matrix.orientation = BatterPitcherMatrix.BATTER_ORIENTATION
    matrix_filter.matrix_filter(bp_matrix)

if __name__ == "__main__":
    create_naive_matrix()


