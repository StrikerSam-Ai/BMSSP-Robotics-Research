import random
from core.graph import Graph

def generate_grid_graph(rows=50, cols=50, obstacle_prob=0.25):
    """
    Generates a grid graph where each cell is a node.
    Nodes are connected to their 4-neighbors (N, S, E, W).
    Some cells become obstacles (black tiles).
    """
    g = Graph(rows * cols)

    def node_id(r, c):  # map (r,c) -> node index
        return r * cols + c

    obstacles = set()

    for r in range(rows):
        for c in range(cols):
            if random.random() < obstacle_prob:
                obstacles.add(node_id(r, c))
                continue

            curr = node_id(r, c)

            if r > 0 and node_id(r - 1, c) not in obstacles:
                g.add_edge(curr, node_id(r - 1, c), 1)

            if c > 0 and node_id(r, c - 1) not in obstacles:
                g.add_edge(curr, node_id(r, c - 1), 1)

            if r < rows - 1 and node_id(r + 1, c) not in obstacles:
                g.add_edge(curr, node_id(r + 1, c), 1)

            if c < cols - 1 and node_id(r, c + 1) not in obstacles:
                g.add_edge(curr, node_id(r, c + 1), 1)

    return g, obstacles
