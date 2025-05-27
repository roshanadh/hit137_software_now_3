import pygame
import sys
import os
pygame.font.init()

# initialze Pygame
pygame.init()

#DEFINE SIZE OF THE WINDOW
WIDTH, HEIGHT = 750, 750

## game screen size
window_screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# SET TITLE
pygame.display.set_caption('My Game')


# Load images for game
RED_SPACE_SHIP = pygame.image.load('game_project/image/ship_enemy_red.png').convert_alpha()
GREEN_SPACE_SHIP = pygame.image.load('game_project/image/ship_enemy_green.png').convert_alpha()
BLUE_SPACE_SHIP = pygame.image.load('game_project/image/ship_enemy_blue.png').convert_alpha()

# Player ship image
PLAYER_SPACE_SHIP = pygame.image.load('game_project/image/player_ship.png').convert_alpha()

# Lasers image
RED_LASER = pygame.image.load('game_project/image/laser_red.png').convert_alpha()
GREEN_LASER = pygame.image.load('game_project/image/laser_green.png').convert_alpha()
BLUE_LASER = pygame.image.load('game_project/image/laser_blue.png').convert_alpha()
YELLOW_LASER = pygame.image.load('game_project/image/laser_yellow.png').convert_alpha()

# Background
BG = pygame.transform.scale(pygame.image.load('game_project/image/background.png').convert_alpha(), (WIDTH, HEIGHT))


## ship class
class Ship:
    def __init__(self, x, y,  health= 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

## Player class
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health




# main game loop
def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("ArialTimes New Roman", 40)

    player_vel = 5
    player = Player(300, 650)

    clock = pygame.time.Clock()

    #Create function within function
    def redraw_window():
        window_screen.blit(BG, (0,0))

        #Draw text show score and life
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"level: {level}", 1, (255,255,255))

        window_screen.blit(lives_label, (10, 10))
        window_screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        player.draw(window_screen)
        pygame.display.update()




    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        ##key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left move
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + 50 < WIDTH: # right move
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up move
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + 50 < HEIGHT: # right move
            player.y += player_vel




### Run when this file is executed
if __name__ == '__main__' :
    main()



