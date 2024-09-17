import cv2
import pyautogui
import threading
import tracking as tck

from tracking.utils import math
from tracking.utils.drawing import normalize_pixel

tck.init((1920, 1080), flags=tck.type.HAND_TRACKING)
pyautogui.FAILSAFE = False

hand_tck = tck.HandTracking(max_num_hands=1)
cap = tck.CONFIG.VIDEO_CAPTURE

mouse = pyautogui.position()
mouse = mouse.x, mouse.y

mouse_button = False

def mouse_move():
    while cap.isOpened:
        x, y = mouse
        if mouse_button:
            pyautogui.mouseDown(x, y)
        else:
            pyautogui.mouseUp(x, y)
mouse_thread = threading.Thread(target=mouse_move)
mouse_thread.start()

thumb_tip_index = tck.finger.get_tip(tck.finger.THUMB)
index_tip_index = tck.finger.get_tip(tck.finger.INDEX)

while cap.isOpened:
    hands = hand_tck.predict()
    frame = cap.frame
    height, width = frame.shape[:2]
    
    if hands:
        hand = hands[0]
        center = hand.center_palm()
        center = normalize_pixel(center[0], center[1], width, height)
        if center:
            cv2.circle(frame, center, 5, (0, 255, 0), -1)
            
            x, y = center[0] / width, center[1] / height
            x, y = 1 - x, y
            x, y = x * tck.CONFIG.SCREEN_WIDTH, y * tck.CONFIG.SCREEN_HEIGHT
            x, y = int(x), int(y)
            
            mouse = (x, y)
            
        thumb_tip = hand.landmarks._get_points([thumb_tip_index])[0]
        index_tip = hand.landmarks._get_points([index_tip_index])[0]
        
        thumb_tip_pixel = normalize_pixel(thumb_tip[0], thumb_tip[1], width, height)
        index_tip_pixel = normalize_pixel(index_tip[0], index_tip[1], width, height)
        
        if thumb_tip_pixel and index_tip_pixel:
            distance = math.euclidean_distance(thumb_tip, index_tip)
            mouse_button = distance < 0.05
            
            color = (255, 0, 0) if mouse_button else (0, 0, 255)
            cv2.line(frame, thumb_tip_pixel, index_tip_pixel, color, 3)
        else:
            mouse_button = False
    else:
        mouse_pos = pyautogui.position()
        mouse = mouse_pos.x, mouse_pos.y
        mouse_button = False
    
    cv2.imshow("Camera", frame)
    if cv2.waitKey(10) & 0xFF == 27:
        cap.close()
    
cv2.destroyAllWindows()
mouse_thread.join()