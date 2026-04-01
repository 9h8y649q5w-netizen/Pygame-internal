'''Date: 30/03/2026

Author: Oliver Lloyd

About:

Inspired by the game "Impossible Dash" by Nitrome and the rip of version of "Impossible Dash", "Geometry dash" by Robert Topala, 
this is a remake of the game in Python using Pygame but it much more harder.'''

import os
import pygame
from button import Button
from Player import Player
from pygame.locals import *
import random

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720), FULLSCREEN)
pygame.display.set_caption("Impossible Dash")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 34)

class KillObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 64
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        asset_path = os.path.join(os.path.dirname(__file__), "assets", "KillObject.png")
        try:
            self.raw_image = pygame.image.load(asset_path).convert_alpha()
            self.raw_image = pygame.transform.scale(self.raw_image, (self.size, self.size))
        except Exception:
            self.raw_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(self.raw_image, (255, 0, 0), (self.size//2, self.size//2), self.size//2)

    def update(self, dx):
        self.x -= dx
        self.rect.x = round(self.x)

    def draw(self, surface):
        surface.blit(self.raw_image, self.rect)


def reset_game():
    global platforms, kill_objects, world_scroll_timer, Number_of_trys, player_start_y, player_start_x, death_effect_counter, is_dead
    Number_of_trys += 1
    if Number_of_trys > High_score_of_number_of_trys:
        update_high_score(Number_of_trys)
    USER.x = player_start_x
    USER.y = player_start_y
    USER.vx = 0
    USER.vy = 0
    USER.is_on_ground = False
    USER.rotation = 0
    USER.target_rotation = 0
    USER.is_rotating = False
    USER.rect.topleft = (USER.x, USER.y)
    platforms = [pygame.Rect(0, 660, 1280, 60)]
    kill_objects = []
    world_scroll_timer = 0
    death_effect_counter = 0s
    is_dead = False


def update_high_score(current):
    global High_score_of_number_of_trys
    High_score_of_number_of_trys = current


# Create player at start position
player_start_x = 100
player_start_y = 500
USER = Player(player_start_x, player_start_y)

platforms = [pygame.Rect(0, 660, 1280, 60)]  # floor
kill_objects = []

Number_of_trys = 0
High_score_of_number_of_trys = 0
world_scroll_timer = 0
spawn_interval = 180
is_dead = False
death_effect_counter = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                if not is_dead:
                    USER.jump()

    # world scrolling; player is fixed horizontally at start position
    if not is_dead:
        world_dx = 4
        for obj in kill_objects:
            obj.update(world_dx)

        # Spawn kills at intervals
        world_scroll_timer += 1
        if world_scroll_timer >= spawn_interval:
            world_scroll_timer = 0
            spawn_x = 1280 + random.randint(0, 300)
            spawn_y = player_start_y
            kill_objects.append(KillObject(spawn_x, spawn_y))

    # Update player
    USER.update(platforms)

    # Collision with kill objects
    if not is_dead:
        for obj in kill_objects[:]:
            if USER.rect.colliderect(obj.rect):
                is_dead = True
                death_effect_counter = 36
                break

    # automatic reset after death effect
    if is_dead:
        death_effect_counter -= 1
        if death_effect_counter <= 0:
            reset_game()

    # cleanup kill objects off-screen
    kill_objects = [obj for obj in kill_objects if obj.rect.right > -50]

    # Draw
    SCREEN.fill((30, 30, 40))

    # background parallax tile
    for i in range(-1, 3):
        pygame.draw.rect(SCREEN, (20, 20, 70), (i*640 - (pygame.time.get_ticks()//20 % 640), 0, 640, 720))

    # Draw platforms and kill objects
    for platform in platforms:
        pygame.draw.rect(SCREEN, (100, 100, 100), platform)
    for obj in kill_objects:
        obj.draw(SCREEN)

    USER.draw(SCREEN)

    # Death flash overlay
    if is_dead:
        alpha = min(180, (36 - death_effect_counter) * 5)
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, alpha))
        SCREEN.blit(overlay, (0, 0))

    # HUD
    txt = font.render(f"Try: {Number_of_trys}  High: {High_score_of_number_of_trys}", True, (255, 255, 255))
    SCREEN.blit(txt, (24, 24))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
