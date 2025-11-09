# simulation/grid_world.py

from core.graph import Graph
import random

def generate_grid_graph(rows=50, cols=50, obstacle_prob=0.15):
    graph = Graph()
    obstacles = []

    # Add nodes
    for x in range(rows):
        for y in range(cols):
            graph.add_node((x, y))

    # Add edges + mark obstacles
    for x in range(rows):
        for y in range(cols):

            # Random obstacle placement
            if random.random() < obstacle_prob:
                obstacles.append((x, y))
                graph.remove_node((x, y))
                continue

            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for nx, ny in neighbors:
                if (nx, ny) in graph.nodes:
                    graph.add_edge((x, y), (nx, ny), weight=1)

    return graph, obstacles
