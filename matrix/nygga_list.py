import random as rnd

class ListGraph:
    def __init__(self, n):
        self.n = n
        self.graph = {}
        for i in range(n):
            self.graph[i] = []

    def fill(self,saturation):
        p = self.n * (self.n - 1) * saturation
        while p > 0:
            x = rnd.randint(0, self.n - 1)
            y = rnd.randint(0, self.n - 1)
            if y in self.graph[x] or x == y:
                continue
            self.graph[x].append(y)
            #matrix[x][y] = 1
            p -= 1

    def dfs(self, start, path=[]):
        stack = [start]
        while stack:
            current = stack.pop(0)
            if current not in path:
                path = path + [current]
                stack = self.graph[current] + stack
        return path


    def bfs(self, start, path=[]):
        queue = [start]
        while queue:
            vertex = queue.pop(0)
            if vertex not in path:
                path.append(vertex)
                queue.extend(list(set( self.graph[vertex]) - set(path)))
        return path


if __name__ == "__main__":
    g = ListGraph(10)
    g.fill()
    print g.dfs(0)
    print g.bfs(0)

