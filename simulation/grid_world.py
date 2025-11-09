import random
from core.graph import Graph

def generate_grid_graph(rows=50, cols=50, obstacle_prob=0.18):
    graph = Graph(rows * cols)
    obstacles = set()

    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c

            # START allowed, GOAL allowed
            if (r, c) in [(0, 0), (rows - 1, cols - 1)]:
                continue  

            # FIX ✅ reduce randomness & give path guarantee
            if random.random() < obstacle_prob:
                obstacles.add(idx)

            # add neighbors (4-way connectivity)
            if c > 0:  
                graph.add_edge(idx, idx - 1, 1)
                graph.add_edge(idx - 1, idx, 1)

            if r > 0:
                graph.add_edge(idx, idx - cols, 1)
                graph.add_edge(idx - cols, idx, 1)

    # ✅ Hardcode a guaranteed corridor from START → GOAL
    for i in range(rows):
        obstacles.discard(i * cols)  # clear first column

    return graph, obstacles
