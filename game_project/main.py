import pygame
import sys

# initialze Pygame
pygame.init()

#DEFINE SIZE OF THE WINDOW
window_width, window_height = 750, 750

## game screen size
window_screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
# SET TITLE
pygame.display.set_caption('My Game')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)

# Spaceship properties
ship_x = window_width // 10
ship_y = window_height // 10
ship_speed = 5

## Create Space ship
def draw_spaceShip(x, y):
    # Main body
    pygame.draw.polygon(window_screen, DARK_GRAY, [
        (x, y - 40),  # Tip
        (x - 25, y + 40),  # Left base
        (x + 25, y + 40)   # Right base
     ])
    # Cockpit (smaller triangle)
    pygame.draw.circle(window_screen, BLUE, 
        (x, y  + 15), 10)

     # Wings
    pygame.draw.polygon(window_screen, DARK_GRAY, [
        (x - 25, y + 10),
        (x - 45, y + 40),
        (x - 25, y + 40)
        ])
    pygame.draw.polygon(window_screen, DARK_GRAY, [
        (x + 25, y + 10),
        (x + 45, y + 40),
        (x + 25, y + 40)
        ])
    
    # Thruster flames
    pygame.draw.rect(window_screen, RED, (x - 8, y + 30, 16, 15))
    pygame.draw.rect(window_screen, RED, (x - 5, y + 45, 10, 10))




is_running = True
surface = pygame.Surface((100, 100))
 
## Game running loop 
while is_running:
    window_screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    

    # Movement controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_x > 40:
        ship_x -= ship_speed
    if keys[pygame.K_RIGHT] and ship_x < window_width - 40:
        ship_x += ship_speed
    if keys[pygame.K_UP] and ship_y > 60:
        ship_y -= ship_speed
    if keys[pygame.K_DOWN] and ship_y < window_height - 60:
        ship_y += ship_speed
    
    draw_spaceShip(ship_x, ship_y)

    #window_screen.fill('gray')
   # window_screen.blit(surface, (400, 400))
    pygame.display.update()
    clock.tick(60)

pygame.quit


