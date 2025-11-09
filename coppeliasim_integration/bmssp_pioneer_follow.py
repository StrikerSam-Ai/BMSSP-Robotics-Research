import sys, os, time, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from simulation.grid_world import generate_grid_graph
from algorithms.bmssp import bmssp_main

# -------------------------------
# CONFIG
# -------------------------------
ROWS = 50
COLS = 50
START = 0
GOAL = ROWS * COLS - 1
OBSTACLE_PROB = 0.22
# -------------------------------

print("🔵 Connecting to CoppeliaSim ...")
client = RemoteAPIClient()
sim = client.getObject("sim")
print("🟢 Connected to CoppeliaSim")

robot = sim.getObject("/PioneerP3DX")
print("🟢 Robot handle acquired")


# ✅ Generate grid + obstacle matrix
graph, obstacles = generate_grid_graph(rows=ROWS, cols=COLS, obstacle_prob=OBSTACLE_PROB)

# ✅ Compute BMSSP path
dist, pred, _ = bmssp_main(graph, START)

if pred[GOAL] is None:
    print("❌ No path found")
    sim.setNamedInt32Signal("grid", [])  # send empty just in case
    sim.setNamedFloatSignal("path", [])
    exit()

print("✅ Path computed!")


# ✅ Convert BMSSP path (node indices → x,y coordinates)
path = []
node = GOAL

while node != START:
    path.append(node)
    node = pred[node]

path.append(START)
path.reverse()

print(f"➡️ Path length: {len(path)} nodes")


# ✅ Flatten obstacle grid for Lua (convert 2D → 1D vector)
flat_grid = [int(o) for o in obstacles]

# ✅ Flatten path into [x1, y1, x2, y2, ...]
flat_path = []
for p in path:
    r = p // COLS
    c = p % COLS
    flat_path += [float(r), float(c)]

# ✅ Send signals to CoppeliaSim for drawing
sim.setNamedInt32Signal("grid", flat_grid)
sim.setNamedFloatSignal("path", flat_path)


# ✅ Move robot in real world
for p in path:
    r = p // COLS
    c = p % COLS
    world_x, world_y = r * 0.1, c * 0.1
    sim.setObjectPosition(robot, -1, [world_x, world_y, 0.138])
    time.sleep(0.25)

print("🏁 Path following complete!")
