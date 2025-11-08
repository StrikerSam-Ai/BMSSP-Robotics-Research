# simulation/grid_world.py

import random

class GridWorld:
    def __init__(self, size=50, obstacle_probability=0.2):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.obstacle_prob = obstacle_probability

    def randomize_obstacles(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = 1 if random.random() < self.obstacle_prob else 0

    def add_dynamic_obstacle(self, x, y):
        self.grid[x][y] = 1

    def is_free(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] == 0
