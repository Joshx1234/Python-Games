"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path

# Initialize Pygame
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

class GameSettings:

        screen_width: int = 600
        screen_height: int = 300
        player_size: int = 10
        player_x: int = 100 # Initial x position of the player

        jump_velocity: float = 1.25
        white: tuple = (255, 255, 255)
        black: tuple = (0, 0, 0)

        gravity: float = 1.0 # acceleration, the change in velocity per frame
        d_t: float = 1.0/30
        m: float = 2.0 # mass of the player, used to calculate acceleration
screen = pygame.display.set_mode((GameSettings.screen_width, GameSettings.screen_height))
pygame.display.set_caption("Dino Jump")

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FPS
FPS = 60

# Player attributes
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 55

player_speed = 5

# Obstacle attributes
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 60
obstacle_speed = 1


# Font
font = pygame.font.SysFont(None, 36)


# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.load_img = pygame.image.load(images_dir / "cactus_9.png")
        self.image = pygame.transform.scale(self.load_img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = GameSettings.screen_width
        self.rect.y = GameSettings.screen_height - OBSTACLE_HEIGHT

        self.explosion = pygame.image.load(images_dir / "explosion1.gif")

    def update(self):
        self.rect.x -= obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.kill()

    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)


# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.v_y = 0
        self.load_img = pygame.image.load(images_dir / "dino_0.png")
        self.image = pygame.transform.scale(self.load_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GameSettings.screen_height - PLAYER_HEIGHT
        self.speed = player_speed

        self.is_jumping = False
    def update(self):
        
        d_v_y = 0
        keys = pygame.key.get_pressed()
        

        if keys[pygame.K_SPACE]:
            if self.is_jumping is False:
            # Jumping means that the player is going up. The top of the 
            # screen is y=0, and the bottom is y=SCREEN_HEIGHT. So, to go up,
            # we need to have a negative y velocity
                self.is_jumping = True
                d_v_y = -GameSettings.jump_velocity
                

        # acelleration in the y direction
        a_y = -GameSettings.gravity

        

        
        # Change in the velocity due to accelleration
        d_v_y += -a_y * GameSettings.d_t

        # Change in the position due to the velocity
        self.v_y += d_v_y

        if self.is_jumping is False:
            self.v_y = 0

        if self.is_jumping is True and self.rect.y >= GameSettings.screen_height - PLAYER_HEIGHT:
            self.is_jumping = False
            self.rect.y = GameSettings.screen_height - PLAYER_HEIGHT
   

       
        self.rect.y += self.v_y

# Create a player object
player = Player()
player_group = pygame.sprite.GroupSingle(player)



# Add obstacles periodically
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    
    if random.random() < 0.4:
        obstacle = Obstacle()
        obstacles.add(obstacle)
        return 1
    return 0


# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    game_over = False
    last_obstacle_time = pygame.time.get_ticks()

    # Group for obstacles
    obstacles = pygame.sprite.Group()


    obstacle_count = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Update player
        player.update()

        # Add obstacles and update
        if pygame.time.get_ticks() - last_obstacle_time > 500:
            last_obstacle_time = pygame.time.get_ticks()
            obstacle_count += add_obstacle(obstacles)
        
        obstacles.update()

        # Check for collisions
        collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
        if collider:
            collider[0].explode()
       
        # Draw everything
        screen.fill(WHITE)
        obstacles.draw(screen)
        player_group.draw(screen)

        # Display obstacle count
        obstacle_text = font.render(f"Obstacles: {obstacle_count}", True, BLACK)
        screen.blit(obstacle_text, (10, 10))

        pygame.display.update()
        # clock.tick(FPS)

    # Game over screen
    screen.fill(WHITE)

if __name__ == "__main__":
    game_loop()
