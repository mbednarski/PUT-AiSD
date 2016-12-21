from Queue import Queue
import networkx as nx
import matplotlib.pyplot as plt

'''graph = {0: [1],
		 1: [2, 4],
		 2: [3],  #removed a
		 3: [2, 5],
		 4: [2, 3],
		 5: [0, 1, 2]}'''
graph = {0: [1],
		 1: [2, 4],
		 2: [3, 0],  #removed a
		 3: [2, 5],
		 4: [2, 3],
		 5: [0, 1, 2]}


def closes_cycle(g, a, b):
	return b in g[a]


def get_first_avaiable(gg, g, s):
	nbs = gg[g]
	for nb in nbs:
		if nb not in s:
			return nb
	return None


q = []


def hamiltonian_backend(g, v, visited,once):
	q.append(v)
	if len(q) == 6:
		if closes_cycle(g, v, 1):
			print 'cykl'
		else:
			print 'sciezka'
		print q
		if once:
			return True
	else:
		visited[v] = True
		for x in g[v]:
			if not visited[x]:
				found = hamiltonian_backend(g, x, visited, once)
				if found:
					return True
		visited[v] = False
	q.pop(-1)


def hamiltonian(g,once=False):
	v = [False] * len(g)
	return hamiltonian_backend(g, 1, v,once)



if __name__ == "__main__":
	hamiltonian(graph,once=True)
	G = nx.from_dict_of_lists(graph, create_using=nx.MultiDiGraph())
	nx.draw(G)
	plt.show()



