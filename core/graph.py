# core/graph.py

from typing import List, Tuple, Dict

class Graph:
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.nodes = list(range(num_nodes))
        self.adj_list: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(num_nodes)}
        self.edges: List[Tuple[int, int, float]] = []

    @classmethod
    def from_edge_list(cls, num_nodes: int, edges: List[Tuple[int, int, float]]):
        graph = cls(num_nodes)
        for u, v, w in edges:
            graph.adj_list[u].append((v, w))
            graph.edges.append((u, v, w))
        return graph

    def get_neighbors(self, u: int) -> List[Tuple[int, float]]:
        return self.adj_list[u]
