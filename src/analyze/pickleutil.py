import cPickle as pickle
import os

__author__ = 'karl'


def cache_matrix(matrix, filename):
    fout = open(filename, 'wb')
    pickle.dump(matrix, fout)
    fout.close()


def has_cache(filename):
    return os.path.isfile(filename)


def get_cache(filename):
    fin = open(filename, 'rb')
    obj = pickle.load(fin)
    fin.close()
    return obj