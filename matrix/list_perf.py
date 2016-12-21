from sys import setrecursionlimit
from time import clock
from nygga_list import ListGraph

import numpy as np

probe_sizes = [int(x) for x in np.linspace(1, 1000, 15)]

repeats = 5


def measure_exe_time(algo):
    start = clock()
    algo()
    stop = clock()
    return stop - start


def single_algo(algo):
    dd = np.zeros((1 + repeats, len(probe_sizes)))
    dd[0, :] = probe_sizes

    #to fill

    probeIndex = 0
    for probe in probe_sizes:
        print 'Probe size ', probe, '(Index ', probeIndex, ')...'
        matrix = ListGraph(probe)
        matrix.fill()
        for row in range(1, repeats + 1):
            print 'Repeat ', row, '...'
            try:
                start = clock()
                algo(matrix, 0)
                stop = clock()
                perf = stop - start
                dd[row, probeIndex] = perf
                print perf
            except RuntimeError:
                dd[row, probeIndex] = -10

        probeIndex += 1

    return dd


if __name__ == '__main__':
    setrecursionlimit(999999)
    b = single_algo(ListGraph.bfs)
    d = single_algo(ListGraph.dfs)

    np.savetxt('bfs_list', b)
    np.savetxt('dfs_list', d)
