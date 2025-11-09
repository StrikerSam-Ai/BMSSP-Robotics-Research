from core.graph import Graph
import random

def generate_grid_graph(rows, cols, obstacle_prob=0.2):
    graph = Graph(rows * cols)
    obstacles = [0] * (rows * cols)

    def idx(r, c):
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            i = idx(r, c)

            if random.random() < obstacle_prob:
                obstacles[i] = 1
                continue

            if c < cols - 1:
                graph.add_edge(i, idx(r, c+1))
            if r < rows - 1:
                graph.add_edge(i, idx(r+1, c))

    return graph, obstacles
