import sys, os, time, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from simulation.grid_world import generate_grid_graph
from algorithms.bmssp import bmssp_main


ROWS = 50
COLS = 50
START = 0
GOAL = ROWS * COLS - 1
OBSTACLE_PROB = 0.22


print("🔵 Connecting to CoppeliaSim ...")
client = RemoteAPIClient()
sim = client.getObject("sim")
print("🟢 Connected to CoppeliaSim")

robot = sim.getObject("/PioneerP3DX")
print("🟢 Robot handle acquired")


# ✅ Generate grid & obstacles
graph, obstacles = generate_grid_graph(rows=ROWS, cols=COLS, obstacle_prob=OBSTACLE_PROB)
flat_grid = [int(x) for x in obstacles]


# ✅ Run BMSSP
dist, pred, _ = bmssp_main(graph, START)

if pred.get(GOAL) is None:
    print("❌ No path found! Obstacles blocked.")
    sim.setStringSignal("grid", json.dumps(flat_grid))
    sim.setStringSignal("path", "[]")
    exit()


# ✅ Extract path
path = []
node = GOAL
while node != START:
    path.append(node)
    node = pred[node]
path.append(START)
path.reverse()

print(f"✅ Path computed! Length: {len(path)} nodes")

# ✅ Send signals to CoppeliaSim
sim.setStringSignal("grid", json.dumps(flat_grid))
sim.setStringSignal("path", json.dumps(path))


# ✅ Move Robot
for p in path:
    r = p // COLS
    c = p % COLS
    sim.setObjectPosition(robot, -1, [r * 0.1, c * 0.1, 0.138])
    time.sleep(0.20)

print("🏁 Path following complete!")
