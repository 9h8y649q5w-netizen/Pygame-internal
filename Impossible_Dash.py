''' Date: 8/04/2026

Author: Oliver Lloyd

About:

Inspired by the game "Impossible Dash" by Nitrome and the rip of version of "Impossible Dash", "Geometry dash" by Robert Topala, 
this is a remake of the game in Python using Pygame but it much more harder.

Recent Updates (2026):
- Added shop system with 8 colored skins (red, blue, green, yellow, purple, orange, pink, cyan)
- Implemented settings screen with music toggle, score/coin/skin resets
- Dynamic coin value system that increases based on collection milestones
- Added sound effects for coin collection and spending
- Music controls with mute functionality
- Fallback system to backup version if main game crashes
- Enhanced UI with coin value display and improved controls

first step is to create the gui,
second step is to create the player and the obstacles,
third step is to add the scoring system and the death counter,'''





import pygame 
import random
import sys
import json
import os 
from pygame.locals import *
from turtle import speed

# Initialize Pygame
pygame.init()
pygame.mixer.init()
import time

last_frame_time = time.time()
FREEZE_LIMIT = 3  # seconds before we consider it frozen

"""this definds a function that will find out why the game is frozen and will stop the game if it is frozen."""

def freeze_screen():
    frozen = True
    debug_font = pygame.font.SysFont(None, 32)

    while frozen:
        screen.fill((0, 0, 40))  # dark blue

        title = font.render("GAME FROZEN", True, (255, 255, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        msg = debug_font.render("Press ESC to quit", True, (255, 255, 255))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


# Screen
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
#pygame.display.set_caption("Impossible Dash")

# Game States
GAME_STATE = "menu"

HIGH_SCORE_FILE = "player_data.json"
MAX_SCORES = 10

# Added game states for menu navigation (menu, game, shop, settings)
# Added persistent data storage with player_data.json including coins, skins, music settings

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

    play_button = Button("PLAY", WIDTH//2 - 100, HEIGHT//2 - 50, 200, 100)
    settings_button = Button("SETTINGS", WIDTH//2 - 100, HEIGHT//2 + 170, 200, 100)

    while intro_running:
        screen.fill((30, 30, 30))

        title_text = font.render("IMPOSSIBLE DASH", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))

        play_button.draw(screen, font)
        settings_button.draw(screen, font)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player_data = load_player_data()
                    save_player_data(player_data)
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                player_data = load_player_data()
                save_player_data(player_data)
                pygame.quit()
                sys.exit()

            if play_button.is_clicked(event):
                intro_running = False
                return "game"
            
            if settings_button.is_clicked(event):
                intro_running = False
                return "settings"

        pygame.display.update()
        clock.tick(60)



"""this definds a function that loads and saves your high score when you die or quit the game."""

def load_player_data():
    """Load existing player data from file, or return defaults."""
    if not os.path.exists(HIGH_SCORE_FILE):
        data = {"high_scores": [], "coins": 0, "skins": ["red"], "current_skin": "red", "music_muted": False}
        # Migrate old highscores.json
        old_file = "highscores.json"
        if os.path.exists(old_file):
            with open(old_file, "r") as f:
                old_scores = json.load(f)
                data["high_scores"] = old_scores
            os.rename(old_file, old_file + ".backup")  # Backup old file
        return data
    with open(HIGH_SCORE_FILE, "r") as file:
        data = json.load(file)
        # Ensure all keys exist
        if "high_scores" not in data:
            data["high_scores"] = []
        if "coins" not in data:
            data["coins"] = 0
        if "skins" not in data:
            data["skins"] = ["red"]
        if "current_skin" not in data:
            data["current_skin"] = "red"
        if "music_muted" not in data:
            data["music_muted"] = False
        return data

def save_player_data(data):
    """Save player data to file."""
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump(data, file, indent=2)

def add_score(new_score, data):
    """Add a new score, keep top 10 only."""
    high_scores = data["high_scores"]
    high_scores.append(new_score)
    # Sort from highest to lowest
    high_scores.sort(reverse=True)
    high_scores = high_scores[:MAX_SCORES]
    data["high_scores"] = high_scores
    return data

def add_coins(amount, data):
    """Add coins to player data."""
    data["coins"] += amount
    return data



clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)  # Smaller font for UI elements

HIGH_SCORE_LIST = []

# Colors - Base color definitions for UI and player skins
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Primary Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)

# Dark Variants
DARK_RED = (139, 0, 0)
DARK_BLUE = (0, 0, 139)
DARK_GREEN = (0, 100, 0)
DARK_YELLOW = (204, 204, 0)
DARK_PURPLE = (75, 0, 130)
DARK_ORANGE = (204, 102, 0)
DARK_PINK = (219, 39, 119)
DARK_CYAN = (0, 139, 139)

# Light Variants
LIGHT_RED = (255, 102, 102)
LIGHT_BLUE = (102, 178, 255)
LIGHT_GREEN = (102, 255, 102)
LIGHT_YELLOW = (255, 255, 153)
LIGHT_PURPLE = (200, 100, 255)
LIGHT_ORANGE = (255, 204, 102)
LIGHT_PINK = (255, 204, 229)
LIGHT_CYAN = (102, 255, 255)

# Additional Colors
MAGENTA = (255, 0, 255)
LIME = (50, 205, 50)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
BROWN = (165, 42, 42)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)
INDIGO = (75, 0, 130)
TURQUOISE = (64, 224, 208)

# Skin Color Mapping - Available skins that players can use
SKIN_COLORS = {
    # Default and Primary
    "default": RED,
    "red": RED,
    "blue": BLUE,
    "green": GREEN,
    "yellow": YELLOW,
    "purple": PURPLE,
    "orange": ORANGE,
    "pink": PINK,
    "cyan": CYAN,
    
    # Dark Variants
    "dark_red": DARK_RED,
    "dark_blue": DARK_BLUE,
    "dark_green": DARK_GREEN,
    "dark_yellow": DARK_YELLOW,
    "dark_purple": DARK_PURPLE,
    "dark_orange": DARK_ORANGE,
    "dark_pink": DARK_PINK,
    "dark_cyan": DARK_CYAN,
    
    # Light Variants
    "light_red": LIGHT_RED,
    "light_blue": LIGHT_BLUE,
    "light_green": LIGHT_GREEN,
    "light_yellow": LIGHT_YELLOW,
    "light_purple": LIGHT_PURPLE,
    "light_orange": LIGHT_ORANGE,
    "light_pink": LIGHT_PINK,
    "light_cyan": LIGHT_CYAN,
    
    # Additional Colors
    "magenta": MAGENTA,
    "lime": LIME,
    "navy": NAVY,
    "teal": TEAL,
    "brown": BROWN,
    "gold": GOLD,
    "gray": GRAY,
    "silver": SILVER,
    "indigo": INDIGO,
    "turquoise": TURQUOISE
}

# Dynamic coin value system: coin value increases based on collection milestones
# Increment intervals scale with total coins owned (100, 1000, 10000)
def get_coin_increment(total_coins):
    """Get the increment interval for coin value based on total coins."""
    if total_coins < 1000:
        return 100
    elif total_coins < 10000:
        return 1000
    else:
        return 10000
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
    def __init__(self, skin="default"):
        self.x = 100
        self.width = 40
        self.height = 40
        self.y = GROUND_Y - self.height
        self.skin = skin
        self.base_image = pygame.transform.scale(pygame.image.load("assets/Character.png"), (self.width, self.height))
        self.image = self.base_image.copy()
        self.apply_skin()  # Apply skin color tinting
        self.vel_y = 0
        self.on_ground = True

    def apply_skin(self):
        # Apply color tint to player sprite based on selected skin
        self.image = self.base_image.copy()
        if self.skin in SKIN_COLORS and SKIN_COLORS[self.skin]:
            color = SKIN_COLORS[self.skin]
            self.image.fill(color, special_flags=pygame.BLEND_MULT)

    def set_skin(self, skin):
        self.skin = skin
        self.apply_skin()

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


"""this definds a coin object which the player can collect for coins."""

class Coin(Obstacle):
    def __init__(self, speed_scale=1, width_scale=1, height_scale=1):
        super().__init__(speed_scale, width_scale, height_scale)

        self.type = "Coin"

        self.image = pygame.transform.scale(
            pygame.image.load("assets/pngtree-gold-dollar-coin-png-image_3975554.png"),
            (self.width, self.height)
        )

        self.width = 30 * width_scale
        self.height = 30 * height_scale
        self.y = GROUND_Y - self.height - 50  # Float above ground



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





def settings_screen():
    # Settings screen for game configuration
    # Allows toggling music, resetting scores/coins/skins
    player_data = load_player_data()
    running = True

    back_button = Button("BACK", WIDTH//2 - 100, HEIGHT - 100, 200, 50)
    mute_button = Button("TOGGLE MUSIC", WIDTH//2 - 150, 200, 300, 50)
    reset_scores_button = Button("RESET SCORES", WIDTH//2 - 150, 280, 300, 50)
    reset_coins_button = Button("RESET COINS", WIDTH//2 - 150, 360, 300, 50)
    reset_skins_button = Button("RESET SKINS", WIDTH//2 - 150, 440, 300, 50)

    while running:
        screen.fill((30, 30, 30))

        title_text = font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))

        music_status = "ON" if not player_data["music_muted"] else "OFF"
        music_text = font.render(f"Music: {music_status}", True, (255, 255, 255))
        screen.blit(music_text, (WIDTH//2 - music_text.get_width()//2, 150))

        mute_button.draw(screen, font)
        reset_scores_button.draw(screen, font)
        reset_coins_button.draw(screen, font)
        reset_skins_button.draw(screen, font)
        back_button.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_player_data(player_data)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_player_data(player_data)
                    return "menu"

            if back_button.is_clicked(event):
                save_player_data(player_data)
                running = False
                return "menu"

            if mute_button.is_clicked(event):
                player_data["music_muted"] = not player_data["music_muted"]

            if reset_scores_button.is_clicked(event):
                player_data["high_scores"] = []

            if reset_coins_button.is_clicked(event):
                player_data["coins"] = 0

            if reset_skins_button.is_clicked(event):
                player_data["skins"] = ["red"]
                player_data["current_skin"] = "red"

        pygame.display.update()
        clock.tick(60)

def main():
    pygame.display.set_caption("Impossible_Dash")
    
    player_data = load_player_data()
    player = Player(player_data["current_skin"])
    obstacles = []

    level = []
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, Coin, 1))
    level.append(LevelItem(1, 3, Obstacle, 2))
    level.append(LevelItem(1, 1, Obstacle, 3))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, Coin, 2))
    level.append(LevelItem(1, 2, Obstacle, 2))
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, Coin, 1))
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, Obstacle, 2))
    level.append(LevelItem(1, 1, Obstacle, 2))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, Obstacle, 3))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, KillObject, 1))
    level.append(LevelItem(1, 1, Obstacle, 1))
    level.append(LevelItem(1, 1, Obstacle, 2))
    level.append(LevelItem(1, 1, KillObject, 1))

    player_data = load_player_data()
    high_scores = player_data["high_scores"]

    try:
        pygame.mixer.music.load("assets/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.stop()  # Ensure stopped before playing
        pygame.mixer.music.play(-1)
        if player_data["music_muted"]:
            pygame.mixer.music.set_volume(0)
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

    try:
        coin_collect_sound = pygame.mixer.Sound("assets/chieuk-coin-257878.mp3")
        coin_collect_sound.set_volume(1.0)

    except Exception as e:
        print("Coin collect sound error:", e)
        coin_collect_sound = None

    spawn_timer = 0
    score = 0
    deaths = 0
    coins_collected = 0
    coin_value = 1  # Dynamic coin value, increases with collection milestones
    last_increment_coins = 0  # Tracks last milestone for value increases
    running = True
    info_message = ""

    current_timer = 40

    level_index = 0

    while running:

        clock.tick(60)
        screen.fill(WHITE)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save data
                player_data["high_scores"] = high_scores
                player_data["coins"] += coins_collected
                save_player_data(player_data)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player_data["high_scores"] = high_scores
                    player_data["coins"] += coins_collected
                    save_player_data(player_data)
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_e:
                    player_data["high_scores"] = high_scores
                    player_data["coins"] += coins_collected
                    save_player_data(player_data)
                    pygame.mixer.music.stop()
                    return "menu"
                elif event.key == pygame.K_SPACE:
                    if player.on_ground:
                        player.jump()
                        if not jump_sound.get_num_channels():
                            jump_sound.play()
                    info_message = ""
                else:
                    info_message = "Press SPACE to jump, ESC to quit, or E to go back to main menu."
            elif event.type == pygame.MOUSEBUTTONDOWN:
                info_message = "Press SPACE to jump, ESC to quit, or E to go back to main menu."

        # Spawn obstacles
        spawn_timer += 1
            
        if spawn_timer > current_timer:

# Reset level index if we reach the end of the level list
            if level_index == len(level):    
                level_index = 0
                obstacle.speed_scale += 555500
                 
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

            if obstacle.type == "Coin" and player_rect.colliderect(obstacle.get_rect()):
                coins_collected += coin_value  # Add coins based on current value multiplier
                if coin_collect_sound and not coin_collect_sound.get_num_channels():
                    coin_collect_sound.play()
                # Dynamic coin value system: increase value at collection milestones
                total_coins = player_data["coins"] + coins_collected
                increment = get_coin_increment(total_coins)
                if coins_collected >= last_increment_coins + increment:
                    coin_value += 1
                    last_increment_coins += increment
                obstacles.remove(obstacle)
                continue

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
                    player = Player(player_data["current_skin"])
                    obstacles.clear()

                    level_index = 0
                    current_timer = 40

                    # Update high scores
                    player_data = add_score(score, player_data)
                    high_scores = player_data["high_scores"]
                    save_player_data(player_data)

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
        coins_text = font.render(f"Coins: {player_data['coins'] + coins_collected}", True, BLACK)
        coin_value_text = font.render(f"Coin Value: {coin_value}", True, BLACK)
        save_high_scores_text = font.render(f"High Score: {high_scores[0] if high_scores else 0}", True, BLACK)
        info_text = font.render(info_message, True, BLACK) if info_message else None

        screen.blit(score_text, (10, 10))
        screen.blit(death_text, (10, 40))
        screen.blit(coins_text, (10, 70))
        screen.blit(coin_value_text, (10, 100))
        screen.blit(save_high_scores_text, (10, 130))
        if info_text:
            screen.blit(info_text, (10, 160))

        pygame.display.update()

if __name__ == "__main__":
    try:
        # Main game loop with menu, game, shop, and settings states
        while True:
            if GAME_STATE == "menu":
                GAME_STATE = intro_screen()
            elif GAME_STATE == "game":
                GAME_STATE = main()
            elif GAME_STATE == "shop":
                GAME_STATE = shop_screen()
            elif GAME_STATE == "settings":
                GAME_STATE = settings_screen()
    except Exception as e:
        # Fallback system: if main game crashes, attempt to run backup version
        print(f"Main game crashed with error: {e}")
        print("Attempting to run backup version...")
        try:
            exec(open("Impossible_Dash_Backup.py").read())
        except Exception as e2:
            print(f"Backup also failed: {e2}")
            print("Unable to run the game. Please check the code.")
