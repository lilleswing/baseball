import os
from analyze import pickleutil
import constants

__author__ = 'karl'


class AverageFilter:
    """
    TODO(LESWING) figure out how to cache this intelligently
    """
    def __init__(self, force_recalculate=False):
        self.name = "average"
        self.force_recalculate = force_recalculate

    def matrix_filter(self, bp_matrix):
        bp_matrix.matrix_filter = self.name
        file_name = "%s_%s_%s.pickle" % (bp_matrix.matrix_filter, bp_matrix.algorithm, bp_matrix.orientation)
        file_name = os.path.join(constants.raw_matrix_folder, file_name)
        if not self.force_recalculate and pickleutil.has_cache(file_name):
            return pickleutil.get_cache(file_name)

        matrix = bp_matrix.matrix
        for i in xrange(len(matrix)):
            row = matrix[i]
            entries = 0
            total = 0
            for j in xrange(len(row)):
                val = matrix[i][j]
                if val != -1:
                    total += val
                    entries += 1
            average = self.get_average(total, entries)
            for j in xrange(len(row)):
                val = matrix[i][j]
                if val == -1:
                    matrix[i][j] = average

        pickleutil.cache_matrix(bp_matrix, file_name)
        return bp_matrix

    def get_average(self, total_value, num_entries):
        if num_entries == 0:
            return 0
        return float(total_value)/float(num_entries)
