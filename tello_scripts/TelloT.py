from djitellopy import Tello
import time

# Create Tello object
drone = Tello()

# Connect to the drone
print("Connecting to Tello...")
drone.connect()
print(f"Battery level: {drone.get_battery()}%")

try:
    # Takeoff
    drone.takeoff()
    print("Drone has taken off.")

    # Rise (ascend) to 50 cm
    drone.move_up(50)  # move_up uses centimeters
    print("Drone ascended 50 cm.")

    # Move forward 50 cm (0.5 meters)
    drone.move_forward(50)
    print("Drone moved forward 0.5 meters.")

    # Hover for 2 seconds
    time.sleep(1)
    print("Drone hovering for 2 seconds.")

    # Move backward 50 cm to original spot
    drone.move_back(50)
    print("Drone returned to original spot.")

    # Land
    drone.land()
    print("Drone has landed.")

except Exception as e:
    print(f"An error occurred: {e}")
    drone.land()