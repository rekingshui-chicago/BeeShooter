"""
PowerUp entity
"""
import pygame
import random
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, RED, GREY, YELLOW, WHITE, ORANGE, CYAN
)
from src.utils.resources import load_image

class PowerUp(pygame.sprite.Sprite):
    """PowerUp class for player upgrades"""
    def __init__(self, center, powerup_type=None):
        super(PowerUp, self).__init__()

        # Randomly choose type if not specified
        if powerup_type is None:
            # 30% weapon upgrade, 20% bomb, 20% missile, 30% missile upgrade
            self.type = random.choice(["weapon_upgrade"] * 3 + ["bomb"] * 2 +
                                    ["missile"] * 2 + ["missile_upgrade"] * 3)
        else:
            self.type = powerup_type

        # Create image based on type
        self.image = self.create_powerup_image()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2  # Falling speed

        # Animation variables
        self.animation_timer = 0
        self.pulse_direction = 1  # 1 for growing, -1 for shrinking
        self.original_image = self.image.copy()
        self.scale_factor = 1.0

    def create_powerup_image(self):
        """Create powerup image based on type"""
        image = pygame.Surface((30, 30), pygame.SRCALPHA)

        if self.type == "weapon_upgrade":
            # Weapon upgrade - blue lightning bolt
            pygame.draw.circle(image, BLUE, (15, 15), 12)
            pygame.draw.polygon(image, YELLOW, [(15, 5), (10, 15), (15, 15), (10, 25), (20, 10), (15, 10)])
            pygame.draw.circle(image, WHITE, (15, 15), 5)

        elif self.type == "bomb":
            # Bomb - red circle with fuse
            pygame.draw.circle(image, RED, (15, 18), 10)
            pygame.draw.rect(image, GREY, (14, 5, 2, 8))
            pygame.draw.circle(image, ORANGE, (15, 5), 3)
            pygame.draw.circle(image, WHITE, (12, 15), 2)  # Highlight

        elif self.type == "missile":
            # Missile - grey rocket
            pygame.draw.rect(image, GREY, (12, 8, 6, 15))
            pygame.draw.polygon(image, RED, [(12, 8), (18, 8), (15, 3)])
            pygame.draw.polygon(image, GREY, [(10, 23), (12, 18), (12, 23)])
            pygame.draw.polygon(image, GREY, [(18, 23), (18, 18), (20, 23)])
            pygame.draw.rect(image, ORANGE, (13, 23, 4, 3))

        elif self.type == "missile_upgrade":
            # Missile upgrade - advanced missile
            pygame.draw.rect(image, GREY, (12, 8, 6, 15))
            pygame.draw.polygon(image, RED, [(12, 8), (18, 8), (15, 3)])
            pygame.draw.polygon(image, GREY, [(10, 23), (12, 18), (12, 23)])
            pygame.draw.polygon(image, GREY, [(18, 23), (18, 18), (20, 23)])
            pygame.draw.rect(image, ORANGE, (13, 23, 4, 3))
            # Add upgrade indicator
            pygame.draw.circle(image, CYAN, (22, 8), 6)
            pygame.draw.polygon(image, WHITE, [(22, 4), (20, 8), (22, 8), (20, 12), (24, 8), (22, 8)])

        # Add glow effect
        glow_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 255, 255, 50), (20, 20), 18)

        # Create final image with glow
        final_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        final_image.blit(glow_surf, (0, 0))
        final_image.blit(image, (5, 5))

        return final_image

    def update(self):
        """Update powerup position and animation"""
        # Move down
        self.rect.y += self.speedy

        # Kill if it moves off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # Animate powerup (pulsing effect)
        self.animation_timer += 1

        if self.animation_timer % 5 == 0:  # Update every 5 frames
            # Change scale direction if reaching limits
            if self.scale_factor >= 1.2:
                self.pulse_direction = -1
            elif self.scale_factor <= 0.8:
                self.pulse_direction = 1

            # Update scale factor
            self.scale_factor += 0.05 * self.pulse_direction

            # Scale the image
            new_width = int(self.original_image.get_width() * self.scale_factor)
            new_height = int(self.original_image.get_height() * self.scale_factor)

            # Keep original center
            old_center = self.rect.center

            # Scale image
            self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
            self.rect = self.image.get_rect()
            self.rect.center = old_center
