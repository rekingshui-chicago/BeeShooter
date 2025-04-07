"""
Bullet entity
"""
import pygame
from src.utils.constants import (
    SCREEN_WIDTH, GREEN, CYAN, PINK, WHITE, YELLOW
)
from src.utils.resources import load_image

class Bullet(pygame.sprite.Sprite):
    """Bullet class for player's weapon"""
    def __init__(self, x, y, angle=0):
        super(Bullet, self).__init__()

        # Create bullet image based on angle
        self.image = pygame.Surface((5, 15), pygame.SRCALPHA)

        # Rotate bullet based on angle
        if angle != 0:
            # Different colors for different angles
            if angle == 0:
                color = GREEN
            elif angle > 0:
                color = CYAN
            else:
                color = PINK

            pygame.draw.rect(self.image, color, (0, 0, 5, 15))
            pygame.draw.rect(self.image, WHITE, (2, 0, 1, 15))
            self.damage = 1
        else:
            # Standard bullet
            pygame.draw.rect(self.image, YELLOW, (0, 0, 5, 15))
            pygame.draw.rect(self.image, WHITE, (2, 0, 1, 15))
            self.damage = 1

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.speedx = angle  # Horizontal movement based on angle

    def update(self):
        """Update bullet position"""
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # Kill if it moves off the screen
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
