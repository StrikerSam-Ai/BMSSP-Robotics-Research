# coppeliasim_integration/bmssp_pioneer_follow.py

from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from simulation.grid_world import generate_grid_graph
from algorithms.bmssp import bmssp_main
import time
import math

START = (0, 0)
GOAL = (49, 49)

def move_robot(sim, robot, path):
    for (x, y) in path:
        target_pos = [x * 0.1, y * 0.1, 0.138]  # scale to meters for CoppeliaSim
        sim.setObjectPosition(robot, -1, target_pos)
        time.sleep(0.1)

print("🔵 Connecting to CoppeliaSim ...")
client = RemoteAPIClient()
sim = client.getObject("sim")

print("🟢 Connected to CoppeliaSim")

robot = sim.getObject('/PioneerP3DX')
print("🟢 Robot handle acquired")

graph, obstacles = generate_grid_graph(rows=50, cols=50, obstacle_prob=0.15)

dist, pred, _ = bmssp_main(graph, START)

# Backtrack shortest predecessor chain
path = []
node = GOAL

while node in pred:
    path.append(node)
    node = pred[node]

path.reverse()

if len(path) == 0:
    print("❌ No path found")
else:
    print(f"✅ Path found — total {len(path)} steps")
    move_robot(sim, robot, path)
    print("🎉 Goal reached successfully!")
