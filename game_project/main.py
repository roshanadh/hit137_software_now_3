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
        self.x = x  # Laser x position
        self.y = y  # Laser y position
        self.img = img  # Laser image
        self.mask = pygame.mask.from_surface(self.img)  # For collision detection

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))  # Draw laser on screen

    #function for move space ship laser up and down
    def move(self, vel):
        self.y += vel  # Move laser vertically

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)  # Check if laser is on screen
    
    def collision(self, obj):
        return collide(self,obj)  # Check collision with another object




## ship class
class Ship:
    def __init__(self, x, y,  health= 100):
        self.x = x  # Ship x position
        self.y = y  # Ship y position
        self.health = health  # Ship health
        self.ship_img = None  # Ship image
        self.laser_img = None  # Laser image for this ship
        self.lasers = []  # List of lasers fired
        self.cool_down_counter = 0  # Cooldown for shooting

    def draw(self, window):
        if self.ship_img is not None:
            window.blit(self.ship_img, (self.x, self.y))  # Draw ship
        for laser in self.lasers:
            laser.draw(window)  # Draw all lasers

    def shoot(self):
        if self.cool_down_counter == 0:
            # Center the laser on the ship
            laser = Laser(self.x + self.get_width()//2 - self.laser_img.get_width()//2, self.y-25, self.laser_img)
            self.lasers.append(laser)  # Add new laser
            self.cool_down_counter = 1  # Start cooldown

    def get_width(self):
        return self.ship_img.get_width()  # Get ship width
    def get_height(self):
        return self.ship_img.get_height()  # Get ship height

    def cooldown(self):
        if self.cool_down_counter > 0:
            self.cool_down_counter += 1  # Increase cooldown
        if self.cool_down_counter > 15:
            self.cool_down_counter = 0  # Reset cooldown
    ##move laser
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

## Player class
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACE_SHIP  # Set player image
        self.laser_img = YELLOW_LASER  # Set player laser image
        self.mask = pygame.mask.from_surface(self.ship_img)  # For collision
        self.max_health = health  # Store max health
        self.score = 0

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser) ## if laser off the screen remove
            else:
                for obj in objs: 
                    if laser.collision(obj): ## check the colsion of the laser with ship
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        # Increment score when an enemy is hit                       
                        self.score += 1  # Increase score by 1 for each hit
                        break
                         



## Enemy ship
class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue" : (BLUE_SPACE_SHIP, BLUE_LASER)
               }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]  # Set enemy image and laser
        self.mask = pygame.mask.from_surface(self.ship_img)  # For collision

    def move(self, vel):
        self.y += vel  # Move enemy down by velocity

    def hit(self):
        return True  # Enemy is destroyed on hit
    
    ## overwirte function for adjust sooting point for enmemy
    def shoot(self):
        if self.cool_down_counter == 0:
            # Center the laser on the ship
            laser = Laser(self.x + self.get_width()//2 - self.laser_img.get_width()//2, self.y+5, self.laser_img)
            self.lasers.append(laser)  # Add new laser
            self.cool_down_counter = 1  # Start cooldown

# function check laser beam collide with spaceShip
# Returns True if two objects collide using their masks
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# main game loop
def main():
    def show_instructions():
        """Display game instructions on the screen."""
        instructions = [
            "SPACE SHOOTER GAME",
            "",
            "Instructions:",
            "- Move: W/A/S/D or Arrow Keys",
            "- Shoot: Automatic",
            "- Destroy enemy ships to score points.",
            "- If an enemy reaches the bottom, you lose a life.",
            "- Game ends when all lives are lost.",
            "",
            "Press any key to start!"
        ]
        window_screen.blit(BG, (0,0))  # Draw background
        font = pygame.font.SysFont("Arial", 32)
        for i, line in enumerate(instructions):
            label = font.render(line, 1, (255,255,255))
            window_screen.blit(label, (WIDTH//2 - label.get_width()//2, 150 + i*40))  # Center text
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False  # Start game on key press

    show_instructions()  # Show instructions before game starts
    run = True
    FPS = 60  # Frames per second
    level = 0  # Current level
    score = 0  # Player score
    lost = False  # Game over flag
    main_font = pygame.font.SysFont("ArialTimes New Roman", 40)  # Main font
    lost_font = pygame.font.SysFont("comicsans", 60)  # Font for lost message

    enemies = []  # List of enemy ships
    wave_lenght = 5  # Initial number of enemies
    enemy_vel = 2  # Initial enemy speed

    player_vel = 5  # Player movement speed
    laser_vel = 4  # Laser moves up
    player = Player(300, 650)  # Create player

    clock = pygame.time.Clock()
    lost_count = 0

    def redraw_window():
        window_screen.blit(BG, (0,0))  # Draw background
        score_label = main_font.render(f"Score: {player.score}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        lives_label = main_font.render(f"Lives: {player.health//10}", 1, (255,255,255))
        window_screen.blit(score_label, (10, 10))  # Draw score
        window_screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))  # Draw level
        window_screen.blit(lives_label, (10, 50))  # Draw lives
        for enemy in enemies:
            enemy.draw(window_screen)  # Draw each enemy
        player.draw(window_screen)  # Draw player
        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            window_screen.blit(lost_label, (WIDTH/2 -lost_label.get_width()/2, 350))  # Draw lost message
       
        pygame.display.update()

    shoot_timer = 0
    shoot_delay = 20  # frames between shots

    while run:
        clock.tick(FPS)  # Maintain FPS
        redraw_window()  # Draw everything
        player.cooldown()  # Handle shooting cooldown
        if player.health <= 0:
            lost = True  # Player lost if health is 0
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False  # End game after showing lost message
            else:
                continue
        if len(enemies) == 0:
            level += 1  # Next level
            wave_lenght = min(5 + level * 2, 30)  # Cap the wave length
            enemy_vel = 1 + level * 0.5  # Increase enemy speed
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)  # Add new enemies
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Quit game
        keys = pygame.key.get_pressed()
        # Support both WASD and Arrow keys
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_vel > 0:
            player.x -= player_vel  # Move left
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel  # Move right
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - player_vel > 0:
            player.y -= player_vel  # Move up
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel  # Move down
        # Continuous firing
        shoot_timer += 1
        if shoot_timer >= shoot_delay:
            player.shoot()  # Shoot laser
            shoot_timer = 0
       
        ## for enemy space ship
        for enemy in enemies[:]:
            enemy.move(enemy_vel)  # Move enemy down
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            ## check collide with enemy and player ship
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                enemies.remove(enemy)  # Remove enemy if it reaches bottom
                player.health -= 10  # Decrease player health

            

         # Move player's lasers and check collision
        player.move_lasers(-laser_vel, enemies)

        if lost:
            # Show restart and exit buttons
            button_font = pygame.font.SysFont("Arial", 36)
            restart_label = button_font.render("Restart", 1, (255,255,255), (0,128,0))
            exit_label = button_font.render("Exit", 1, (255,255,255), (128,0,0))
            restart_rect = restart_label.get_rect(center=(WIDTH//2 - 100, 450))
            exit_rect = exit_label.get_rect(center=(WIDTH//2 + 100, 450))
            window_screen.blit(restart_label, restart_rect)  # Draw restart button
            window_screen.blit(exit_label, exit_rect)  # Draw exit button
            pygame.display.update()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if restart_rect.collidepoint(mx, my):
                            main()  # Restart the game
                            return
                        if exit_rect.collidepoint(mx, my):
                            pygame.quit()
                            sys.exit()

### Run when this file is executed
if __name__ == '__main__' :
    main()