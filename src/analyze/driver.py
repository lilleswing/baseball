from analyze.naive import Naive

__author__ = 'karl'


def create_naive_matrix():
    naive = Naive()
    matrix = naive.create_batter_matrix()
    for i in xrange(0, len(matrix)):
        row = matrix[i]
        for j in xrange(0, len(row)):
            value = matrix[i][j]
            if value != 0:
                print ("%d,%d:%f" % (i, j, value))


if __name__ == "__main__":
    create_naive_matrix()


