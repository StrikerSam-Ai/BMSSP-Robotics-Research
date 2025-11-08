# simulation/visualize.py

import pygame
import random
from simulation.grid_world import GridWorld
from simulation.robot_sim import Robot
from core.graph import Graph

pygame.init()
size = 15
world_size = 50

win = pygame.display.set_mode((world_size * size, world_size * size))
pygame.display.set_caption("BMSSP Robotics Simulation")

world = GridWorld(world_size)
world.randomize_obstacles()

# build graph from grid
graph = Graph()
for i in range(world_size):
    for j in range(world_size):
        if world.is_free(i, j):
            node = i * world_size + j
            for dx, dy in [(1,0),(0,1),(-1,0),(0,-1)]:
                nx, ny = i + dx, j + dy
                if world.is_free(nx, ny):
                    graph.add_edge(node, nx * world_size + ny, 1)

robot = Robot(world)

running = True
path = robot.calculate_path(graph, 0, (world_size**2)-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # introduce dynamic obstacles
    if random.random() < 0.01:
        x, y = random.randint(0,49), random.randint(0,49)
        world.add_dynamic_obstacle(x, y)

    win.fill((0,0,0))

    # draw grid + obstacles
    for i in range(world_size):
        for j in range(world_size):
            color = (255,255,255)
            if world.grid[i][j] == 1:
                color = (0,0,0)
            pygame.draw.rect(win, color, (j * size, i * size, size-1, size-1))

    # draw path
    for node in path:
        px, py = node // world_size, node % world_size
        pygame.draw.rect(win, (0,0,255), (py * size, px * size, size-1, size-1))

    pygame.display.update()

pygame.quit()
