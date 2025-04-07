"""
Boss entity
"""
import pygame
import math
import random
from pygame.locals import USEREVENT
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, YELLOW, ORANGE, RED, PURPLE, GREEN, GREY,
    ENEMY_LEVEL_1, ENEMY_LEVEL_2, ENEMY_LEVEL_3, ENEMY_LEVEL_4
)
from src.utils.resources import load_image
from src.entities.bee import Bee

class Boss(pygame.sprite.Sprite):
    """Boss class for end of level challenges"""
    def __init__(self, level):
        super(Boss, self).__init__()

        # Boss properties based on level
        self.level = level

        if level == 1:  # Level 1 Boss: Giant Bee
            self.health = 75  # Increased 5x from 15
            self.max_health = 75
            self.speed = 1.5
            self.points = 500
            self.color = YELLOW
            self.size = 100
            self.attack_pattern = "circle"
            self.attack_cooldown = 1500
            self.last_attack = 0
        elif level == 2:  # Level 2 Boss: Bee Queen
            self.health = 100  # Increased 5x from 20
            self.max_health = 100
            self.speed = 2
            self.points = 1000
            self.color = ORANGE
            self.size = 120
            self.attack_pattern = "zigzag"
            self.attack_cooldown = 1200
            self.last_attack = 0
        elif level == 3:  # Level 3 Boss: Alien Hive Mind
            self.health = 150  # Increased 5x from 30
            self.max_health = 150
            self.speed = 2.5
            self.points = 2000
            self.color = RED
            self.size = 150
            self.attack_pattern = "swarm"
            self.attack_cooldown = 1000
            self.last_attack = 0

        # Create boss image with proper transparency
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        # Fill with transparent color to ensure no background rectangle
        self.image.fill((0, 0, 0, 0))

        # Draw boss based on level
        if level == 1:  # Giant Bee
            # Body
            pygame.draw.circle(self.image, self.color, (self.size//2, self.size//2), self.size//2 - 10)

            # Stripes
            for i in range(3):
                y_pos = self.size//4 + i * self.size//6
                pygame.draw.rect(self.image, BLACK, (10, y_pos, self.size - 20, self.size//10))

            # Eyes
            eye_size = self.size // 8
            pygame.draw.circle(self.image, BLACK, (self.size//3, self.size//3), eye_size)
            pygame.draw.circle(self.image, BLACK, (2*self.size//3, self.size//3), eye_size)

            # Wings
            wing_points = [
                (self.size//4, self.size//4),
                (0, 0),
                (self.size//4, self.size//2)
            ]
            pygame.draw.polygon(self.image, WHITE, wing_points)

            wing_points = [
                (3*self.size//4, self.size//4),
                (self.size, 0),
                (3*self.size//4, self.size//2)
            ]
            pygame.draw.polygon(self.image, WHITE, wing_points)

        elif level == 2:  # Bee Queen
            # Body
            pygame.draw.circle(self.image, self.color, (self.size//2, self.size//2), self.size//2 - 10)

            # Crown
            crown_points = [
                (self.size//4, self.size//4),
                (self.size//3, self.size//8),
                (self.size//2, self.size//4),
                (2*self.size//3, self.size//8),
                (3*self.size//4, self.size//4)
            ]
            pygame.draw.polygon(self.image, YELLOW, crown_points)

            # Stripes
            for i in range(4):
                y_pos = self.size//3 + i * self.size//8
                pygame.draw.rect(self.image, BLACK, (10, y_pos, self.size - 20, self.size//12))

            # Eyes
            eye_size = self.size // 8
            pygame.draw.circle(self.image, BLACK, (self.size//3, self.size//3), eye_size)
            pygame.draw.circle(self.image, BLACK, (2*self.size//3, self.size//3), eye_size)

            # Wings
            wing_points = [
                (self.size//4, self.size//3),
                (0, self.size//6),
                (0, self.size//2),
                (self.size//4, self.size//2)
            ]
            pygame.draw.polygon(self.image, WHITE, wing_points)

            wing_points = [
                (3*self.size//4, self.size//3),
                (self.size, self.size//6),
                (self.size, self.size//2),
                (3*self.size//4, self.size//2)
            ]
            pygame.draw.polygon(self.image, WHITE, wing_points)

        elif level == 3:  # Alien Hive Mind
            # Main body
            pygame.draw.circle(self.image, self.color, (self.size//2, self.size//2), self.size//2 - 10)

            # Alien features
            # Eyes (multiple)
            for i in range(3):
                for j in range(2):
                    eye_x = self.size//3 + j * self.size//3
                    eye_y = self.size//4 + i * self.size//6
                    eye_size = self.size // 12
                    pygame.draw.circle(self.image, GREEN, (eye_x, eye_y), eye_size)
                    pygame.draw.circle(self.image, BLACK, (eye_x, eye_y), eye_size//2)

            # Tentacles
            for i in range(8):
                angle = i * math.pi / 4
                end_x = self.size//2 + int(math.cos(angle) * self.size//1.5)
                end_y = self.size//2 + int(math.sin(angle) * self.size//1.5)
                pygame.draw.line(self.image, PURPLE, (self.size//2, self.size//2), (end_x, end_y), 5)

        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.top = 50

        # Movement variables
        self.direction = 1  # 1 for right, -1 for left
        self.movement_timer = 0
        self.angle = 0  # For circular movement

        # Attack variables
        self.attack_timer = 0

    def update(self):
        """Update boss movement and behavior"""
        # Update movement timer
        self.movement_timer += 1

        # Move based on attack pattern
        if self.attack_pattern == "circle":
            # Circular movement
            self.angle += 0.02
            self.rect.centerx = SCREEN_WIDTH // 2 + int(math.sin(self.angle) * 200)
            self.rect.centery = 150 + int(math.cos(self.angle) * 100)
        elif self.attack_pattern == "zigzag":
            # Zigzag movement
            if self.movement_timer % 60 < 30:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

            # Occasionally move up and down
            if self.movement_timer % 120 < 60:
                self.rect.y += self.speed / 2
            else:
                self.rect.y -= self.speed / 2
        elif self.attack_pattern == "swarm":
            # Complex swarm-like movement
            self.angle += 0.03
            self.rect.centerx = SCREEN_WIDTH // 2 + int(math.sin(self.angle) * 250)
            self.rect.centery = 150 + int(math.cos(self.angle * 2) * 100)

        # Keep boss on screen
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT // 2:
            self.rect.bottom = SCREEN_HEIGHT // 2

        # Attack logic
        now = pygame.time.get_ticks()
        if now - self.last_attack > self.attack_cooldown:
            self.attack()
            self.last_attack = now

    def attack(self):
        """Attack by spawning enemy bees"""
        # Different attack patterns based on boss level (reduced difficulty)
        if self.level == 1:  # Level 1 Boss: Simple attack
            # Spawn 2 bees (reduced from 3) in a spread pattern
            bees = []
            for i in range(2):
                new_bee = Bee(level=ENEMY_LEVEL_1)  # Easier bees (reduced from level 2)
                offset = (i - 0.5) * 50  # -25, 25
                new_bee.rect.centerx = self.rect.centerx + offset
                new_bee.rect.top = self.rect.bottom
                bees.append(new_bee)
            return bees

        elif self.level == 2:  # Level 2 Boss: More complex attack
            # Spawn 3 bees (reduced from 5) in a circular pattern
            bees = []
            for i in range(3):
                new_bee = Bee(level=ENEMY_LEVEL_2)  # Easier bees (reduced from level 3)
                angle = i * 2 * math.pi / 3
                offset_x = int(math.cos(angle) * 70)
                offset_y = int(math.sin(angle) * 70)
                new_bee.rect.centerx = self.rect.centerx + offset_x
                new_bee.rect.centery = self.rect.centery + offset_y
                bees.append(new_bee)
            return bees

        elif self.level == 3:  # Level 3 Boss: Advanced attack
            # Spawn 4 bees (reduced from 7) in a complex pattern
            bees = []
            for i in range(4):
                new_bee = Bee(level=ENEMY_LEVEL_3)  # Easier bees (reduced from level 4)
                angle = i * 2 * math.pi / 4
                offset_x = int(math.cos(angle) * 100)
                offset_y = int(math.sin(angle) * 100)
                new_bee.rect.centerx = self.rect.centerx + offset_x
                new_bee.rect.centery = self.rect.centery + offset_y
                bees.append(new_bee)
            return bees

        return []

    def hit(self, damage):
        """Handle being hit"""
        # Handle being hit
        self.health -= damage

        # Check if boss is destroyed
        if self.health <= 0:
            # Boss is destroyed, return True
            return True

        # Boss still alive, flash white briefly to indicate damage
        flash_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        flash_surface.fill((255, 255, 255, 100))  # Semi-transparent white
        self.image.blit(flash_surface, (0, 0))

        # Schedule a redraw of the boss after the flash
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)  # 50ms flash duration

        # Return False as boss is not destroyed
        return False

    def redraw(self):
        """Redraw the boss after flash effect"""
        # Create boss image with proper transparency
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Fill with transparent color

        # Redraw boss based on level
        if self.level == 1:  # Giant Bee
            # Body
            pygame.draw.circle(self.image, self.color, (self.size//2, self.size//2), self.size//2 - 10)

            # Stripes
            for i in range(3):
                y_pos = self.size//4 + i * self.size//6
                pygame.draw.rect(self.image, BLACK, (10, y_pos, self.size - 20, self.size//10))

            # Eyes
            eye_size = self.size // 8
            pygame.draw.circle(self.image, BLACK, (self.size//3, self.size//3), eye_size)
            pygame.draw.circle(self.image, BLACK, (2*self.size//3, self.size//3), eye_size)

            # Wings
            wing_points = [
                (self.size//4, self.size//4),
                (0, 0),
                (self.size//4, self.size//2)
            ]
            pygame.draw.polygon(self.image, WHITE, wing_points)

            wing_points = [
                (3*self.size//4, self.size//4),
                (self.size, 0),
                (3*self.size//4, self.size//2)
            ]
            pygame.draw.polygon(self.image, WHITE, wing_points)

        elif self.level == 2:  # Bee Queen
            # Body
            pygame.draw.circle(self.image, self.color, (self.size//2, self.size//2), self.size//2 - 10)

            # Crown
            crown_points = [
                (self.size//4, self.size//4),
                (self.size//3, self.size//8),
                (self.size//2, self.size//4),
                (2*self.size//3, self.size//8),
                (3*self.size//4, self.size//4)
            ]
            pygame.draw.polygon(self.image, YELLOW, crown_points)

            # Stripes
            for i in range(4):
                y_pos = self.size//3 + i * self.size//8
                pygame.draw.rect(self.image, BLACK, (10, y_pos, self.size - 20, self.size//12))

            # Eyes
            eye_size = self.size // 8
            pygame.draw.circle(self.image, BLACK, (self.size//3, self.size//3), eye_size)
            pygame.draw.circle(self.image, BLACK, (2*self.size//3, self.size//3), eye_size)

            # Wings
            wing_points = [
                (self.size//4, self.size//3),
                (0, self.size//6),
                (0, self.size//2),
                (self.size//4, self.size//2)
            ]
            pygame.draw.polygon(self.image, WHITE, wing_points)

            wing_points = [
                (3*self.size//4, self.size//3),
                (self.size, self.size//6),
                (self.size, self.size//2),
                (3*self.size//4, self.size//2)
            ]
            pygame.draw.polygon(self.image, WHITE, wing_points)

        elif self.level == 3:  # Alien Hive Mind
            # Main body
            pygame.draw.circle(self.image, self.color, (self.size//2, self.size//2), self.size//2 - 10)

            # Alien features
            # Eyes (multiple)
            for i in range(3):
                for j in range(2):
                    eye_x = self.size//3 + j * self.size//3
                    eye_y = self.size//4 + i * self.size//6
                    eye_size = self.size // 12
                    pygame.draw.circle(self.image, GREEN, (eye_x, eye_y), eye_size)
                    pygame.draw.circle(self.image, BLACK, (eye_x, eye_y), eye_size//2)

            # Tentacles
            for i in range(8):
                angle = i * math.pi / 4
                end_x = self.size//2 + int(math.cos(angle) * self.size//1.5)
                end_y = self.size//2 + int(math.sin(angle) * self.size//1.5)
                pygame.draw.line(self.image, PURPLE, (self.size//2, self.size//2), (end_x, end_y), 5)

    def draw_health_bar(self, screen):
        """Draw boss health bar"""
        # Draw health bar
        bar_width = 200
        bar_height = 20
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 20

        # Background (empty health)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))

        # Foreground (current health)
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

        # Border
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        # Text
        font = pygame.font.Font(None, 24)
        boss_text = font.render(f"BOSS - Level {self.level}", True, WHITE)
        screen.blit(boss_text, (bar_x + bar_width // 2 - boss_text.get_width() // 2, bar_y - 25))
