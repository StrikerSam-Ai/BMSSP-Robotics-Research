"""
BMSSP → Pioneer P3DX CoppeliaSim Integration
Author: Sam (BMSSP Robotics Research – Case Study)
"""

import sys, os, time, math
from collections import deque

# ✅ Add repo root to import search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ✅ Internal project imports
from algorithms.bmssp import bmssp_main
from simulation.grid_world import generate_grid_graph

# ✅ CoppeliaSim ZMQ API
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


# ------------------------------------------------------------------------------------
# Convert grid cell to world coordinates of Pioneer robot
# ------------------------------------------------------------------------------------
def grid_to_world(r, c, scale=0.1):
    return [c * scale, r * scale, 0.138]  # z = robot height


# ------------------------------------------------------------------------------------
# Rotate robot towards next direction
# ------------------------------------------------------------------------------------
def rotate_robot(sim, robot, current, target):
    dx = target[0] - current[0]
    dy = target[1] - current[1]
    yaw = math.atan2(dy, dx)
    sim.setObjectOrientation(robot, [0, 0, yaw])
    time.sleep(0.1)  # small delay for visualization


# ------------------------------------------------------------------------------------
# Move robot smoothly to the next cell
# ------------------------------------------------------------------------------------
def move_robot(sim, robot, pos):
    sim.setObjectTargetPosition(robot, pos)
    time.sleep(0.5)  # ⏳ movement visible (slow motion)


# ------------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------------
if __name__ == "__main__":

    print("🔄 Connecting to CoppeliaSim ...")

    client = RemoteAPIClient()
    sim = client.getObject("sim")
    print("✅ Connected to CoppeliaSim")

    # Get Pioneer handle (change name here if your model name differs)
    robot = sim.getObject("/PioneerP3DX")
    print("✅ Robot handle acquired")

    # ------------------------------------------------------------------------------
    # Build grid & run BMSSP
    # ------------------------------------------------------------------------------
    graph, obstacles = generate_grid_graph(rows=50, cols=50, obstacle_prob=0.25)

    START = 0
    GOAL = 2499  # bottom-right corner 50x50 grid

    dist, pred, _ = bmssp_main(graph, START)

    # ------------------------------------------------------------------------------
#  Run BMSSP and reconstruct path safely
# ------------------------------------------------------------------------------

dist, pred, _ = bmssp_main(graph, START)

path = deque()
node = GOAL

# ✅ If GOAL unreachable, regenerate graph instead of crashing
if pred.get(node, None) is None:
    print("\n❌ No path found! Obstacles blocked the goal.")
    print("🔄 Regenerating new grid and trying again...\n")

    graph, obstacles = generate_grid_graph(rows=50, cols=50, obstacle_prob=0.20)
    dist, pred, _ = bmssp_main(graph, START)
    node = GOAL

# ✅ Safe reconstruction (avoid KeyError None)
while node is not None and pred.get(node, None) is not None:
    path.appendleft(node)
    node = pred.get(node, None)

# If path is empty, stop
if len(path) <= 1:
    print("⚠ Could not compute valid path even after retry.")
    sys.exit(0)

print(f"✅ Path length: {len(path)} nodes")

