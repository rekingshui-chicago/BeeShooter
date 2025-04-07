"""
Victory effect
"""
import pygame
import random
import math
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, YELLOW, WHITE, ORANGE, LIGHT_BLUE

class VictoryEffect(pygame.sprite.Sprite):
    """Visual effect for victory celebration"""
    def __init__(self):
        super(VictoryEffect, self).__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.timer = 0
        self.duration = 180  # 3 seconds at 60 FPS
        self.particles = []

        # Create particles
        for _ in range(100):
            x = random.randrange(0, SCREEN_WIDTH)
            y = random.randrange(0, SCREEN_HEIGHT)
            size = random.randrange(5, 15)
            speed = random.uniform(1, 3)
            angle = random.uniform(0, 2 * math.pi)
            color = random.choice([YELLOW, WHITE, ORANGE, LIGHT_BLUE])
            self.particles.append({
                "pos": [x, y],
                "size": size,
                "speed": speed,
                "angle": angle,
                "color": color
            })

    def update(self):
        """Update victory effect animation"""
        self.timer += 1
        if self.timer >= self.duration:
            self.kill()
            return

        # Clear the image
        self.image.fill((0, 0, 0, 0))

        # Update and draw particles
        for particle in self.particles:
            # Move particle
            particle["pos"][0] += math.cos(particle["angle"]) * particle["speed"]
            particle["pos"][1] += math.sin(particle["angle"]) * particle["speed"]

            # Draw particle
            pygame.draw.circle(self.image, particle["color"],
                             (int(particle["pos"][0]), int(particle["pos"][1])),
                             particle["size"])

            # Wrap around screen
            if particle["pos"][0] < 0:
                particle["pos"][0] = SCREEN_WIDTH
            elif particle["pos"][0] > SCREEN_WIDTH:
                particle["pos"][0] = 0
            if particle["pos"][1] < 0:
                particle["pos"][1] = SCREEN_HEIGHT
            elif particle["pos"][1] > SCREEN_HEIGHT:
                particle["pos"][1] = 0

        # Draw victory text
        font = pygame.font.Font(None, 72)
        text = font.render("CONGRATULATIONS!", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.image.blit(text, text_rect)

        font = pygame.font.Font(None, 48)
        text = font.render("You have defeated all bosses!", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.image.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        text = font.render("Press ENTER to play again", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 2*SCREEN_HEIGHT//3))
        self.image.blit(text, text_rect)
