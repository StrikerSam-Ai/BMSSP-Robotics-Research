# core/graph.py

class Graph:
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.adj_list = {i: [] for i in range(num_nodes)}  # adjacency list

    @property
    def nodes(self):
        """BMSSP ke liye node list return karta hai"""
        return list(self.adj_list.keys())

    def add_edge(self, u, v, w=1):
        """Undirected weighted graph"""
        self.adj_list[u].append((v, w))
        self.adj_list[v].append((u, w))

    def neighbors(self, node):
        """Return neighbors like: [(nbr, weight), ...]"""
        return self.adj_list[node]

    def get_neighbors(self, node):
        """BMSSP ke compatible naming ke liye wrapper"""
        return self.neighbors(node)

    def remove_node(self, node):
        """Node remove + edges cleanup"""
        for key in list(self.adj_list.keys()):
            self.adj_list[key] = [(n, w) for (n, w) in self.adj_list[key] if n != node]
        self.adj_list.pop(node, None)
