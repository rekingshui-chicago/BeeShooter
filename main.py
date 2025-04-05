#!/usr/bin/env python3
import pygame
import random
import os  # Needed for sound file paths
import sys
import math  # Needed for missile rotation
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_ESCAPE, K_RETURN, K_b, K_m

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
LIGHT_YELLOW = (255, 255, 153)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 100)
LIGHT_BLUE = (135, 206, 250)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)
BROWN = (165, 42, 42)
DARK_GREEN = (0, 100, 0)
DARK_RED = (139, 0, 0)

# Enemy levels
ENEMY_LEVEL_1 = 1  # Basic bee - low health, slow movement
ENEMY_LEVEL_2 = 2  # Soldier bee - medium health, medium movement
ENEMY_LEVEL_3 = 3  # Elite bee - high health, fast movement
ENEMY_LEVEL_4 = 4  # Queen bee - very high health, special attack patterns

# Weapon levels
WEAPON_LEVEL_1 = 1  # Basic dual lasers
WEAPON_LEVEL_2 = 2  # Triple lasers
WEAPON_LEVEL_3 = 3  # Spread shot
WEAPON_LEVEL_4 = 4  # Rapid fire with quad lasers
WEAPON_LEVEL_5 = 5  # Ultimate weapon

# Missile levels
MISSILE_LEVEL_1 = 1  # Basic single missile
MISSILE_LEVEL_2 = 2  # Dual missiles
MISSILE_LEVEL_3 = 3  # Triple missiles with increased damage
MISSILE_LEVEL_4 = 4  # Quad missiles with max damage

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Retro Bee Shooter")
clock = pygame.time.Clock()

# Load assets
def load_image(name, colorkey=None, scale=1):
    # Simple placeholder function for loading images
    # In a real game, you'd load actual image files
    if name == "background":
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surf.fill(DARK_BLUE)
        # Add stars
        for _ in range(100):
            x = random.randrange(0, SCREEN_WIDTH)
            y = random.randrange(0, SCREEN_HEIGHT)
            radius = random.randrange(1, 3)
            pygame.draw.circle(surf, WHITE, (x, y), radius)
    elif name == "player":
        # Create a more detailed spaceship
        surf = pygame.Surface((60, 40))
        surf.fill(BLACK)

        # Main body of the ship
        pygame.draw.polygon(surf, BLUE, [(30, 0), (50, 30), (30, 40), (10, 30)])

        # Cockpit
        pygame.draw.circle(surf, LIGHT_BLUE, (30, 20), 8)
        pygame.draw.circle(surf, WHITE, (30, 20), 4)

        # Wings
        pygame.draw.polygon(surf, RED, [(10, 30), (0, 40), (20, 40)])
        pygame.draw.polygon(surf, RED, [(50, 30), (60, 40), (40, 40)])

        # Engine flames
        pygame.draw.polygon(surf, ORANGE, [(25, 40), (30, 50), (35, 40)])

        # Weapon mounts
        pygame.draw.rect(surf, GREY, (15, 25, 5, 10))
        pygame.draw.rect(surf, GREY, (40, 25, 5, 10))
    elif name == "bee":
        # Create a larger surface for more detailed bee
        surf = pygame.Surface((50, 50))
        surf.fill(BLACK)

        # Body - oval shape
        pygame.draw.ellipse(surf, YELLOW, (10, 15, 30, 20))

        # Stripes
        pygame.draw.line(surf, BLACK, (15, 20), (35, 20), 2)
        pygame.draw.line(surf, BLACK, (15, 25), (35, 25), 2)
        pygame.draw.line(surf, BLACK, (15, 30), (35, 30), 2)

        # Head
        pygame.draw.circle(surf, LIGHT_YELLOW, (10, 25), 8)

        # Eyes
        pygame.draw.circle(surf, BLACK, (7, 23), 2)
        pygame.draw.circle(surf, BLACK, (13, 23), 2)

        # Antennae
        pygame.draw.line(surf, BLACK, (7, 20), (5, 15), 1)
        pygame.draw.line(surf, BLACK, (13, 20), (15, 15), 1)
        pygame.draw.circle(surf, BLACK, (5, 15), 1)
        pygame.draw.circle(surf, BLACK, (15, 15), 1)

        # Wings
        pygame.draw.ellipse(surf, WHITE, (15, 10, 15, 10))
        pygame.draw.ellipse(surf, WHITE, (20, 10, 15, 10))

        # Stinger
        pygame.draw.polygon(surf, ORANGE, [(40, 25), (45, 20), (45, 30)])
    elif name == "bullet":
        surf = pygame.Surface((5, 15))
        surf.fill(BLACK)
        # Draw a laser-like bullet
        pygame.draw.rect(surf, GREEN, (0, 0, 5, 15))
        # Add a glow effect
        pygame.draw.rect(surf, WHITE, (2, 0, 1, 15))

    if colorkey is not None:
        if colorkey == -1:
            colorkey = surf.get_at((0, 0))
        surf.set_colorkey(colorkey)

    if scale != 1:
        surf = pygame.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))

    return surf

# Load sounds
def load_sounds():
    sounds = {}
    # Create placeholder sounds if no sound files exist
    sounds['shoot'] = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'laser.wav'))
    sounds['explosion'] = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'explosion.wav'))
    sounds['game_over'] = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'game_over.wav'))
    sounds['powerup'] = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'powerup.wav'))
    sounds['bomb'] = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'bomb.wav'))
    sounds['missile'] = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'missile.wav'))

    # Set default volumes
    sounds['shoot'].set_volume(0.4)
    sounds['explosion'].set_volume(0.6)
    sounds['game_over'].set_volume(0.7)
    sounds['powerup'].set_volume(0.5)
    sounds['bomb'].set_volume(0.8)  # Louder for dramatic effect
    sounds['missile'].set_volume(0.5)

    return sounds

# Try to load sounds, but handle the case where files don't exist yet
try:
    sounds = load_sounds()
    sound_enabled = True
except:
    print("Sound files not found. Creating placeholder sounds.")
    # Create silent sounds as placeholders
    sounds = {}
    buffer = pygame.mixer.Sound(buffer=bytearray(44100))
    buffer.set_volume(0.0)
    sounds['shoot'] = buffer
    sounds['explosion'] = buffer
    sounds['game_over'] = buffer
    sounds['powerup'] = buffer
    sounds['bomb'] = buffer
    sounds['missile'] = buffer
    sound_enabled = False

# PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powerup_type=None):
        super(PowerUp, self).__init__()

        # Randomly choose type if not specified
        if powerup_type is None:
            # 50% weapon upgrade, 15% bomb, 15% missile, 20% missile upgrade
            self.type = random.choice(["weapon_upgrade"] * 5 + ["bomb"] * 15 +
                                    ["missile"] * 15 + ["missile_upgrade"] * 2)
        else:
            self.type = powerup_type

        self.image = pygame.Surface((20, 20))
        self.image.fill(BLACK)

        if self.type == "weapon_upgrade":
            # Draw a colorful weapon upgrade power-up
            pygame.draw.circle(self.image, CYAN, (10, 10), 8)
            pygame.draw.circle(self.image, WHITE, (10, 10), 4)
            pygame.draw.circle(self.image, PURPLE, (10, 10), 2)

            # Add a glow effect
            for i in range(4):
                pygame.draw.circle(self.image, CYAN, (10, 10), 10 + i, 1)

        elif self.type == "bomb":
            # Draw a bomb power-up (red with warning symbol)
            pygame.draw.circle(self.image, RED, (10, 10), 8)
            pygame.draw.circle(self.image, ORANGE, (10, 10), 6)
            pygame.draw.circle(self.image, YELLOW, (10, 10), 4)

            # Add warning symbol
            pygame.draw.line(self.image, BLACK, (8, 6), (12, 14), 2)
            pygame.draw.line(self.image, BLACK, (12, 6), (8, 14), 2)

            # Add a glow effect
            for i in range(4):
                pygame.draw.circle(self.image, RED, (10, 10), 10 + i, 1)

        elif self.type == "missile":
            # Draw a missile power-up (green with targeting symbol)
            pygame.draw.circle(self.image, GREEN, (10, 10), 8)
            pygame.draw.circle(self.image, LIGHT_GREY, (10, 10), 6)

            # Add targeting crosshair symbol
            pygame.draw.circle(self.image, GREEN, (10, 10), 4, 1)
            pygame.draw.line(self.image, GREEN, (6, 10), (14, 10), 1)
            pygame.draw.line(self.image, GREEN, (10, 6), (10, 14), 1)

            # Add a glow effect
            for i in range(4):
                pygame.draw.circle(self.image, GREEN, (10, 10), 10 + i, 1)

        elif self.type == "missile_upgrade":
            # Draw a missile upgrade power-up (red with multiple targeting symbols)
            pygame.draw.circle(self.image, RED, (10, 10), 8)
            pygame.draw.circle(self.image, LIGHT_GREY, (10, 10), 6)

            # Add multiple targeting symbols to indicate upgrade
            pygame.draw.circle(self.image, RED, (10, 10), 4, 1)
            pygame.draw.line(self.image, RED, (6, 10), (14, 10), 1)
            pygame.draw.line(self.image, RED, (10, 6), (10, 14), 1)

            # Add small dots to indicate multiple missiles
            pygame.draw.circle(self.image, WHITE, (7, 7), 1)
            pygame.draw.circle(self.image, WHITE, (13, 7), 1)
            pygame.draw.circle(self.image, WHITE, (7, 13), 1)
            pygame.draw.circle(self.image, WHITE, (13, 13), 1)

            # Add a glow effect
            for i in range(4):
                pygame.draw.circle(self.image, RED, (10, 10), 10 + i, 1)

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        # Position randomly at the top of the screen
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)

        # Movement speed
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-1, 2)

    def update(self):
        # Move the power-up
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # If it goes off-screen, remove it
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# BombEffect class for the bomb weapon visual effect
class BombEffect(pygame.sprite.Sprite):
    def __init__(self, center):
        super(BombEffect, self).__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.center = center
        self.radius = 10
        self.max_radius = max(SCREEN_WIDTH, SCREEN_HEIGHT) * 1.5  # Make sure it covers the entire screen
        self.growth_speed = 25  # Faster expansion
        self.fade_speed = 4
        self.alpha = 200  # More visible
        self.frame_count = 0

    def update(self):
        # Expand the radius
        self.radius += self.growth_speed
        self.frame_count += 1

        # Fade out as it expands
        if self.radius > 100:
            self.alpha = max(0, self.alpha - self.fade_speed)

        # Redraw the effect
        self.image.fill((0, 0, 0, 0))  # Clear with transparent

        # Draw expanding shockwave with pulsating effect
        pulse = abs(math.sin(self.frame_count * 0.2)) * 30

        # Outer ring (white)
        pygame.draw.circle(self.image, (255, 255, 255, self.alpha // 3), self.center, self.radius, 3)

        # Middle ring (orange/yellow)
        pygame.draw.circle(self.image, (255, 200, 50, self.alpha // 2), self.center, self.radius - 15, 4)

        # Inner ring (red with pulse)
        pygame.draw.circle(self.image, (255, 50, 50, self.alpha), self.center, self.radius - 30 + pulse, 0)

        # Add some particles for extra effect
        if self.frame_count % 3 == 0 and self.alpha > 50:
            for _ in range(5):
                angle = random.uniform(0, math.pi * 2)
                distance = random.uniform(0.7, 1.0) * self.radius
                x = self.center[0] + math.cos(angle) * distance
                y = self.center[1] + math.sin(angle) * distance
                size = random.randint(2, 6)
                pygame.draw.circle(self.image, (255, 200, 50, self.alpha), (int(x), int(y)), size)

        # Kill when fully expanded or faded
        if self.radius >= self.max_radius or self.alpha <= 0:
            self.kill()

# Missile class for auto-tracking projectiles
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, level=MISSILE_LEVEL_1, offset=0):
        super(Missile, self).__init__()
        self.level = level
        self._base_image = self.create_missile_image()  # Use a different name to avoid conflict
        self.image = self._base_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x + offset  # Allow for horizontal offset for multiple missiles
        self.rect.bottom = y

        # Set properties based on missile level
        if level == MISSILE_LEVEL_1:
            self.speedy = -3.0  # Basic speed
            self.max_speed = 5.0
            self.acceleration = 0.2
            self.damage = 3     # Basic damage
            self.smoke_delay = 5 # Normal smoke trail
        elif level == MISSILE_LEVEL_2:
            self.speedy = -3.5  # Slightly faster
            self.max_speed = 5.5
            self.acceleration = 0.25
            self.damage = 4     # More damage
            self.smoke_delay = 4 # More frequent smoke
        elif level == MISSILE_LEVEL_3:
            self.speedy = -4.0  # Even faster
            self.max_speed = 6.0
            self.acceleration = 0.3
            self.damage = 5     # High damage
            self.smoke_delay = 3 # Dense smoke trail
        elif level == MISSILE_LEVEL_4:
            self.speedy = -4.5  # Fastest
            self.max_speed = 7.0
            self.acceleration = 0.35
            self.damage = 7     # Maximum damage
            self.smoke_delay = 2 # Very dense smoke trail

        self.speedx = 0
        self.target = None
        self.smoke_timer = 0

    def create_missile_image(self):
        # Create a surface for the missile
        surf = pygame.Surface((10, 20))
        surf.fill(BLACK)

        # Base missile body color depends on level
        if self.level == MISSILE_LEVEL_1:
            body_color = GREEN
            fin_color = ORANGE
        elif self.level == MISSILE_LEVEL_2:
            body_color = CYAN
            fin_color = BLUE
        elif self.level == MISSILE_LEVEL_3:
            body_color = PURPLE
            fin_color = PINK
        else:  # MISSILE_LEVEL_4
            body_color = RED
            fin_color = YELLOW

        # Draw missile body
        pygame.draw.rect(surf, body_color, (0, 0, 10, 20))
        pygame.draw.polygon(surf, fin_color, [(0, 15), (5, 20), (10, 15)])
        pygame.draw.rect(surf, LIGHT_GREY, (3, 5, 4, 4))

        # Add engine flame
        pygame.draw.polygon(surf, YELLOW, [(3, 0), (5, -5), (7, 0)])

        # Add level indicator dots
        for i in range(self.level):
            pygame.draw.circle(surf, WHITE, (5, 15 - i * 3), 1)

        surf.set_colorkey(BLACK)
        return surf

    def update(self):
        global all_sprites

        # Create smoke trail
        self.smoke_timer += 1
        if self.smoke_timer >= self.smoke_delay:
            self.smoke_timer = 0
            smoke = SmokeParticle(self.rect.centerx, self.rect.bottom)
            all_sprites.add(smoke)

        # Find a target if we don't have one or if it's been destroyed
        if self.target is None or not self.target.alive():
            # Find the nearest bee
            min_distance = float('inf')
            nearest_bee = None
            for bee in bees:
                dx = bee.rect.centerx - self.rect.centerx
                dy = bee.rect.centery - self.rect.centery
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_bee = bee
            self.target = nearest_bee

        # If we have a target, track it
        if self.target:
            # Calculate direction to target
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Avoid division by zero

            # Normalize and scale by acceleration
            dx = dx / distance * self.acceleration
            dy = dy / distance * self.acceleration

            # Update velocity (with max speed limit)
            self.speedx += dx
            self.speedy += dy

            # Limit speed
            speed = (self.speedx ** 2 + self.speedy ** 2) ** 0.5
            if speed > self.max_speed:
                self.speedx = self.speedx / speed * self.max_speed
                self.speedy = self.speedy / speed * self.max_speed

            # Rotate missile to face direction of travel
            angle = math.degrees(math.atan2(-self.speedy, self.speedx)) - 90
            self.image = pygame.transform.rotate(self._base_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        # Move the missile
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Kill if it moves off the screen
        if (self.rect.bottom < 0 or self.rect.right < 0 or
            self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT):
            self.kill()

    # Removed the property that was causing infinite recursion

# Smoke particle for missile trail
class SmokeParticle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(SmokeParticle, self).__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, GREY, (2, 2), 2)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 20
        self.alpha = 200

    def update(self):
        self.lifetime -= 1
        self.alpha = int(self.alpha * 0.9)
        if self.lifetime <= 0:
            self.kill()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = load_image("player", BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8
        self.shoot_delay = 250  # milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.engine_flicker = 0  # For engine animation
        self.weapon_level = WEAPON_LEVEL_1  # Start with basic weapon
        self.weapon_heat = 0  # For weapon overheating mechanic
        self.bombs = 1  # Start with 1 bomb
        self.bomb_delay = 2000  # Cooldown between bomb uses (milliseconds)
        self.last_bomb = 0
        self.missiles = 3  # Start with 3 missiles
        self.missile_level = MISSILE_LEVEL_1  # Start with basic missiles
        self.missile_delay = 1000  # Cooldown between missile launches (milliseconds)
        self.last_missile = 0

    def update(self):
        # Movement - now with full directional control
        keys = pygame.key.get_pressed()
        moved = False

        # Horizontal movement
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            moved = True
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            moved = True

        # Vertical movement
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            moved = True
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
            moved = True

        # Engine animation - more intense when moving
        self.engine_flicker = (self.engine_flicker + 1) % 6
        if moved or self.engine_flicker < 3:
            # Update engine flame animation
            self.image = load_image("player", BLACK)
            # Draw larger flame when moving or flickering
            flame_size = 55 if moved else 50
            pygame.draw.polygon(self.image, YELLOW, [(25, 40), (30, flame_size), (35, 40)])

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now

            # Try to launch a missile automatically if available
            # Use a 20% chance to launch a missile when shooting (to conserve missiles)
            if self.missiles > 0 and random.random() < 0.20:
                self.launch_missile(auto_launch=True)

            # Different shooting patterns based on weapon level
            if self.weapon_level == WEAPON_LEVEL_1:
                # Basic dual lasers
                bullet1 = Bullet(self.rect.left + 15, self.rect.top + 10, 0)
                bullet2 = Bullet(self.rect.right - 15, self.rect.top + 10, 0)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)

            elif self.weapon_level == WEAPON_LEVEL_2:
                # Triple lasers
                bullet1 = Bullet(self.rect.left + 15, self.rect.top + 10, 0)
                bullet2 = Bullet(self.rect.centerx, self.rect.top, 0)
                bullet3 = Bullet(self.rect.right - 15, self.rect.top + 10, 0)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)

            elif self.weapon_level == WEAPON_LEVEL_3:
                # Spread shot (5 bullets in a fan pattern)
                for angle in range(-2, 3):
                    bullet = Bullet(self.rect.centerx, self.rect.top, angle * 2)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

            elif self.weapon_level == WEAPON_LEVEL_4:
                # Rapid fire with quad lasers (reduced delay and more bullets)
                self.shoot_delay = 150  # Faster firing rate

                # Create 4 bullets with increased damage and spread pattern
                # Left side bullets with outward angles
                bullet1 = Bullet(self.rect.left + 10, self.rect.top + 10, -1, damage_boost=True)  # Angled left
                bullet2 = Bullet(self.rect.left + 25, self.rect.top + 5, 0, damage_boost=True)    # Straight

                # Right side bullets with outward angles
                bullet3 = Bullet(self.rect.right - 25, self.rect.top + 5, 0, damage_boost=True)   # Straight
                bullet4 = Bullet(self.rect.right - 10, self.rect.top + 10, 1, damage_boost=True)  # Angled right

                # Add bullets to sprite groups
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)

            elif self.weapon_level == WEAPON_LEVEL_5:
                # Ultimate weapon (combination of spread and rapid fire)
                self.shoot_delay = 150
                # Center powerful beam
                big_bullet = Bullet(self.rect.centerx, self.rect.top, 0, True)
                all_sprites.add(big_bullet)
                bullets.add(big_bullet)
                # Side spread shots
                for angle in range(-2, 3):
                    if angle != 0:  # Skip center as we already have the big bullet there
                        bullet = Bullet(self.rect.centerx, self.rect.top, angle * 3)
                        all_sprites.add(bullet)
                        bullets.add(bullet)

            # Play shooting sound
            sounds['shoot'].play()

    def upgrade_weapon(self):
        if self.weapon_level < WEAPON_LEVEL_5:
            self.weapon_level += 1

            # Set appropriate shoot delay based on weapon level
            if self.weapon_level < WEAPON_LEVEL_4:
                self.shoot_delay = 250  # Normal fire rate for levels 1-3
            else:
                self.shoot_delay = 150  # Faster fire rate for levels 4-5

            # Play power-up sound
            sounds['powerup'].play()
            return True
        return False

    def add_bomb(self):
        self.bombs += 1
        sounds['powerup'].play()

    def use_bomb(self):
        now = pygame.time.get_ticks()
        if self.bombs > 0 and now - self.last_bomb > self.bomb_delay:
            self.bombs -= 1
            self.last_bomb = now
            # Create bomb effect
            bomb_effect = BombEffect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            all_sprites.add(bomb_effect)
            # Play bomb sound
            sounds['bomb'].play()
            return bomb_effect
        return None

    def add_missile(self):
        self.missiles += 2  # Add 2 missiles at a time
        sounds['powerup'].play()

    def upgrade_missile(self):
        if self.missile_level < MISSILE_LEVEL_4:
            self.missile_level += 1
            # Add bonus missiles when upgrading
            self.missiles += 3
            # Play power-up sound
            sounds['powerup'].play()
            return True
        else:
            # If already at max level, just add more missiles
            self.missiles += 5
            sounds['powerup'].play()
            return False

    def launch_missile(self, auto_launch=False):
        now = pygame.time.get_ticks()
        if self.missiles > 0 and now - self.last_missile > self.missile_delay:
            # Determine how many missiles to launch based on missile level
            if self.missile_level == MISSILE_LEVEL_1:
                # Single missile
                missiles_to_launch = 1
                self.missiles -= 1
            elif self.missile_level == MISSILE_LEVEL_2:
                # Dual missiles
                missiles_to_launch = 2
                self.missiles -= 1  # Still only consume 1 missile for multiple launches
            elif self.missile_level == MISSILE_LEVEL_3:
                # Triple missiles
                missiles_to_launch = 3
                self.missiles -= 1
            else:  # MISSILE_LEVEL_4
                # Quad missiles
                missiles_to_launch = 4
                self.missiles -= 1

            self.last_missile = now

            # Calculate offsets for multiple missiles
            if missiles_to_launch == 1:
                offsets = [0]  # Center
            elif missiles_to_launch == 2:
                offsets = [-15, 15]  # Left and right
            elif missiles_to_launch == 3:
                offsets = [-20, 0, 20]  # Left, center, right
            else:  # 4 missiles
                offsets = [-30, -10, 10, 30]  # Far left, left, right, far right

            # Create missiles with appropriate offsets
            launched_missiles = []
            for offset in offsets:
                missile = Missile(self.rect.centerx, self.rect.top, self.missile_level, offset)
                all_sprites.add(missile)
                missiles_group.add(missile)
                launched_missiles.append(missile)

            # Play missile sound (at lower volume if auto-launched)
            if auto_launch:
                # Store original volume
                original_volume = sounds['missile'].get_volume()
                # Set to lower volume for auto-launch
                sounds['missile'].set_volume(original_volume * 0.6)
                sounds['missile'].play()
                # Restore original volume
                sounds['missile'].set_volume(original_volume)
            else:
                sounds['missile'].play()

            return launched_missiles
        return None

# Bee class (enemy)
class Bee(pygame.sprite.Sprite):
    def __init__(self, level=None):
        super(Bee, self).__init__()

        # Randomly choose level if not specified, with higher levels being less common
        if level is None:
            # Level distribution: 60% level 1, 25% level 2, 10% level 3, 5% level 4
            level_choices = [ENEMY_LEVEL_1] * 60 + [ENEMY_LEVEL_2] * 25 + [ENEMY_LEVEL_3] * 10 + [ENEMY_LEVEL_4] * 5
            self.level = random.choice(level_choices)
        else:
            self.level = level

        # Set properties based on level
        if self.level == ENEMY_LEVEL_1:
            # Basic bee
            self.health = 1
            self.speed_factor = 1.0
            self.points = 10
            self.color = YELLOW
            self.size = 1.0
            self.drop_chance = 0.10  # 10% chance to drop power-up
            self.drop_weights = {"weapon_upgrade": 2, "bomb": 1, "missile": 1}  # 50% weapon, 25% bomb, 25% missile
        elif self.level == ENEMY_LEVEL_2:
            # Soldier bee
            self.health = 2
            self.speed_factor = 1.2  # Reduced from 1.3 to prevent too fast movement
            self.points = 20
            self.color = ORANGE
            self.size = 1.2
            self.drop_chance = 0.15  # 15% chance to drop power-up
            self.drop_weights = {"weapon_upgrade": 2, "bomb": 2, "missile": 1}  # 40% weapon, 40% bomb, 20% missile
        elif self.level == ENEMY_LEVEL_3:
            # Elite bee
            self.health = 3
            self.speed_factor = 1.3  # Reduced from 1.6 to prevent too fast movement
            self.points = 30
            self.color = RED
            self.size = 1.4
            self.drop_chance = 0.20  # 20% chance to drop power-up
            self.drop_weights = {"weapon_upgrade": 1, "bomb": 2, "missile": 2}  # 20% weapon, 40% bomb, 40% missile
        elif self.level == ENEMY_LEVEL_4:
            # Queen bee
            self.health = 5
            self.speed_factor = 0.9  # Slightly slower than basic bee
            self.points = 50
            self.color = PURPLE
            self.size = 1.8
            self.drop_chance = 0.30  # 30% chance to drop power-up
            self.drop_weights = {"weapon_upgrade": 1, "bomb": 3, "missile": 3}  # 14% weapon, 43% bomb, 43% missile

        # Create the base image
        self.base_image = self.create_bee_image()
        self.image = self.base_image
        self.rect = self.image.get_rect()

        # Position
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

        # Movement - limit the base speed range to prevent extreme values
        base_speedy = random.randrange(1, 3)  # Reduced upper limit from 4 to 3
        base_speedx = random.randrange(-1, 2)  # Reduced range from (-2,2) to (-1,2)

        # Apply speed factor with a maximum cap
        self.speedy = min(base_speedy * self.speed_factor, 3.5)  # Cap vertical speed
        self.speedx = max(min(base_speedx * self.speed_factor, 2.0), -2.0)  # Cap horizontal speed

        # Special movement patterns for higher level bees
        self.movement_timer = 0
        self.movement_delay = random.randrange(60, 120)  # 1-2 seconds at 60 FPS
        self.movement_pattern = random.choice(["zigzag", "circle", "straight"])
        self.angle = 0  # For circular movement

        # Animation variables
        self.wing_timer = 0
        self.wing_state = 0
        self.wing_delay = random.randrange(5, 15)  # Random wing flap speed

    def create_bee_image(self):
        # Create a surface sized according to the bee's level
        size = int(50 * self.size)
        surf = pygame.Surface((size, size))
        surf.fill(BLACK)

        # Calculate center and scaling factors
        center = size // 2
        scale = self.size

        # Body - oval shape
        body_width = int(30 * scale)
        body_height = int(20 * scale)
        body_x = center - body_width // 2
        body_y = center - body_height // 2
        pygame.draw.ellipse(surf, self.color, (body_x, body_y, body_width, body_height))

        # Stripes - number based on level
        stripe_count = min(self.level + 1, 5)  # 2 for level 1, 3 for level 2, etc.
        stripe_spacing = body_height / (stripe_count + 1)
        for i in range(stripe_count):
            y_pos = body_y + (i + 1) * stripe_spacing
            pygame.draw.line(surf, BLACK,
                            (body_x, int(y_pos)),
                            (body_x + body_width, int(y_pos)),
                            max(1, int(2 * scale)))

        # Head
        head_radius = int(8 * scale)
        head_x = body_x - head_radius // 2
        head_y = center
        pygame.draw.circle(surf, LIGHT_YELLOW, (head_x, head_y), head_radius)

        # Eyes
        eye_radius = int(2 * scale)
        pygame.draw.circle(surf, BLACK, (head_x - 3, head_y - 2), eye_radius)
        pygame.draw.circle(surf, BLACK, (head_x + 3, head_y - 2), eye_radius)

        # Antennae
        pygame.draw.line(surf, BLACK, (head_x - 3, head_y - 5), (head_x - 5, head_y - 10), 1)
        pygame.draw.line(surf, BLACK, (head_x + 3, head_y - 5), (head_x + 5, head_y - 10), 1)
        pygame.draw.circle(surf, BLACK, (head_x - 5, head_y - 10), int(scale))
        pygame.draw.circle(surf, BLACK, (head_x + 5, head_y - 10), int(scale))

        # Wings
        wing_width = int(15 * scale)
        wing_height = int(10 * scale)
        pygame.draw.ellipse(surf, WHITE, (center - wing_width // 2, body_y - wing_height // 2, wing_width, wing_height))
        pygame.draw.ellipse(surf, WHITE, (center, body_y - wing_height // 2, wing_width, wing_height))

        # Stinger
        stinger_size = int(5 * scale)
        pygame.draw.polygon(surf, ORANGE,
                           [(body_x + body_width, center),
                            (body_x + body_width + stinger_size, center - stinger_size // 2),
                            (body_x + body_width + stinger_size, center + stinger_size // 2)])

        # Level indicator (crown for queen, etc.)
        if self.level == ENEMY_LEVEL_4:  # Queen bee
            crown_height = int(6 * scale)
            crown_width = int(12 * scale)
            crown_x = center - crown_width // 2
            crown_y = body_y - crown_height
            # Draw a crown
            pygame.draw.polygon(surf, YELLOW,
                              [(crown_x, crown_y),
                               (crown_x + crown_width // 4, crown_y - crown_height),
                               (crown_x + crown_width // 2, crown_y),
                               (crown_x + 3 * crown_width // 4, crown_y - crown_height),
                               (crown_x + crown_width, crown_y)])

        surf.set_colorkey(BLACK)
        return surf

    def update(self):
        # Apply different movement patterns based on level
        if self.level >= ENEMY_LEVEL_3:  # Elite and Queen bees have special movement
            self.movement_timer += 1

            if self.movement_timer >= self.movement_delay:
                self.movement_timer = 0
                # Change movement pattern occasionally
                self.movement_pattern = random.choice(["zigzag", "circle", "straight"])
                self.movement_delay = random.randrange(60, 120)

            if self.movement_pattern == "zigzag":
                # Zigzag pattern - with speed caps
                if self.movement_timer % 30 < 15:  # Switch direction every 15 frames
                    # Use a fixed value instead of multiplying by speed_factor again
                    self.speedx = min(1.5, abs(self.speedx))
                else:
                    self.speedx = max(-1.5, -abs(self.speedx))

            elif self.movement_pattern == "circle":
                # Circular pattern - with speed caps
                self.angle += 0.05
                # Use a fixed multiplier instead of speed_factor
                self.speedx = math.sin(self.angle) * 1.5
                # Keep moving downward at a reasonable speed
                self.speedy = min(2.5, abs(self.speedy))

            # For straight pattern, just use the current speeds

        # Move the bee
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Wing animation
        self.wing_timer += 1
        if self.wing_timer > self.wing_delay:
            self.wing_timer = 0
            self.wing_state = 1 - self.wing_state  # Toggle between 0 and 1

            # Create a copy of the base image for animation
            self.image = self.base_image.copy()

            # Add wing animation by drawing different wings based on state
            center = int(self.image.get_width() // 2)
            body_y = center - int(10 * self.size)
            wing_width = int(15 * self.size)
            wing_height = int(10 * self.size)

            if self.wing_state == 0:
                # Wings up
                wing_y = body_y - wing_height // 2 - int(4 * self.size)
            else:
                # Wings down
                wing_y = body_y - wing_height // 2 + int(4 * self.size)

            # Clear previous wings
            pygame.draw.ellipse(self.image, BLACK, (center - wing_width // 2, body_y - wing_height // 2 - int(5 * self.size),
                                                 wing_width, wing_height + int(10 * self.size)))
            pygame.draw.ellipse(self.image, BLACK, (center, body_y - wing_height // 2 - int(5 * self.size),
                                                 wing_width, wing_height + int(10 * self.size)))

            # Draw new wings
            pygame.draw.ellipse(self.image, WHITE, (center - wing_width // 2, wing_y, wing_width, wing_height))
            pygame.draw.ellipse(self.image, WHITE, (center, wing_y, wing_width, wing_height))

        # If bee goes off screen, respawn it
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 25:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

            # Reset movement with the same speed caps as initialization
            base_speedy = random.randrange(1, 3)  # Reduced upper limit
            base_speedx = random.randrange(-1, 2)  # Reduced range

            # Apply speed factor with caps
            self.speedy = min(base_speedy * self.speed_factor, 3.5)  # Cap vertical speed
            self.speedx = max(min(base_speedx * self.speed_factor, 2.0), -2.0)  # Cap horizontal speed

            self.wing_delay = random.randrange(5, 15)  # Randomize wing flap speed

    def hit(self, damage):
        """Handle being hit by a bullet or missile"""
        self.health -= damage
        # Flash the bee white briefly to indicate damage
        self.color = WHITE
        self.base_image = self.create_bee_image()
        self.image = self.base_image

        # Schedule color restoration
        pygame.time.set_timer(pygame.USEREVENT, 100)  # 100ms flash

        # Return True if the bee is destroyed
        return self.health <= 0

# Explosion class for visual effects
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super(Explosion, self).__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 2
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.frame += 1
            if self.frame == 1:
                # First frame - small explosion
                self.image = pygame.Surface((30, 30))
                self.image.fill(BLACK)
                pygame.draw.circle(self.image, YELLOW, (15, 15), 5)
                self.image.set_colorkey(BLACK)
            elif self.frame == 2:
                # Second frame - medium explosion
                self.image = pygame.Surface((30, 30))
                self.image.fill(BLACK)
                pygame.draw.circle(self.image, ORANGE, (15, 15), 10)
                self.image.set_colorkey(BLACK)
            elif self.frame == 3:
                # Third frame - large explosion
                self.image = pygame.Surface((30, 30))
                self.image.fill(BLACK)
                pygame.draw.circle(self.image, RED, (15, 15), 15)
                self.image.set_colorkey(BLACK)
            elif self.frame > 3:
                self.kill()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0, powered=False, damage_boost=False):
        super(Bullet, self).__init__()

        if powered:
            # Create a larger, more powerful bullet (level 5 center beam)
            self.image = pygame.Surface((10, 20))
            self.image.fill(BLACK)
            pygame.draw.rect(self.image, PURPLE, (0, 0, 10, 20))
            pygame.draw.rect(self.image, WHITE, (4, 0, 2, 20))
            self.damage = 3
        elif damage_boost:
            # Enhanced bullet for weapon level 4 (same size but more damage)
            self.image = pygame.Surface((5, 15))
            self.image.fill(BLACK)

            # Red-orange color for level 4 bullets
            color = ORANGE

            pygame.draw.rect(self.image, color, (0, 0, 5, 15))
            pygame.draw.rect(self.image, WHITE, (2, 0, 1, 15))
            # Add a glow effect
            self.damage = 2  # Double damage compared to regular bullets
        else:
            # Regular bullet with color based on angle
            self.image = pygame.Surface((5, 15))
            self.image.fill(BLACK)

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

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.speedx = angle  # Horizontal movement based on angle

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # Kill if it moves off the screen
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# Game function
def game():
    global all_sprites, bullets, bees, score, missiles_group

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    bees = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    missiles_group = pygame.sprite.Group()

    # Create background
    background = load_image("background")

    # Create player
    player = Player()
    all_sprites.add(player)

    # Create bees with different levels
    for _ in range(8):
        new_bee = Bee()  # Random level based on distribution
        all_sprites.add(new_bee)
        bees.add(new_bee)

    # Score
    score = 0
    font = pygame.font.Font(None, 36)

    # Power-up spawn timer
    powerup_timer = pygame.time.get_ticks()
    powerup_delay = random.randrange(10000, 15000)  # 10-15 seconds

    # Game loop
    running = True
    game_over = False

    while running:
        # Keep loop running at the right speed
        clock.tick(FPS)

        # Process input (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False  # Exit the game
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    return False  # Exit the game
                if event.key == K_SPACE:
                    player.shoot()
                if event.key == K_b:
                    # Use bomb if available
                    bomb_effect = player.use_bomb()
                    if bomb_effect:
                        # Store bee data before destroying them
                        bee_data = [(bee.rect.center, bee.points, bee.level, bee.size, bee.drop_chance, bee.drop_weights) for bee in bees]

                        # Calculate score based on bee levels
                        total_score = sum(points for _, points, _, _, _, _ in bee_data)
                        score += total_score

                        # Remove all bees from sprite groups
                        for bee in bees:
                            bee.kill()  # This removes from all sprite groups

                        # Create explosions and potentially power-ups at all bee positions
                        for pos, _, _, size, drop_chance, drop_weights in bee_data:
                            # Create explosion sized based on bee level
                            explosion = Explosion(pos)
                            explosion_size = int(30 * size)
                            explosion.image = pygame.transform.scale(explosion.image, (explosion_size, explosion_size))
                            all_sprites.add(explosion)
                            explosions.add(explosion)

                            # Chance to spawn power-ups from bomb explosions (based on bee level)
                            # Bombs have a higher chance of generating power-ups
                            if random.random() < (drop_chance * 0.75):  # 75% of normal drop chance
                                # Favor bombs in the drop weights
                                weights = dict(drop_weights)  # Copy the weights
                                # Increase bomb weight
                                if "bomb" in weights:
                                    weights["bomb"] += 2

                                powerup_choices = []
                                for ptype, weight in weights.items():
                                    powerup_choices.extend([ptype] * weight)
                                powerup_type = random.choice(powerup_choices)

                                powerup = PowerUp(powerup_type)
                                powerup.rect.center = pos
                                all_sprites.add(powerup)
                                powerups.add(powerup)

                        # Spawn new bees after a delay (with level distribution)
                        for _ in range(8):
                            new_bee = Bee()
                            all_sprites.add(new_bee)
                            bees.add(new_bee)
                if event.key == K_m:
                    # Launch missile if available (manual launch)
                    player.launch_missile(auto_launch=False)
                if game_over and event.key == K_RETURN:
                    return True  # Restart the game

        if not game_over:
            # Update
            all_sprites.update()

            # Check for power-up spawn
            now = pygame.time.get_ticks()
            if now - powerup_timer > powerup_delay:
                powerup_timer = now
                powerup_delay = random.randrange(10000, 15000)  # 10-15 seconds
                powerup = PowerUp()
                all_sprites.add(powerup)
                powerups.add(powerup)

            # Check for bullet-bee collisions
            # Use a custom collision detection that doesn't automatically kill bees
            hits_dict = pygame.sprite.groupcollide(bees, bullets, False, True)
            for bee, bullet_list in hits_dict.items():
                # Apply damage from each bullet
                total_damage = sum(bullet.damage for bullet in bullet_list)

                # Check if the bee is destroyed
                if bee.hit(total_damage):
                    # Add score based on bee level
                    score += bee.points

                    # Create explosion at bee position (size based on bee level)
                    explosion = Explosion(bee.rect.center)
                    # Scale explosion based on bee size
                    explosion_size = int(30 * bee.size)
                    explosion.image = pygame.transform.scale(explosion.image, (explosion_size, explosion_size))
                    all_sprites.add(explosion)
                    explosions.add(explosion)

                    # Play explosion sound
                    sounds['explosion'].play()

                    # Random chance to spawn a power-up based on bee's drop chance
                    if random.random() < bee.drop_chance:
                        # Determine power-up type based on bee's drop weights
                        weights = bee.drop_weights
                        powerup_choices = []
                        for ptype, weight in weights.items():
                            powerup_choices.extend([ptype] * weight)
                        powerup_type = random.choice(powerup_choices)

                        powerup = PowerUp(powerup_type)
                        powerup.rect.center = bee.rect.center
                        all_sprites.add(powerup)
                        powerups.add(powerup)

                    # Remove the bee
                    bee.kill()

                    # Create a new bee (with level distribution)
                    new_bee = Bee()
                    all_sprites.add(new_bee)
                    bees.add(new_bee)

            # Check for missile-bee collisions
            hits_dict = pygame.sprite.groupcollide(bees, missiles_group, False, True)
            for bee, missile_list in hits_dict.items():
                # Apply damage from each missile (missiles do more damage)
                total_damage = sum(missile.damage for missile in missile_list)

                # Check if the bee is destroyed
                if bee.hit(total_damage):
                    # Add score based on bee level (bonus for missile kills)
                    score += int(bee.points * 1.5)  # 50% bonus for missile kills

                    # Create larger explosion at bee position
                    explosion = Explosion(bee.rect.center)
                    # Scale explosion based on bee size and missile bonus
                    explosion_size = int(40 * bee.size)  # Bigger than bullet explosions
                    explosion.image = pygame.transform.scale(explosion.image, (explosion_size, explosion_size))
                    all_sprites.add(explosion)
                    explosions.add(explosion)

                    # Play explosion sound
                    sounds['explosion'].play()

                    # Higher chance to spawn a power-up with missiles (1.5x normal drop rate)
                    if random.random() < (bee.drop_chance * 1.5):
                        # Determine power-up type with weighted probabilities favoring missiles
                        weights = dict(bee.drop_weights)  # Copy the weights
                        # Increase missile weight
                        if "missile" in weights:
                            weights["missile"] += 1

                        powerup_choices = []
                        for ptype, weight in weights.items():
                            powerup_choices.extend([ptype] * weight)
                        powerup_type = random.choice(powerup_choices)

                        powerup = PowerUp(powerup_type)
                        powerup.rect.center = bee.rect.center
                        all_sprites.add(powerup)
                        powerups.add(powerup)

                    # Remove the bee
                    bee.kill()

                    # Create a new bee (with level distribution)
                    new_bee = Bee()
                    all_sprites.add(new_bee)
                    bees.add(new_bee)

            # Check for player-powerup collisions
            hits = pygame.sprite.spritecollide(player, powerups, True)
            for hit in hits:
                if hit.type == "weapon_upgrade":
                    player.upgrade_weapon()
                elif hit.type == "bomb":
                    player.add_bomb()
                elif hit.type == "missile":
                    player.add_missile()
                elif hit.type == "missile_upgrade":
                    player.upgrade_missile()

            # Check for bee-player collisions
            hits = pygame.sprite.spritecollide(player, bees, False)
            if hits:
                game_over = True
                # Play game over sound
                sounds['game_over'].play()

        # Draw / render
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw weapon level
        weapon_text = font.render(f"Weapon: Level {player.weapon_level}", True, WHITE)
        screen.blit(weapon_text, (SCREEN_WIDTH - weapon_text.get_width() - 10, 10))

        # Draw bomb count
        bomb_text = font.render(f"Bombs: {player.bombs}", True, WHITE)
        screen.blit(bomb_text, (SCREEN_WIDTH - bomb_text.get_width() - 10, 50))

        # Draw missile count and level
        missile_text = font.render(f"Missiles: {player.missiles} (Lvl {player.missile_level})", True, WHITE)
        screen.blit(missile_text, (SCREEN_WIDTH - missile_text.get_width() - 10, 90))

        # Draw missile level indicator with color based on level
        if player.missile_level == MISSILE_LEVEL_1:
            missile_level_color = GREEN
        elif player.missile_level == MISSILE_LEVEL_2:
            missile_level_color = CYAN
        elif player.missile_level == MISSILE_LEVEL_3:
            missile_level_color = PURPLE
        else:  # MISSILE_LEVEL_4
            missile_level_color = RED

        # Draw missile level indicator dots
        for i in range(player.missile_level):
            pygame.draw.circle(screen, missile_level_color,
                             (SCREEN_WIDTH - 20 - (i * 10), 110), 3)

        # Draw game over screen
        if game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Press ENTER to restart or ESC to quit", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                        SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 + 50))

        # Flip the display
        pygame.display.flip()

    return False

# Main menu
def main_menu():
    font = pygame.font.Font(None, 74)
    title_text = font.render("BEE SHOOTER", True, YELLOW)

    font = pygame.font.Font(None, 36)
    start_text = font.render("Press ENTER to start", True, WHITE)
    quit_text = font.render("Press ESC to quit", True, WHITE)

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    if game():  # Start the game
                        continue  # If game returns True, continue to main menu
                    else:
                        return False  # If game returns False, exit
                elif event.key == K_ESCAPE:
                    return False

        screen.fill(BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()
