_author__ = 'Mateusz Bednarski'

from hamilton import hamiltonian
from nygga_list import ListGraph
import numpy as np
import time

density = 10
sizes = np.linspace(2, 15, density).tolist()
guard_percentages = np.linspace(0.1, 0.5, density).tolist()
repeats = 3


def measure_stealing_time(victim):
	start = time.time()
	stolen = museum.steal_no_destroy()
	stop = time.time()
	return stop - start, stolen

def measure_creation(n, gc, vc, tp):
	start = time.time()
	mus = Museum(n, guards_count=gc, visitors_count=vc, treasurePos=tp)
	stop = time.time()
	return stop - start, mus


if __name__ == "__main__":

	results = np.zeros((len(guard_percentages), (len(sizes))))
	generations = np.zeros((len(guard_percentages), (len(sizes))))
	for n in range(len(sizes)):
		for m in range(len(guard_percentages)):

			size = int(sizes[n])
			saturation = guard_percentages[m]
			print "%d/%d  Map size: %dx%d Guards %.2f%%" % (
				n * len(sizes) + m + 1, len(sizes) * len(guard_percentages), size, size, saturation)
			#generate map
			hope = 3;
			while True:
				ct, museum = measure_creation(size, int(size * size * saturation / 100.),
								int(size * size * visitors_percentage / 100.),
								tp=Vector2(size - 1, size - 1))
				stolen = museum.steal_no_destroy()  #test pass
				print "Creation: %.2f" % ct
				if stolen or hope < 0:
					break
				hope -= 1
			measurement = []

			for r in range(1, repeats + 1):
				exe_time, foo = measure_stealing_time(museum)
				measurement.append(exe_time)
				print "\t%d/%d: %f s." % (r, repeats, exe_time)

			score = np.mean(measurement)

			results[m][n] = score
			generations[m][n] = ct

	np.savetxt('museum_results', results)
	np.savetxt('museum_creations', generations)


