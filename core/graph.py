# core/graph.py

from typing import List, Tuple, Dict

class Graph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.nodes = list(range(num_nodes))
        self.edges = []
        self.adj_list = [[] for _ in range(num_nodes)]

    def add_edge(self, u, v, w=1):
        self.edges.append((u, v, w))
        self.adj_list[u].append((v, w))

    def get_neighbors(self, u):
        return self.adj_list[u]

