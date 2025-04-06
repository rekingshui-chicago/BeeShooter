"""
Player entity
"""
import pygame
import math
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, ORANGE, YELLOW,
    WEAPON_LEVEL_1, WEAPON_LEVEL_2, WEAPON_LEVEL_3, WEAPON_LEVEL_4, WEAPON_LEVEL_5,
    MISSILE_LEVEL_1, MISSILE_LEVEL_2, MISSILE_LEVEL_3, MISSILE_LEVEL_4
)
from src.utils.resources import load_image, sounds
from src.entities.bullet import Bullet
from src.entities.missile import Missile

class Player(pygame.sprite.Sprite):
    """Player class representing the player's ship"""
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
        self.bombs = 3  # Start with 3 bombs
        self.bomb_delay = 500  # Cooldown between bomb uses
        self.last_bomb = 0
        self.missiles = 3  # Start with 3 missiles
        self.missile_level = MISSILE_LEVEL_1  # Start with basic missiles
        self.missile_delay = 1000  # Cooldown between missile launches
        self.last_missile = 0
        self.engine_flames = []  # Initialize engine flames list

    def update(self):
        """Update player position and state"""
        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Movement
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed

        # Force the player to be within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Engine animation - more intense when moving
        self.engine_flicker = (self.engine_flicker + 1) % 6

        # Load the base fighter image
        self.image = load_image("player")

        # Add engine flames
        self.draw_engine_flames()

    def draw_engine_flames(self):
        """Draw engine flames on the player ship"""
        # Engine flame positions (adjust based on your ship design)
        flame_positions = [(40, 45)]  # Center engine

        # Add side engines for higher weapon levels
        if self.weapon_level >= WEAPON_LEVEL_3:
            flame_positions.extend([(30, 40), (50, 40)])  # Side engines

        # Draw flames with flicker effect
        for pos in flame_positions:
            # Flame size varies with flicker
            flame_height = 5 + (self.engine_flicker % 3)
            flame_width = 3

            # Flame colors
            colors = [ORANGE, YELLOW, WHITE]

            # Draw flame layers (from outside to inside)
            for i, color in enumerate(colors):
                # Each layer is smaller than the outer one
                layer_height = flame_height - i
                layer_width = flame_width - (i * 0.5)

                if layer_height > 0 and layer_width > 0:
                    # Create flame polygon
                    flame_points = [
                        (pos[0] - layer_width/2, pos[1]),  # Top left
                        (pos[0] + layer_width/2, pos[1]),  # Top right
                        (pos[0], pos[1] + layer_height)    # Bottom point
                    ]

                    # Draw flame on ship image
                    pygame.draw.polygon(self.image, color, flame_points)

    def shoot(self):
        """Create bullets based on weapon level"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now

            bullets = []

            # Different bullet patterns based on weapon level
            if self.weapon_level == WEAPON_LEVEL_1:
                # Single bullet
                bullets.append(Bullet(self.rect.centerx, self.rect.top))

            elif self.weapon_level == WEAPON_LEVEL_2:
                # Two bullets side by side
                bullets.append(Bullet(self.rect.left + 10, self.rect.top))
                bullets.append(Bullet(self.rect.right - 10, self.rect.top))

            elif self.weapon_level == WEAPON_LEVEL_3:
                # Three bullets - one center, two angled
                bullets.append(Bullet(self.rect.centerx, self.rect.top))
                bullets.append(Bullet(self.rect.left + 10, self.rect.top, -1))
                bullets.append(Bullet(self.rect.right - 10, self.rect.top, 1))

            elif self.weapon_level == WEAPON_LEVEL_4:
                # Four bullets - two straight, two angled
                bullets.append(Bullet(self.rect.centerx - 15, self.rect.top))
                bullets.append(Bullet(self.rect.centerx + 15, self.rect.top))
                bullets.append(Bullet(self.rect.left + 5, self.rect.top, -1))
                bullets.append(Bullet(self.rect.right - 5, self.rect.top, 1))

            elif self.weapon_level == WEAPON_LEVEL_5:
                # Five bullets - three straight, two angled
                bullets.append(Bullet(self.rect.centerx, self.rect.top))
                bullets.append(Bullet(self.rect.centerx - 20, self.rect.top))
                bullets.append(Bullet(self.rect.centerx + 20, self.rect.top))
                bullets.append(Bullet(self.rect.left + 5, self.rect.top, -2))
                bullets.append(Bullet(self.rect.right - 5, self.rect.top, 2))

            # Play shooting sound
            sounds['shoot'].play()

            return bullets

        return None

    def upgrade_weapon(self):
        """Upgrade the player's weapon"""
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
        """Add a bomb to the player's inventory"""
        self.bombs += 1
        sounds['powerup'].play()

    def bomb(self):
        """Use a bomb if available and not on cooldown"""
        # Check if player has bombs available
        if self.bombs <= 0:
            # Silently fail - no bombs available
            return False

        # Check if cooldown has expired
        now = pygame.time.get_ticks()
        cooldown_active = now - self.last_bomb < self.bomb_delay

        if cooldown_active:
            # Silently fail - cooldown active
            return False

        # Use a bomb
        self.bombs -= 1
        self.last_bomb = now

        # Play bomb sound
        sounds['bomb'].play()

        # Force event processing to ensure keyboard input isn't blocked
        pygame.event.pump()

        return True

    def add_missile(self):
        """Add missiles to the player's inventory"""
        self.missiles += 2  # Add 2 missiles at a time
        sounds['powerup'].play()

    def upgrade_missile(self):
        """Upgrade the player's missiles"""
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
        """Launch missiles based on missile level"""
        now = pygame.time.get_ticks()

        # Check if player has missiles and cooldown has expired
        if self.missiles > 0 and now - self.last_missile > self.missile_delay:
            self.last_missile = now
            self.missiles -= 1

            launched_missiles = []

            # Different missile patterns based on missile level
            # All missiles are target seeking with increased damage for higher levels
            if self.missile_level == MISSILE_LEVEL_1:
                # Single missile
                launched_missiles.append(Missile(self.rect.centerx, self.rect.top, damage=1, target_seeking=True))

            elif self.missile_level == MISSILE_LEVEL_2:
                # Two missiles with slight spread and increased damage
                launched_missiles.append(Missile(self.rect.centerx - 10, self.rect.top, damage=2, target_seeking=True))
                launched_missiles.append(Missile(self.rect.centerx + 10, self.rect.top, damage=2, target_seeking=True))

            elif self.missile_level == MISSILE_LEVEL_3:
                # Three missiles with wider spread and increased damage
                launched_missiles.append(Missile(self.rect.centerx, self.rect.top, damage=3, target_seeking=True))
                launched_missiles.append(Missile(self.rect.centerx - 20, self.rect.top, damage=3, target_seeking=True))
                launched_missiles.append(Missile(self.rect.centerx + 20, self.rect.top, damage=3, target_seeking=True))

            elif self.missile_level == MISSILE_LEVEL_4:
                # Four missiles with maximum spread and damage
                launched_missiles.append(Missile(self.rect.centerx - 15, self.rect.top, damage=4, target_seeking=True))
                launched_missiles.append(Missile(self.rect.centerx + 15, self.rect.top, damage=4, target_seeking=True))
                launched_missiles.append(Missile(self.rect.centerx - 30, self.rect.top, damage=4, target_seeking=True))
                launched_missiles.append(Missile(self.rect.centerx + 30, self.rect.top, damage=4, target_seeking=True))

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
