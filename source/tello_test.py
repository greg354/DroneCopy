from djitellopy import Tello
import cv2
import time
import os

def square_edge_photos(square_size):
    tello = Tello()
    tello.connect()
    
    print(f"Battery: {tello.get_battery()}%")
    
    tello.streamon()
    frame_read = tello.get_frame_read()
    
    os.makedirs('../data', exist_ok=True)
    
    tello.takeoff()
    time.sleep(3)
    
    sides = ['front', 'right', 'back', 'left']
    half_distance = min(50, square_size // 2)
    
    for side_num in range(4):
        side_name = sides[side_num]
        
        # Take photo at start of side
        frame = frame_read.frame
        cv2.imwrite(f'../data/{side_name}_image_1.jpg', frame)
        
        # Move halfway and take photo
        tello.move_right(half_distance)
        time.sleep(2)
        frame = frame_read.frame
        cv2.imwrite(f'../data/{side_name}_image_2.jpg', frame)
        
        # Move to corner and take photo
        tello.move_right(half_distance)
        time.sleep(2)
        frame = frame_read.frame
        cv2.imwrite(f'../data/{side_name}_image_3.jpg', frame)
        
        # Rotate 90 degrees counter-clockwise
        tello.rotate_counter_clockwise(90)
        time.sleep(2)
    
    tello.land()
    tello.streamoff()
    tello.end()

if __name__ == "__main__":
    square_edge_photos(100)