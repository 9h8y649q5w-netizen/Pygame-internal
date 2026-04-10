''' Date: 8/04/2026

Author: Oliver Lloyd

About:

Inspired by the game "Impossible Dash" by Nitrome and the rip of version of "Impossible Dash", "Geometry dash" by Robert Topala, 
this is a remake of the game in Python using Pygame but it much more harder.

first step is to create the gui,
second step is to create the player and the obstacles,
third step is to add the scoring system and the death counter,'''



import pygame 
import random
import sys

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side Scroller")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Gravity
GRAVITY = 0.6


# =====================
# Player Class


''' This definds the player object which creates an object that the player can control, if the user presses the space bar,
the object will jump, if the user makes the object tuch another object the user will die.'''
# =====================
class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT - 60
        self.width = 40
        self.height = 40
        self.image = pygame.transform.scale(pygame.image.load("assets/Character.png"), (self.width, self.height))
        self.vel_y = 0
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = -12
            self.on_ground = False

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        # Ground collision
        if self.y >= HEIGHT - 60:
            self.y = HEIGHT - 60
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    # =====================
# Obstacle Class

''' This this definds an object which the player can jump on or over, 
however I have not finished coding so if the user tuches the
object, the user will die. '''

# =====================
class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = random.randint(30, 60)
        self.x = WIDTH
        self.y = HEIGHT - self.height - 20
        self.image = pygame.transform.scale(pygame.image.load("assets/Object.png"), (self.width, self.height))
        self.speed = 5

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.x < -self.width

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# =====================
# Game Loop
# =====================
def main():
    player = Player()
    obstacles = []

    spawn_timer = 0
    score = 0
    deaths = 0
    running = True

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > 90:
            obstacles.append(Obstacle())
            spawn_timer = 0

        # Update player
        player.update()

        # Update obstacles
        for obstacle in obstacles:
            obstacle.update()

        # Remove off-screen obstacles
        obstacles = [o for o in obstacles if not o.off_screen()]

        # Collision detection
        player_rect = player.get_rect()
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.get_rect()):
                deaths += 1
                player = Player()
                obstacles.clear()
                score = 0
                break

        # Update score
        score += 1

        # Draw everything
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)



        # UI text
        score_text = font.render(f"Score: {score}", True, BLACK)
        death_text = font.render(f"Deaths: {deaths}", True, BLACK)

        screen.blit(score_text, (10, 10))
        screen.blit(death_text, (10, 40))

        pygame.display.update()


if __name__ == "__main__":
    main()
