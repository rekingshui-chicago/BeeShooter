"""
Explosion effect
"""
import pygame
import random
from src.utils.constants import ORANGE, YELLOW, WHITE
from src.utils.resources import load_image

class Explosion(pygame.sprite.Sprite):
    """Explosion animation effect"""
    def __init__(self, center, size=None):
        super(Explosion, self).__init__()
        self.image = load_image("explosion")

        # Scale explosion if size is specified
        if size:
            self.image = pygame.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 50  # ms per frame
        self.last_update = pygame.time.get_ticks()
        self.frame_count = 9  # Total number of frames

        # Store original image for scaling
        self.original_image = self.image.copy()
        self.current_size = self.image.get_width()
        self.max_size = self.current_size * 1.5

    def update(self):
        """Update explosion animation"""
        now = pygame.time.get_ticks()

        # Check if it's time to update the frame
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1

            # If we've reached the end of the animation, kill the sprite
            if self.frame >= self.frame_count:
                self.kill()
            else:
                # Calculate new size based on frame
                if self.frame < self.frame_count // 2:
                    # Expand
                    progress = self.frame / (self.frame_count // 2)
                    new_size = int(self.current_size + (self.max_size - self.current_size) * progress)
                else:
                    # Contract
                    progress = (self.frame - self.frame_count // 2) / (self.frame_count // 2)
                    new_size = int(self.max_size - (self.max_size - self.current_size) * progress)

                # Keep track of center
                center = self.rect.center

                # Scale the image
                self.image = pygame.transform.scale(self.original_image, (new_size, new_size))

                # Update rect and center
                self.rect = self.image.get_rect()
                self.rect.center = center

                # Adjust transparency based on frame
                if self.frame > self.frame_count * 0.7:
                    # Fade out towards the end
                    alpha = int(255 * (1 - (self.frame - self.frame_count * 0.7) / (self.frame_count * 0.3)))
                    self.image.set_alpha(alpha)
