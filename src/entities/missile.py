"""
Missile entity
"""
import pygame
import math
import random
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GREY, RED, ORANGE
)
from src.utils.resources import load_image

class Missile(pygame.sprite.Sprite):
    """Missile class for player's special weapon"""
    def __init__(self, x, y, damage=1, target_seeking=False):
        super(Missile, self).__init__()
        self.image = pygame.Surface((10, 20), pygame.SRCALPHA)

        # Missile body
        pygame.draw.rect(self.image, GREY, (3, 0, 4, 15))
        # Missile head
        pygame.draw.polygon(self.image, RED, [(3, 0), (7, 0), (5, -5)])
        # Missile fins
        pygame.draw.polygon(self.image, GREY, [(0, 15), (3, 15), (3, 10)])
        pygame.draw.polygon(self.image, GREY, [(7, 15), (10, 15), (7, 10)])
        # Missile engine
        pygame.draw.rect(self.image, ORANGE, (4, 15, 2, 5))

        # Store original image for rotation
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -8  # Slower than bullets
        self.speedx = 0
        self.damage = damage
        self.target_seeking = target_seeking
        self.target = None
        self.max_turn_rate = 0.5  # Maximum turning rate (increased from 0.3 for better tracking)
        self.smoke_timer = 0
        self.smoke_delay = 2  # Frames between smoke particles (reduced from 3 for more smoke)

        # For smooth rotation
        self.angle = 0
        self.direction = pygame.math.Vector2(0, -1)  # Initial direction (up)

    def update(self):
        """Update missile position and behavior"""
        # Increment smoke timer
        self.smoke_timer += 1

        # Target seeking behavior
        if self.target_seeking and self.target:
            # Check if target is still alive
            if hasattr(self.target, 'alive') and callable(getattr(self.target, 'alive')) and not self.target.alive():
                # Target is no longer alive, clear it
                self.target = None
            else:
                # Calculate direction to target
                target_direction = pygame.math.Vector2(
                    self.target.rect.centerx - self.rect.centerx,
                    self.target.rect.centery - self.rect.centery
                )

                # Skip if target is too close (avoid division by zero)
                if target_direction.length() > 5:
                    target_direction = target_direction.normalize()

                    # Calculate angle between current direction and target direction
                    angle_diff = math.degrees(math.atan2(
                        self.direction.x * target_direction.y - self.direction.y * target_direction.x,
                        self.direction.x * target_direction.x + self.direction.y * target_direction.y
                    ))

                    # Increase turning rate for better tracking
                    self.max_turn_rate = 0.8  # Increased from 0.3

                    # Limit turning rate
                    if abs(angle_diff) > self.max_turn_rate:
                        angle_diff = self.max_turn_rate if angle_diff > 0 else -self.max_turn_rate

                    # Update direction
                    self.angle += angle_diff
                    self.direction = pygame.math.Vector2(
                        math.sin(math.radians(self.angle)),
                        -math.cos(math.radians(self.angle))
                    )

                    # Update speed based on direction
                    speed_factor = 8  # Base speed
                    # Increase speed if target is far away
                    if target_direction.length() > 200:
                        speed_factor = 10  # Faster to catch up

                    self.speedx = self.direction.x * speed_factor
                    self.speedy = self.direction.y * speed_factor

                    # Rotate image to match direction
                    self.image = pygame.transform.rotate(self.original_image, self.angle)
                    self.rect = self.image.get_rect(center=self.rect.center)
        elif self.target_seeking and not self.target:
            # If missile is seeking but has no target, just go straight up
            self.speedx = 0
            self.speedy = -8

        # Move missile
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Create smoke trail
        if self.smoke_timer >= self.smoke_delay:
            self.smoke_timer = 0
            # Create smoke particle (would be handled by game manager)
            # self.game.create_smoke(self.rect.centerx, self.rect.bottom)

        # Kill if it moves off the screen
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()

    def set_target(self, target):
        """Set the target for the missile"""
        self.target = target
