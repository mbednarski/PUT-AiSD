import numpy as np
import random as rnd
import Queue as qlib

guard_range = 40
guard_base = 500.


def linear_cost(dist):
	assert (dist >= 0, "Negative distance!")
	if dist == 0:
		cost = 0
	elif dist <= guard_range:
		cost = int(dist * (-guard_base / guard_range) + guard_base)
	else:
		cost = 0
	assert (cost >= 0)
	return cost


def quadratic_cost(dist):
	assert (dist >= 0)
	if dist == 0:
		cost = 0
	elif dist <= guard_range:
		cost = int(guard_range ** 2 / guard_base * (dist - guard_range) ** 2) + 1
	else:
		cost = 0
	assert (cost >= 0)
	return cost


def homographic_cost(dist):
	assert (dist >= 0)
	if dist == 0:
		cost = 0
	else:
		cost = int(guard_base / (dist + 1))
	assert (cost >= 0)
	return cost


class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	@staticmethod
	def random(bound):
		xr = rnd.randint(0, bound - 1)
		yr = rnd.randint(0, bound - 1)
		return Vector2(xr, yr)

	def distance(self, b):
		return abs(self.x - b.x) + abs(self.y - b.y)

	def neighbours(self):
		return [Vector2(self.x, self.y + 1),
				Vector2(self.x, self.y - 1),
				Vector2(self.x - 1, self.y),
				Vector2(self.x + 1, self.y)]

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __str__(self):
		return "%d %d" % self.x, self.y

	def __repr__(self):
		return "%d %d" % (self.x, self.y)


# -5: way
# -4: treasure
# -3: start
# -2: guard
# -1: guest
# 0+: guard potential

def get_val(mx, pos):
	return mx[pos.y][pos.x]


def set_val(mx, pos, v):
	mx[pos.y][pos.x] = v


class Museum:
	def __init__(self, n, guards_count=30, visitors_count=100, startingPos=None, treasurePos=None):
		self.matrix = np.zeros((n, n))
		self.n = n
		self.guards_count = guards_count
		self.visitors_count = visitors_count
		self.start_point = startingPos if startingPos is not None else Vector2(0, 0)
		self.target = treasurePos if treasurePos is not None else Vector2(n - 1, n - 1)
		self.put_value(self.start_point, -3)
		self.put_value(self.target, -4)


		#self.put_guard(Vector2(self.n / 2, self.n / 2))
		#self.append_field(Vector2(self.n / 2, self.n / 2))

		#self.put_guard(Vector2(0, 1))
		#self.append_field(Vector2(0, 1))

		self.put_guards(self.guards_count)
		self.put_visitors(visitors_count)
		self._max_cost = 1

	def put_guard(self, pos):
		assert (pos.x <= self.n)
		self.matrix[pos.y][pos.x] = -2

	@property
	def max_cost(self):
		return self.matrix.max()

	def is_prohibited(self, pos):
		assert (pos.x < self.n and pos.y < self.n)
		val = self.matrix[pos.y][pos.x]
		return val < 0

	def is_occupied(self, pos):
		assert (pos.x < self.n and pos.y < self.n)
		val = self.matrix[pos.y][pos.x]
		return val == -2 or val == -1

	def is_way(self, pos):
		return 0 <= pos.x < self.n and 0 <= pos.y < self.n and not self.is_occupied(pos)

	def put_value(self, pos, val):
		assert (pos.x < self.n and pos.y < self.n)
		self.matrix[pos.y][pos.x] = val

	def put_guards(self, n):
		assert (n <= self.n ** 2)
		put = 0
		while put < n:
			pos = Vector2.random(self.n)
			if self.is_prohibited(pos):
				continue
			self.put_value(pos, -2)
			self.append_field(pos)
			put += 1

	def put_visitors(self, n):
		assert (n <= self.n ** 2)
		put = 0
		while put < n:
			pos = Vector2.random(self.n)
			if self.is_prohibited(pos):
				continue
			self.put_value(pos, -1)
			put += 1

	def append_field(self, pos):
		for y in range(pos.y - guard_range, pos.y + guard_range):
			for x in range(pos.x - guard_range, pos.x + guard_range):
				if 0 <= x < self.n and 0 <= y < self.n:
					if not self.is_prohibited(Vector2(x, y)):
						cost = quadratic_cost(pos.distance(Vector2(x, y)))
						assert (cost >= 0)
						self.matrix[y][x] += cost

	def steal(self):
		n = self.n
		hard = np.ones((n, n)) * 99999999
		visited = np.zeros((n, n))
		q = [self.start_point]
		set_val(hard, self.start_point, 0)
		while len(q) > 0:
			#print q
			curr = q.pop(0)
			visited[curr.y][curr.x] = 1
			if self.get_value(curr) == -4:  # skarb
				break
			for nb in curr.neighbours():
				if not self.is_way(nb) or get_val(visited, nb) == 1:
					continue
				new_cost = 1 + get_val(hard, curr) + self.get_value(nb)
				old_cost = get_val(hard, nb)
				set_val(hard, nb, min(new_cost, old_cost))
				if nb not in q:
					q.append(nb)
			set_val(visited, curr, 1)
		np.set_printoptions(suppress=True)
		#print hard

		#done compuing now let's reverse!
		visited = np.zeros((n, n))
		iterator = self.target
		while True:
			if iterator is None:
				print "No chances!"
				break
			if iterator == self.start_point:
				break
			visited[iterator.y][iterator.x] = 1
			self.put_value(iterator, -5)
			#find minimal neighbour
			local_minima = 999999999
			next_way = None
			for nb in iterator.neighbours():
				#possibly redundant
				if not self.is_way(nb) or visited[nb.y][nb.x] == 1:
					continue
				nb_val = get_val(hard, nb)
				if nb_val < local_minima:
					local_minima = nb_val
					next_way = nb
			iterator = next_way

	def steal_no_destroy(self):
		n = self.n
		hard = np.ones((n, n)) * 99999999
		visited = np.zeros((n, n))
		q = [self.start_point]
		set_val(hard, self.start_point, 0)
		while len(q) > 0:
			#print q
			curr = q.pop(0)
			visited[curr.y][curr.x] = 1
			if self.get_value(curr) == -4:  # skarb
				break
			for nb in curr.neighbours():
				if not self.is_way(nb) or get_val(visited, nb) == 1:
					continue
				new_cost = 1 + get_val(hard, curr) + self.get_value(nb)
				old_cost = get_val(hard, nb)
				set_val(hard, nb, min(new_cost, old_cost))
				if nb not in q:
					q.append(nb)
			set_val(visited, curr, 1)
		np.set_printoptions(suppress=True)
		#print hard

		#done compuing now let's reverse!
		visited = np.zeros((n, n))
		iterator = self.target
		while True:
			if iterator is None:
				return False
			if iterator == self.start_point:
				break
			visited[iterator.y][iterator.x] = 1
			#self.put_value(iterator, -5) no marking changes
			#find minimal neighbour
			local_minima = 999999999
			next_way = None
			for nb in iterator.neighbours():
				#possibly redundant
				if not self.is_way(nb) or visited[nb.y][nb.x] == 1:
					continue
				nb_val = get_val(hard, nb)
				if nb_val < local_minima:
					local_minima = nb_val
					next_way = nb
			iterator = next_way
		return True

	def get_value(self, curr):
		return self.matrix[curr.y][curr.x]











