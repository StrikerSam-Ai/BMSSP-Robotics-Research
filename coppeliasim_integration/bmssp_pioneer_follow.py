import sys, os, time, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from simulation.grid_world import generate_grid_graph
from algorithms.bmssp import bmssp_main


# -------------------------
# CONFIG
# -------------------------
ROWS = 50
COLS = 50
START = 0
GOAL = ROWS * COLS - 1
OBSTACLE_PROB = 0.22
# -------------------------


print("🔵 Connecting to CoppeliaSim ...")
client = RemoteAPIClient()
sim = client.getObject("sim")
print("🟢 Connected to CoppeliaSim")

robot = sim.getObject("/PioneerP3DX")
print("🟢 Robot handle acquired")


# ✅ Generate grid
graph, obstacles = generate_grid_graph(rows=ROWS, cols=COLS, obstacle_prob=OBSTACLE_PROB)

# Flatten obstacle list for drawing grid
flat_grid = [int(x) for x in obstacles]


# ✅ Run BMSSP
dist, pred, _ = bmssp_main(graph, START)

# Reconstruct shortest path
path = []
node = GOAL

while node != START:
    path.append(node)
    node = pred[node]
path.append(START)
path.reverse()

print(f"✅ Path computed! Length: {len(path)} nodes")

# -------------------------
# 🔥 Send data to CoppeliaSim (GRID + PATH)
# -------------------------
sim.setStringSignal("grid", json.dumps(flat_grid))
sim.setStringSignal("path", json.dumps(path))



# -------------------------
# 🚀 ROBOT MOVEMENT
# -------------------------
for p in path:
    r = p // COLS
    c = p % COLS
    world_x, world_y = r * 0.1, c * 0.1

    sim.setObjectPosition(robot, -1, [world_x, world_y, 0.138])
    time.sleep(0.25)

print("🏁 Path following complete!")
