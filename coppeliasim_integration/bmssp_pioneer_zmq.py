from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.getObject('sim')

print("[OK] Connected to CoppeliaSim via ZMQ API")

# ✅ Correct object name from your screenshot
robot = sim.getObject('/PioneerP3DX')
print("[OK] Robot handle acquired")

# Example: Move robot a bit forward and rotate
sim.setObjectPosition(robot, -1, [0.5, 0.5, 0.138])  # adjust z to match ground clearance
time.sleep(1)

# Rotate robot by 90 degrees (yaw)
sim.setObjectOrientation(robot, -1, [0, 0, 1.57])
time.sleep(1)

print("✅ Movement Completed")
