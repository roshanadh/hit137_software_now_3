import pygame
import sys
import os
import random


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


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    #function for move space ship laser up and down
    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y <= height and self.y >= 0
    
    def collision(self, obj):
        return collide(self,obj)




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

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(x, y, self.laser_img)
            self.laser.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

## Player class
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


## Enemy ship
class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue" : (BLUE_SPACE_SHIP, BLUE_LASER)
               }
    def __init__(self, x, y,color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

## function check laser beam colid with spaceShip
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2, (offset_x, offset_y))

# main game loop
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    lost = False
    main_font = pygame.font.SysFont("ArialTimes New Roman", 40)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_lenght = 5
    enemy_vel = 5

    player_vel = 5
    player = Player(300, 650)

    clock = pygame.time.Clock()

    lost_count = 0

    #Create function within function
    def redraw_window():
        window_screen.blit(BG, (0,0))

        #Draw text show score and life
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"level: {level}", 1, (255,255,255))

        window_screen.blit(lives_label, (10, 10))
        window_screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        ##for enemy draw
        for enemy in enemies:
            enemy.draw(window_screen)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            window_screen.blit(lost_label, (WIDTH/2 -lost_label.get_width()/2, 350))

            

        player.draw(window_screen)

        
        pygame.display.update()




    while run:
        clock.tick(FPS)

        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        ## it stop screen to show lost text and exit loop
        if lost:
            if lost_count > FPS * 3:
                run = False
            else: 
                continue

        if len(enemies) == 0:
            level += 1
            wave_lenght += 5
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        ##key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left move
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right move
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up move
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # right move
            player.y += player_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

       




### Run when this file is executed
if __name__ == '__main__' :
    main()



