import pygame
import sys

from utils import rescale

COLUMNS = 5
ROWS    = 3

pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

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
update_interval = 5000
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            
    screen.fill((0, 0, 0))
    
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time >= update_interval:
        Next()
        last_update_time = current_time
    
    center_x = (screen_width / COLUMNS) * x + (screen_width / COLUMNS) / 2
    center_y = (screen_height / ROWS) * y + (screen_height / ROWS) / 2
    pygame.draw.circle(screen, (255, 0, 0), (int(center_x), int(center_y)), 10)
            
    pygame.display.flip()
    
pygame.quit()