try:
    from zmqRemoteApi import RemoteAPIClient
except Exception:
    import sys
    import subprocess
    print("[INFO] 'zmqRemoteApi' not found, attempting to install via pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "zmqRemoteApi"])
    from zmqRemoteApi import RemoteAPIClient
import time
import math

client = RemoteAPIClient()
sim = client.getObject('sim')

print("[OK] Connected to CoppeliaSim via ZMQ API")

robot = sim.getObject('/Pioneer_p3dx')
leftMotor = sim.getObject('/Pioneer_p3dx/leftMotor')
rightMotor = sim.getObject('/Pioneer_p3dx/rightMotor')

# BMSSP or Dijkstra ka path (example)
path = [
    [0.2, 0.2],
    [0.3, 0.5],
    [0.4, 0.8],
    [0.7, 1.0],
]

def move_to(x, y, speed=2.0):
    sim.setObjectPosition(robot, -1, [x, y, 0.05])

for waypoint in path:
    move_to(waypoint[0], waypoint[1])
    print("Moving to:", waypoint)
    time.sleep(0.4)

# Stop wheels
sim.setJointTargetVelocity(leftMotor, 0)
sim.setJointTargetVelocity(rightMotor, 0)

print("✅ Path execution finished!")
