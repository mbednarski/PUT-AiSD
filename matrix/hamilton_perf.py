from sys import setrecursionlimit
from time import clock
from hamilton import hamiltonian
from nygga_list import ListGraph

import numpy as np

probe_sizes = [0.1, 0.2, 0.3, 0.4, 0.5,]

repeats = 3


def measure_exe_time(algo):
	start = clock()
	algo()
	stop = clock()
	return stop - start


def single_algo(algo, once):
	dd = np.zeros((1 + repeats, len(probe_sizes)))
	dd[0, :] = probe_sizes

	#to fill

	probeIndex = 0
	for probe in probe_sizes:
		print 'Probe size ', probe, '(Index ', probeIndex, ')...'
		matrix = ListGraph(15)
		matrix.fill(probe)
		for row in range(1, repeats + 1):
			print 'Repeat ', row, '...'
			try:
				start = clock()
				algo(matrix.graph, once)
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
	m = single_algo(hamiltonian, once=False)
	s = single_algo(hamiltonian, once=True)

	np.savetxt('hamilton_Single_15', s)
	np.savetxt('hamilton_Multi_15', s)
