import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.bmssp import bmssp_main
from simulation.grid_world import generate_grid_graph
from coppeliasim_zmqremoteapi_client import RemoteAPIClient




GRID_SIZE = 50
START = (0, 0)
GOAL = (49, 49)

# ---------------------------------------
# ✅ Connect to CoppeliaSim
# ---------------------------------------
client = RemoteAPIClient()
sim = client.getObject('sim')

print("✅ Connected to CoppeliaSim")

robot = sim.getObject('/PioneerP3DX')
print("✅ Robot handle acquired")

# ---------------------------------------
# ✅ Generate grid and compute path
# ---------------------------------------
graph, obstacles = generate_grid_graph()

dist, pred, _ = bmssp_main(graph, START)


path = []
cur = GOAL
while cur is not None:
    path.append(cur)
    cur = pred.get(cur)

path.reverse()  # start → goal

print(f"✅ Path length: {len(path)} nodes")

# ---------------------------------------
# ✅ Convert grid → world positions
# ---------------------------------------
def grid_to_world(cell):
    (x, y) = cell
    return [x * 0.1, y * 0.1, 0.138]  # adjust scaling and z based on your floor height

# ---------------------------------------
# ✅ Move robot along BMSSP path
# ---------------------------------------
for waypoint in path:
    target = grid_to_world(waypoint)

    # Move position
    sim.setObjectPosition(robot, -1, target)

    print(f"➡ Moving to {waypoint} => {target}")
    time.sleep(0.05)

print("\n🎉 Path following complete! Robot reached goal.")
