"""
Bomb effect
"""
import pygame
import random
import math
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, ORANGE, RED

class BombEffect(pygame.sprite.Sprite):
    """Visual effect for bomb explosion"""
    def __init__(self, center):
        super(BombEffect, self).__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.frame = 0
        self.max_frames = 30
        self.center = center
        self.particles = []

        # Create particles
        for _ in range(50):
            # Random angle and speed
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 15)
            size = random.randint(3, 10)
            life = random.randint(20, 30)
            color = random.choice([WHITE, YELLOW, ORANGE, RED])

            # Calculate velocity
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            self.particles.append({
                'pos': [center[0], center[1]],
                'vel': [vx, vy],
                'size': size,
                'color': color,
                'life': life
            })

        # Create shockwave
        self.shockwave_radius = 10
        self.shockwave_max_radius = 300
        self.shockwave_width = 5
        self.shockwave_color = WHITE

    def update(self):
        """Update bomb effect animation"""
        self.frame += 1

        # Clear the image
        self.image.fill((0, 0, 0, 0))

        # Update and draw particles
        for particle in self.particles:
            # Update position
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]

            # Apply gravity
            particle['vel'][1] += 0.2

            # Reduce life
            particle['life'] -= 1

            # Skip dead particles
            if particle['life'] <= 0:
                continue

            # Calculate alpha based on remaining life
            alpha = int(255 * (particle['life'] / 30))

            # Draw particle
            pygame.draw.circle(self.image, particle['color'] + (alpha,),
                              (int(particle['pos'][0]), int(particle['pos'][1])),
                              particle['size'])

        # Update and draw shockwave
        self.shockwave_radius += (self.shockwave_max_radius - self.shockwave_radius) * 0.2

        # Calculate alpha based on radius
        alpha = int(255 * (1 - self.shockwave_radius / self.shockwave_max_radius))

        # Draw shockwave
        pygame.draw.circle(self.image, self.shockwave_color + (alpha,),
                          self.center, int(self.shockwave_radius),
                          self.shockwave_width)

        # Kill when animation is complete
        if self.frame >= self.max_frames:
            self.kill()
