import numpy as np
import pygame
import sys
import ctypes
import win32api
import win32con
import win32gui

import tracking as tck

COLUMNS = 5
ROWS    = 3
GAP     = 20

pygame.init()
tck.init((1920, 1080), flags=tck.type.FACE_TRACKING)

face_tck = tck.FaceTracking()
calibration = tck.Calibration((COLUMNS, ROWS))

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, display=1)

def move_window_to_monitor(monitor_number):
    hwnd = pygame.display.get_wm_info()["window"]
    monitors = win32api.EnumDisplayMonitors()
    if monitor_number < len(monitors):
        monitor_info = monitors[monitor_number]
        monitor_rect = monitor_info[2]
        x, y = monitor_rect[0], monitor_rect[1]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, screen_width, screen_height, win32con.SWP_NOACTIVATE | win32con.SWP_NOSIZE)

move_window_to_monitor(0)

x = 0
y = 0
running = True
def Next():
    global x
    global y
    global running
    x += 1
    if x == COLUMNS:
        x = 0
        y += 1
    
    if y == ROWS:
        running = False
        
last_update_time = pygame.time.get_ticks()
waiting_interval = 1000
update_interval = 2000
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            
    screen.fill((0, 0, 0))
    
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time >= waiting_interval:
        result, _ = face_tck.predict()
        if result:
            calibration.append((x, y), result[0])

    if current_time - last_update_time >= update_interval + waiting_interval:
        Next()
        last_update_time = current_time
        
    center_x = (screen_width - GAP) / (COLUMNS - 1) * x + GAP / 2
    center_y = (screen_height - GAP) / (ROWS - 1) * y + GAP / 2
    
    pygame.draw.circle(screen, (255, 0, 0), (int(center_x), int(center_y)), 10)
            
    pygame.display.flip()
    
pygame.quit()
calibration.save('face_model.json')