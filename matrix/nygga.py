import numpy as np
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import Queue


BLACK = 0
GRAY = 1
WHITE = 2


class MatrixGraph:
	def __init__(self, n=10):
		self.show = False
		self.n = n
		self.matrix = np.zeros((n, n))
		self.color = n * [WHITE]
		self.dist = n * [-1]
		self.parent = n * [-1]


	def fill(self):
		p = self.n * (self.n - 1) / 2
		while p > 0:
			x = rnd.randint(0, self.n - 1)
			y = rnd.randint(0, self.n - 1)
			if self.matrix[y][x] == 1 or x == y:
				continue
			self.matrix[y][x] = 1
			#matrix[x][y] = 1
			p -= 1


	def neighbours(self, u):
		nyg = []
		for i in range(self.n):
			if self.matrix[u][i] == 1:
				nyg.append(i)
		return nyg


	def dfs(self, start):
		discovered = self.n * [False]
		self.dfs_back(start, discovered)


	def dfs_back(self, v, discovered):
		if self.show:
			print v
		discovered[v] = True
		for w in self.neighbours(v):
			if not discovered[w]:
				self.dfs_back(w, discovered)


	def bfs(self, s):
		for u in range(self.n):
			self.color[u] = WHITE
			self.dist[u] = 999999999
			self.parent[u] = None
		self.color[s] = GRAY
		self.dist[s] = 0
		self.parent[s] = None
		q = Queue.Queue()
		q.put(s)
		while not q.empty():
			u = q.get()
			for v in self.neighbours(u):
				if self.color[v] == WHITE:
					self.color[v] = GRAY
					self.dist[v] = self.dist[u] + 1
					self.parent[v] = u
					q.put(v)
			self.color[u] = BLACK
			if self.show:
				print u


if __name__ == "__main__":
	g = MatrixGraph(10)
	g.fill()
	g.show = True
	g.dfs(0)
	g.bfs(0)
	G = nx.from_numpy_matrix(g.matrix, create_using=nx.MultiDiGraph())
	nx.draw(G)
	plt.show()
