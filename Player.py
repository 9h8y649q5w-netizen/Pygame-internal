import os
import math
import pygame

class Player:
    def __init__(self, x, y, speed=6, jump_strength=17):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = speed
        self.jump_strength = jump_strength
        self.is_on_ground = False
        self.rotation = 0
        self.target_rotation = 0
        self.is_rotating = False

        # Try to load an image from assets, otherwise use a placeholder rect
        self.image_path = os.path.join(os.path.dirname(__file__), "assets", "Character.png")
        try:
            self.raw_image = pygame.image.load(self.image_path).convert_alpha()
            self.raw_image = pygame.transform.scale(self.raw_image, (64, 64))
        except Exception:
            self.raw_image = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.polygon(self.raw_image, (0, 200, 255), [(32, 0), (64, 64), (0, 64)])

        self.image = self.raw_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vx = 0

        # Disable horizontal movement for A/D and Left/Right arrow keys.
        # This ensures pressing those keys does not move the player.
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = 0

        # Jump is controlled in main event loop on KEYDOWN to avoid repeated jumping while holding.

    def jump(self):
        if self.is_on_ground:
            self.vy = -self.jump_strength
            self.is_on_ground = False
            # Begin a single 90° rotation for this jump.
            self.target_rotation = (self.rotation + 90) % 360
            self.is_rotating = True

    def apply_gravity(self):
        gravity = 0.9
        self.vy += gravity
        if self.vy > 25:
            self.vy = 25

    def update(self, platforms):
        self.handle_input()
        self.apply_gravity()

        self.x += self.vx
        self.rect.x = round(self.x)

        # Horizontal collisions
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vx > 0:
                    self.rect.right = platform.left
                elif self.vx < 0:
                    self.rect.left = platform.right
                self.x = self.rect.x

        self.y += self.vy
        self.rect.y = round(self.y)

        # Vertical collisions and ground check
        self.is_on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vy > 0:
                    self.rect.bottom = platform.top
                    self.y = self.rect.y
                    self.vy = 0
                    self.is_on_ground = True
                elif self.vy < 0:
                    self.rect.top = platform.bottom
                    self.y = self.rect.y
                    self.vy = 0

        # Rotate while airborne for animation: one jump = one 90° rotation.
        if self.is_rotating:
            # Slower spin per tick.
            step = 3
            diff = (self.target_rotation - self.rotation) % 360
            if diff == 0:
                self.is_rotating = False
            else:
                if diff <= step or diff >= 360 - step:
                    self.rotation = self.target_rotation
                    self.is_rotating = False
                else:
                    self.rotation = (self.rotation + step) % 360

        # Keep player in screen bounds
        SCREEN_W, SCREEN_H = 1280, 720
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.x
        if self.rect.right > SCREEN_W:
            self.rect.right = SCREEN_W
            self.x = self.rect.x
        if self.rect.top < 0:
            self.rect.top = 0
            self.y = self.rect.y
            self.vy = 0

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.raw_image, -self.rotation)
        draw_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, draw_rect)

        # Orientation debug line (red): helps confirm 90° rotation visually.
        angle_rad = math.radians(self.rotation)
        line_length = 32
        end_x = draw_rect.centerx + math.cos(angle_rad) * line_length
        end_y = draw_rect.centery + math.sin(angle_rad) * line_length
        pygame.draw.line(surface, (255, 0, 0), draw_rect.center, (end_x, end_y), 3)
    