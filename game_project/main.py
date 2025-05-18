import pygame

# initialze Pygame
pygame.init()

#DEFINE SIZE OF THE WINDOW
window_width, window_height = 1280, 720

window_surface = pygame.display.set_mode((window_width, window_height))

# SET TITLE
pygame.display.set_caption('My Game')

is_running = True


surface = pygame.Surface((100, 200))

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    
    window_surface.fill('gray')
    window_surface.blit(surface, (100, 150))
    pygame.display.update()

pygame.quit