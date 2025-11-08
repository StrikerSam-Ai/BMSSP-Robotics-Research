# simulation/robot_sim.py

from algorithms.bmssp import bmssp_main
from algorithms.dijkstra import dijkstra

class Robot:
    def __init__(self, world, start=(0, 0), goal=(49, 49), mode="bmssp"):
        self.world = world
        self.x, self.y = start
        self.goal = goal
        self.mode = mode

    def calculate_path(self, graph, source, target):
        if self.mode == "bmssp":
            dist, pred, _ = bmssp_main(graph, source, mode="fast")
        else:
            dist, pred = dijkstra(graph, source)

        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = pred[curr]
        return list(reversed(path))
