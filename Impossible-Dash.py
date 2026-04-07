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
# =====================
class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT - 60
        self.width = 40
        self.height = 40
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
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

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
            spawn_timer = 0

        # Update player
        player.update()

        # Collision detection
        player_rect = player.get_rect()

        # Update score
        score += 1

        # Draw everything
        player.draw(screen)


        # UI text
        score_text = font.render(f"Score: {score}", True, BLACK)
        death_text = font.render(f"Deaths: {deaths}", True, BLACK)

        screen.blit(score_text, (10, 10))
        screen.blit(death_text, (10, 40))

        pygame.display.update()


if __name__ == "__main__":
    main()
