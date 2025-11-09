# core/graph.py

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = []
        self.adj_list = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.add(node)
            self.adj_list[node] = []

    def add_edge(self, src, dst, weight=1):
        if src in self.nodes and dst in self.nodes:
            self.edges.append((src, dst, weight))
            self.adj_list[src].append((dst, weight))

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)

        if node in self.adj_list:
            del self.adj_list[node]

        # Remove edges pointing to removed node
        for src in list(self.adj_list.keys()):
            self.adj_list[src] = [(dst, w) for dst, w in self.adj_list[src] if dst != node]
