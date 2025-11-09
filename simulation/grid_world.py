from core.graph import Graph
import random

def generate_grid_graph(rows=50, cols=50, obstacle_prob=0.20):
    total_nodes = rows * cols
    graph = Graph(total_nodes)

    obstacles = set()
    for r in range(rows):
        for c in range(cols):
            node = r * cols + c

            if random.random() < obstacle_prob:  # create random obstacle
                obstacles.add(node)
                continue

            # Add edges (4-neighbors)
            if r > 0 and (node - cols) not in obstacles:
                graph.add_edge(node, node - cols)
            if r < rows - 1:
                graph.add_edge(node, node + cols)
            if c > 0 and (node - 1) not in obstacles:
                graph.add_edge(node, node - 1)
            if c < cols - 1:
                graph.add_edge(node, node + 1)

    return graph, obstacles
