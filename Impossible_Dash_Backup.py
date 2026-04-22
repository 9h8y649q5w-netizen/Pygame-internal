''' Date: 8/04/2026

Author: Oliver Lloyd

About:

This is the back up version of Impossible Dash. 

first step is to create the gui,
second step is to create the player and the obstacles,
third step is to add the scoring system and the death counter,'''



from turtle import speed

import pygame 
import random
import sys
import json
import os 
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
#pygame.display.set_caption("Impossible Dash")

'''this definds a class that creates a button for the intro screen.'''

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (0, 200, 0)
        self.hover_color = (0, 255, 0)

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

"""this definds a function that creates the intro screen for the game."""

def intro_screen():
    intro_running = True

    button = Button("PLAY", WIDTH//2 - 100, HEIGHT//2 - 50, 200, 100)

    while intro_running:
        screen.fill((30, 30, 30))

        title_text = font.render("IMPOSSIBLE DASH", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))

        button.draw(screen, font)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if button.is_clicked(event):
                intro_running = False  # exit intro

        pygame.display.update()
        clock.tick(60)



"""this definds a function that loads and saves your high score when you die or quit the game."""

def load_high_scores():
    """Load existing high scores from file, or return an empty list."""
    if not os.path.exists(HIGH_SCORE_FILE):
        return []
    with open(HIGH_SCORE_FILE, "r") as file:
        return json.load(file)
def save_high_scores(high_scores):
    """Save high scores to file."""
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump(high_scores, file, indent= 2)
def add_score(new_score):
    """Add a new score, keep top 10 only."""
    high_scores = load_high_scores()
    high_scores.append(new_score)
    # Sort from highest to lowest
    high_scores.sort(reverse=True)
    high_scores = high_scores[:MAX_SCORES]
    save_high_scores(high_scores)
    return high_scores
def show_high_scores():
    """Display the current high scores."""
    high_scores = load_high_scores()
    print("\n=== HIGH SCORES ===")
    for i, score in enumerate(high_scores, start= 1):
        print(f"{i}. {score}")



clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

HIGH_SCORE_LIST = []

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ground
GROUND_HEIGHT = 20
GROUND_Y = HEIGHT - GROUND_HEIGHT

# Gravity
GRAVITY = 0.6


"""this difinds a class that will help us create levels."""
class LevelItem:
    def __init__(self, speed_scale = 1, width_scale = 1, obstacle = None, height_scale = 1):
        self.width_scale = width_scale
        self.speed_scale = speed_scale
        self.obstacle = obstacle
        self.height_scale = height_scale


# =====================
# Player Class


''' This definds the player object which creates an object that the player can control, if the user presses the space bar,
the object will jump, if the user makes the object tuch another object the user will die.'''
# =====================
class Player:
    def __init__(self):
        self.x = 100
        self.width = 40
        self.height = 40
        self.y = GROUND_Y - self.height
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
        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    # =====================
# Obstacle Class

''' This this definds an object which the player can jump on or over. '''

# =====================
class Obstacle:
    def __init__(self, speed_scale = 1, width_scale = 1, height_scale = 1):
        self.type = "Platform"
        self.speed = 5
        self.speed_scale = speed_scale
        self.width = 40 * width_scale
        self.height = 40
        self.height_scale = height_scale
        self.image = pygame.transform.scale(pygame.image.load("assets/Object.png"), (self.width, self.height))

        self.x = WIDTH
        self.y = GROUND_Y - (self.height * self.height_scale)

        self.speed = self.speed * speed_scale

    def reset(self):
        self.x = WIDTH

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  

    def off_screen(self):
        return self.x < -self.width

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

"""this definds an kill object which if the player tuches it the user will die."""

class KillObject(Obstacle):
    def __init__(self, speed_scale = 1, width_scale = 1, height_scale = 1):
        super().__init__(speed_scale, width_scale, height_scale)

        self.type = "KillObject"

         # Load image with correct size
        self.image = pygame.transform.scale(
            pygame.image.load("assets/KillObject.png"),
            (self.width, self.height)
        )

       # Set size FIRST
        self.width = 40 * width_scale
        self.height = 30 * height_scale

        # FORCE correct ground alignment
        self.y = GROUND_Y - (self.height * self.height_scale) - 10



"""this definds a function to checks if the player is on top of the object and if it isn't it will kill the user. """

def is_landing_on_top(player, obstacle):
    player_rect = player.get_rect()
    obstacle_rect = obstacle.get_rect()

    # Check horizontal overlap
    horizontal = player_rect.right > obstacle_rect.left and player_rect.left < obstacle_rect.right

    # Check if player is falling and touching top
    landing = (
        player.vel_y > 0 and  # falling
        player_rect.bottom <= obstacle_rect.top + 10 and
        player_rect.bottom >= obstacle_rect.top - 10
    )

    return horizontal and landing



HIGH_SCORE_FILE = "highscores.json"
MAX_SCORES = 10


""" this is the main game loop, it creates the player and the obstacles, it also checks for collisions and updates the score and death counter. """

# =====================
# Game Loop
# =====================
def main():
    pygame.display.set_caption("Impossible_Dash")
    
    player = Player()
    obstacles = []

    level = []
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 3, Obstacle, 2))
    level.append(LevelItem(1, 1, Obstacle, 3))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 2, Obstacle, 2))
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, Obstacle, 2))
    level.append(LevelItem(1, 1, Obstacle, 2))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, KillObject, 1))

    high_scores = load_high_scores()

    try:
        pygame.mixer.music.load("assets/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Music error:", e)

    try:
        jump_sound = pygame.mixer.Sound("assets/music2.mp3")
        jump_sound.set_volume(1.0)

    except Exception as e:
        print("Jump sound error:", e)
        jump_sound = None

    try: 
        death_sound = pygame.mixer.Sound("assets/dying.mp3")
        death_sound.set_volume(1.0)

    except Exception as e:
        print("Death sound error:", e)
        death_sound = None

    spawn_timer = 0
    score = 0
    deaths = 0
    running = True

    current_timer = 90

    level_index = 0

    while running:

        clock.tick(60)
        screen.fill(WHITE)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save high score even if the user quits the game
                save_high_scores(high_scores)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_high_scores(high_scores)
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE:
                    if player.on_ground:
                        player.jump()
                        if not jump_sound.get_num_channels():
                            jump_sound.play()

        # Spawn obstacles
        spawn_timer += 1
            
        if spawn_timer > current_timer:

# Reset level index if we reach the end of the level list
            if level_index == len(level):    
                level_index = 0
                obstacle.speed_scale += 55550
                 
               # current_timer -= 10  # Increase difficulty by reducing spawn time
               # if current_timer < 10:  # Prevent timer from going too low
               #     current_timer = 10

            obstacle = level[level_index].obstacle(level[level_index].speed_scale, level[level_index].width_scale, level[level_index].height_scale)  # Create obstacle based on current level item
            obstacle.reset()  # Reset obstacle position

            obstacles.append(obstacle)  # Spawn obstacle from lev

            level_index += 1
            spawn_timer = 0

        # Update player
        player.update()

        # Update obstacles
        for obstacle in obstacles:
           if (obstacle is not None):
                obstacle.update()

        # Remove off-screen obstacles
        obstacles = [o for o in obstacles if not o.off_screen()]

        # Collision detection
        player_rect = player.get_rect()
        for obstacle in obstacles:

            # Update score
            score += 1

            if is_landing_on_top(player, obstacle) and obstacle.type == "Platform":
                # Snap player to top of obstacle
                player.y = obstacle.y - player.height
                player.vel_y = 0
                player.on_ground = True
                break
            else: 
                if  (obstacle.type == "KillObject" or obstacle.type == "Platform") and player_rect.colliderect(obstacle.get_rect()):
                    if death_sound and not death_sound.get_num_channels():
                        death_sound.play()

                    deaths += 1
                    player = Player()
                    obstacles.clear()

                    level_index = 0
                    current_timer = 90

                    # Update high scores
                    high_scores = add_score(score)
                    save_high_scores(high_scores)

                    score = 0
                    break


        # Draw floor line
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 4)

        # Draw everything
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)


        # UI text
        score_text = font.render(f"Score: {score}", True, BLACK)
        death_text = font.render(f"Deaths: {deaths}", True, BLACK)
        save_high_scores_text = font.render(f"High Score: {high_scores[0] if high_scores else 0}", True, BLACK)

        screen.blit(score_text, (10, 10))
        screen.blit(death_text, (10, 40))
        screen.blit(save_high_scores_text, (10, 70))

        pygame.display.update()

if __name__ == "__main__":
    intro_screen()
    main()
