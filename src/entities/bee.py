"""
Bee entity (enemy)
"""
import pygame
import random
import math
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, YELLOW, ORANGE, RED, PURPLE, GREY,
    ENEMY_LEVEL_1, ENEMY_LEVEL_2, ENEMY_LEVEL_3, ENEMY_LEVEL_4
)
from src.utils.resources import load_image

class Bee(pygame.sprite.Sprite):
    """Bee class for enemies"""
    def __init__(self, level=None):
        super(Bee, self).__init__()

        # Initialize wing state variables first to avoid attribute errors
        self.wing_state = 0  # 0: wings up, 1: wings middle, 2: wings down
        self.wing_timer = 0
        self.wing_delay = 5  # Frames between wing state changes

        # Randomly choose level if not specified, with more higher level enemies
        if level is None:
            # Level distribution: 40% level 1, 30% level 2, 20% level 3, 10% level 4
            # (Changed from 60/25/10/5 to 40/30/20/10 - more higher level enemies)
            level_choices = [ENEMY_LEVEL_1] * 40 + [ENEMY_LEVEL_2] * 30 + [ENEMY_LEVEL_3] * 20 + [ENEMY_LEVEL_4] * 10
            self.level = random.choice(level_choices)
        else:
            self.level = level

        # Faster wing flapping for higher level bees
        if self.level >= ENEMY_LEVEL_3:
            self.wing_delay = 3  # Elite and Queen bees flap wings faster

        # Set properties based on level
        if self.level == ENEMY_LEVEL_1:
            # Basic bee (increased speed from 1.0 to 1.2)
            self.health = 1
            self.speed_factor = 1.2
            self.points = 10
            self.color = YELLOW
            self.size = 1.0
            self.drop_chance = 0.10  # 10% chance to drop power-up
            self.drop_weights = {"weapon_upgrade": 3, "bomb": 2, "missile": 2, "missile_upgrade": 3}  # 30% weapon, 20% bomb, 20% missile, 30% missile upgrade
        elif self.level == ENEMY_LEVEL_2:
            # Soldier bee (increased speed from 1.2 to 1.4)
            self.health = 2
            self.speed_factor = 1.4
            self.points = 20
            self.color = ORANGE
            self.size = 1.2
            self.drop_chance = 0.15  # 15% chance to drop power-up
            self.drop_weights = {"weapon_upgrade": 3, "bomb": 2, "missile": 2, "missile_upgrade": 3}  # 30% weapon, 20% bomb, 20% missile, 30% missile upgrade
        elif self.level == ENEMY_LEVEL_3:
            # Elite bee (increased speed from 1.3 to 1.6)
            self.health = 3
            self.speed_factor = 1.6
            self.points = 30
            self.color = RED
            self.size = 1.4
            self.drop_chance = 0.20  # 20% chance to drop power-up
            self.drop_weights = {"weapon_upgrade": 3, "bomb": 2, "missile": 2, "missile_upgrade": 3}  # 30% weapon, 20% bomb, 20% missile, 30% missile upgrade
        elif self.level == ENEMY_LEVEL_4:
            # Queen bee (increased speed from 0.9 to 1.1)
            self.health = 5
            self.speed_factor = 1.1
            self.points = 50
            self.color = PURPLE
            self.size = 1.8
            self.drop_chance = 0.30  # 30% chance to drop power-up
            self.drop_weights = {"weapon_upgrade": 3, "bomb": 2, "missile": 2, "missile_upgrade": 3}  # 30% weapon, 20% bomb, 20% missile, 30% missile upgrade

        # Create the base image
        self.base_image = self.create_bee_image()
        self.image = self.base_image
        self.rect = self.image.get_rect()

        # Position - ensure width is valid before using it
        if self.rect.width > 0:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        else:
            self.rect.x = random.randrange(SCREEN_WIDTH - 30)  # Use default width
        self.rect.y = random.randrange(-100, -40)

        # Movement - reduced speed range for lower difficulty
        base_speedy = random.randrange(1, 3)  # Reduced from (2,4) to (1,3)
        base_speedx = random.randrange(-1, 2)  # Reduced from (-2,3) to (-1,2)

        # Apply speed factor with a lower maximum cap
        self.speedy = min(base_speedy * self.speed_factor, 3.0)  # Reduced cap from 5.0 to 3.0
        self.speedx = max(min(base_speedx * self.speed_factor, 2.0), -2.0)  # Reduced cap from 3.0 to 2.0

        # Special movement patterns for higher level bees
        self.movement_pattern = "straight"  # Default pattern
        self.movement_timer = 0
        self.angle = 0  # For circular movement

        # Higher level bees have special movement patterns
        if self.level == ENEMY_LEVEL_3:
            # Elite bees have zigzag movement
            self.movement_pattern = "zigzag"
        elif self.level == ENEMY_LEVEL_4:
            # Queen bees have circular movement
            self.movement_pattern = "circle"

    def create_bee_image(self):
        # Pass wing_state to the method
        """Create the bee image based on level and size with evil cartoon style"""
        # Base size is 30x30, scaled by self.size
        width = int(30 * self.size)
        height = int(30 * self.size)

        image = pygame.Surface((width, height), pygame.SRCALPHA)

        # Body - more oval shaped for cartoon look
        body_width = int(width * 0.45)
        body_height = int(height * 0.5)
        body_rect = pygame.Rect(
            width // 2 - body_width,
            height // 2 - body_height // 2,
            body_width * 2,
            body_height
        )
        pygame.draw.ellipse(image, self.color, body_rect)

        # Add body outline for cartoon effect
        pygame.draw.ellipse(image, BLACK, body_rect, max(1, int(width * 0.03)))

        # Stripes - curved for cartoon look
        stripe_count = 3
        stripe_spacing = body_height / (stripe_count + 1)

        for i in range(stripe_count):
            stripe_y = body_rect.top + stripe_spacing * (i + 1)
            stripe_width = int(body_width * 1.6)
            stripe_height = max(2, int(height * 0.08))

            # Create curved stripe effect
            stripe_rect = pygame.Rect(
                width // 2 - stripe_width // 2,
                int(stripe_y - stripe_height // 2),
                stripe_width,
                stripe_height
            )
            pygame.draw.ellipse(image, BLACK, stripe_rect)

        # Wings - more cartoon style with outlines and flapping animation
        wing_width = int(width * 0.35)
        wing_height = int(height * 0.4)

        # Adjust wing position and shape based on wing state
        wing_offset_y = 0
        wing_scale_y = 1.0

        if self.wing_state == 0:  # Wings up
            wing_offset_y = -int(height * 0.1)  # Move wings up
            wing_scale_y = 0.8  # Slightly narrower wings
        elif self.wing_state == 1:  # Wings middle (default)
            wing_offset_y = 0
            wing_scale_y = 1.0
        elif self.wing_state == 2:  # Wings down
            wing_offset_y = int(height * 0.1)  # Move wings down
            wing_scale_y = 0.8  # Slightly narrower wings

        # Calculate actual wing height with scaling
        actual_wing_height = int(wing_height * wing_scale_y)

        # Left wing
        left_wing_rect = pygame.Rect(
            width // 2 - wing_width * 1.8,
            height // 2 - actual_wing_height // 2 + wing_offset_y,
            wing_width,
            actual_wing_height
        )
        pygame.draw.ellipse(image, WHITE, left_wing_rect)
        pygame.draw.ellipse(image, BLACK, left_wing_rect, max(1, int(width * 0.02)))

        # Right wing
        right_wing_rect = pygame.Rect(
            width // 2 + wing_width * 0.8,
            height // 2 - actual_wing_height // 2 + wing_offset_y,
            wing_width,
            actual_wing_height
        )
        pygame.draw.ellipse(image, WHITE, right_wing_rect)
        pygame.draw.ellipse(image, BLACK, right_wing_rect, max(1, int(width * 0.02)))

        # Add wing motion blur effect for faster flapping (higher level bees)
        if self.level >= ENEMY_LEVEL_3 and self.wing_state != 1:  # Only for up and down states
            # Semi-transparent motion blur
            blur_color = (255, 255, 255, 100)  # White with alpha

            # Blur for left wing
            blur_left_rect = pygame.Rect(
                left_wing_rect.left,
                height // 2 - wing_height // 2,  # Middle position
                wing_width,
                wing_height
            )
            blur_surface = pygame.Surface((wing_width, wing_height), pygame.SRCALPHA)
            pygame.draw.ellipse(blur_surface, blur_color,
                              (0, 0, wing_width, wing_height))
            image.blit(blur_surface, (blur_left_rect.left, blur_left_rect.top))

            # Blur for right wing
            blur_right_rect = pygame.Rect(
                right_wing_rect.left,
                height // 2 - wing_height // 2,  # Middle position
                wing_width,
                wing_height
            )
            image.blit(blur_surface, (blur_right_rect.left, blur_right_rect.top))

        # Evil eyes - different based on level
        eye_width = int(width * 0.15)
        eye_height = int(height * 0.2)
        eye_offset_x = int(width * 0.15)
        eye_offset_y = int(height * 0.1)

        # Left eye
        left_eye_rect = pygame.Rect(
            width // 2 - eye_offset_x - eye_width // 2,
            height // 2 - eye_offset_y - eye_height // 2,
            eye_width,
            eye_height
        )

        # Right eye
        right_eye_rect = pygame.Rect(
            width // 2 + eye_offset_x - eye_width // 2,
            height // 2 - eye_offset_y - eye_height // 2,
            eye_width,
            eye_height
        )

        # Different eye styles based on level
        if self.level == ENEMY_LEVEL_1:
            # Basic bee - simple oval eyes
            pygame.draw.ellipse(image, BLACK, left_eye_rect)
            pygame.draw.ellipse(image, BLACK, right_eye_rect)

            # Add white reflection dots for cartoon effect
            reflection_size = max(1, int(eye_width * 0.3))
            pygame.draw.circle(image, WHITE,
                              (left_eye_rect.left + reflection_size, left_eye_rect.top + reflection_size),
                              reflection_size)
            pygame.draw.circle(image, WHITE,
                              (right_eye_rect.left + reflection_size, right_eye_rect.top + reflection_size),
                              reflection_size)

        elif self.level == ENEMY_LEVEL_2:
            # Soldier bee - angry eyes (inverted triangles)
            left_eye_points = [
                (left_eye_rect.left, left_eye_rect.top),
                (left_eye_rect.right, left_eye_rect.top),
                (left_eye_rect.centerx, left_eye_rect.bottom)
            ]
            right_eye_points = [
                (right_eye_rect.left, right_eye_rect.top),
                (right_eye_rect.right, right_eye_rect.top),
                (right_eye_rect.centerx, right_eye_rect.bottom)
            ]
            pygame.draw.polygon(image, BLACK, left_eye_points)
            pygame.draw.polygon(image, BLACK, right_eye_points)

        elif self.level == ENEMY_LEVEL_3:
            # Elite bee - evil slanted eyes
            pygame.draw.ellipse(image, BLACK, left_eye_rect)
            pygame.draw.ellipse(image, BLACK, right_eye_rect)

            # Add red pupils
            pupil_size = max(1, int(eye_width * 0.4))
            pygame.draw.circle(image, RED,
                              (left_eye_rect.centerx, left_eye_rect.centery),
                              pupil_size)
            pygame.draw.circle(image, RED,
                              (right_eye_rect.centerx, right_eye_rect.centery),
                              pupil_size)

        elif self.level == ENEMY_LEVEL_4:
            # Queen bee - crown and glowing eyes
            pygame.draw.ellipse(image, BLACK, left_eye_rect)
            pygame.draw.ellipse(image, BLACK, right_eye_rect)

            # Glowing yellow pupils
            pupil_size = max(1, int(eye_width * 0.5))
            pygame.draw.circle(image, YELLOW,
                              (left_eye_rect.centerx, left_eye_rect.centery),
                              pupil_size)
            pygame.draw.circle(image, YELLOW,
                              (right_eye_rect.centerx, right_eye_rect.centery),
                              pupil_size)

            # Add a crown
            crown_height = int(height * 0.2)
            crown_width = int(width * 0.4)
            crown_points = [
                (width // 2 - crown_width // 2, height // 2 - body_height // 2 - crown_height // 2),  # Left base
                (width // 2 - crown_width // 4, height // 2 - body_height // 2 - crown_height),  # Left point
                (width // 2, height // 2 - body_height // 2 - crown_height // 3),  # Middle valley
                (width // 2 + crown_width // 4, height // 2 - body_height // 2 - crown_height),  # Right point
                (width // 2 + crown_width // 2, height // 2 - body_height // 2 - crown_height // 2)  # Right base
            ]
            pygame.draw.polygon(image, YELLOW, crown_points)
            pygame.draw.polygon(image, BLACK, crown_points, max(1, int(width * 0.02)))

        # Mouth - evil grin
        mouth_width = int(width * 0.3)
        mouth_height = int(height * 0.1)
        mouth_rect = pygame.Rect(
            width // 2 - mouth_width // 2,
            height // 2 + eye_offset_y - mouth_height // 2,
            mouth_width,
            mouth_height
        )

        # Different mouth styles based on level
        if self.level == ENEMY_LEVEL_1:
            # Basic smile
            pygame.draw.arc(image, BLACK, mouth_rect, 0, math.pi, 2)
        elif self.level == ENEMY_LEVEL_2 or self.level == ENEMY_LEVEL_3:
            # Evil grin with teeth
            pygame.draw.arc(image, BLACK, mouth_rect, 0, math.pi, 2)

            # Add teeth
            tooth_width = max(1, int(mouth_width * 0.15))
            tooth_height = max(1, int(mouth_height * 0.6))
            tooth_count = 3
            tooth_spacing = (mouth_width - tooth_width * tooth_count) / (tooth_count + 1)

            for i in range(tooth_count):
                tooth_x = mouth_rect.left + tooth_spacing * (i + 1) + tooth_width * i
                tooth_y = mouth_rect.centery
                pygame.draw.rect(image, WHITE, (tooth_x, tooth_y, tooth_width, tooth_height))
        elif self.level == ENEMY_LEVEL_4:
            # Queen bee - wider evil grin
            wider_mouth_rect = pygame.Rect(
                width // 2 - mouth_width * 0.7,
                height // 2 + eye_offset_y - mouth_height // 2,
                mouth_width * 1.4,
                mouth_height
            )
            pygame.draw.arc(image, BLACK, wider_mouth_rect, 0, math.pi, 3)

            # Add more teeth
            tooth_width = max(1, int(mouth_width * 0.12))
            tooth_height = max(1, int(mouth_height * 0.8))
            tooth_count = 5
            tooth_spacing = (mouth_width * 1.4 - tooth_width * tooth_count) / (tooth_count + 1)

            for i in range(tooth_count):
                tooth_x = wider_mouth_rect.left + tooth_spacing * (i + 1) + tooth_width * i
                tooth_y = wider_mouth_rect.centery
                pygame.draw.rect(image, WHITE, (tooth_x, tooth_y, tooth_width, tooth_height))

        # Stinger - sharper and more menacing
        stinger_width = int(width * 0.1)
        stinger_height = int(height * 0.25)  # Longer stinger
        stinger_points = [
            (width // 2 - stinger_width // 2, height // 2 + body_height // 2 - stinger_width // 2),
            (width // 2 + stinger_width // 2, height // 2 + body_height // 2 - stinger_width // 2),
            (width // 2, height // 2 + body_height // 2 + stinger_height)
        ]
        pygame.draw.polygon(image, BLACK, stinger_points)

        return image

    def update(self):
        """Update bee position and behavior"""
        # Update movement timer
        self.movement_timer += 1

        # Update wing flapping animation
        self.wing_timer += 1
        if self.wing_timer >= self.wing_delay:
            self.wing_timer = 0
            # Cycle through wing states: 0 (up) -> 1 (middle) -> 2 (down) -> 1 (middle) -> 0 (up)
            if self.wing_state == 0:
                self.wing_state = 1  # middle
            elif self.wing_state == 1:
                # If coming from up (0), go to down (2), if coming from down (2), go to up (0)
                self.wing_state = 2 if self.wing_timer == 0 else 0
            elif self.wing_state == 2:
                self.wing_state = 1  # middle

            # Recreate the bee image with the new wing state
            self.base_image = self.create_bee_image()
            self.image = self.base_image

        # Apply special movement patterns
        if self.movement_pattern != "straight":
            if self.movement_pattern == "zigzag":
                # Zigzag pattern - with reduced speed caps
                if self.movement_timer % 30 < 15:  # Switch direction every 15 frames
                    # Reduced from 2.5 to 1.5
                    self.speedx = min(1.5, abs(self.speedx))
                else:
                    self.speedx = max(-1.5, -abs(self.speedx))

            elif self.movement_pattern == "circle":
                # Circular pattern - with reduced speed caps
                self.angle += 0.05  # Reduced from 0.08 to 0.05 for slower circular movement
                # Reduced from 2.5 to 1.5
                self.speedx = math.sin(self.angle) * 1.5
                # Keep moving downward at a slower speed (reduced from 3.5 to 2.0)
                self.speedy = min(2.0, abs(self.speedy))

        # Update position
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # If bee goes off screen, reset position
        if (self.rect.top > SCREEN_HEIGHT + 10 or
            self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 25):

            # Reset position - ensure width is valid before using it
            if self.rect.width > 0:
                self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            else:
                self.rect.x = random.randrange(SCREEN_WIDTH - 30)  # Use default width
            self.rect.y = random.randrange(-100, -40)

            # Reset movement with reduced speed ranges (same as initialization)
            base_speedy = random.randrange(1, 3)  # Reduced from (2,4) to (1,3)
            base_speedx = random.randrange(-1, 2)  # Reduced from (-2,3) to (-1,2)

            # Apply speed factor with lower caps
            self.speedy = min(base_speedy * self.speed_factor, 3.0)  # Reduced cap from 5.0 to 3.0
            self.speedx = max(min(base_speedx * self.speed_factor, 2.0), -2.0)  # Reduced cap from 3.0 to 2.0

            # Ensure bee is visible by forcing a positive speed
            if self.speedy <= 0:
                self.speedy = 1.0

    def hit(self, damage):
        """Handle being hit by a bullet or missile"""
        self.health -= damage
        # Flash the bee white briefly to indicate damage
        original_color = self.color  # Store original color
        self.color = WHITE

        # Store current wing state
        current_wing_state = self.wing_state

        # Create flashed image
        self.base_image = self.create_bee_image()
        self.image = self.base_image

        # Restore original color and wing state
        self.color = original_color
        self.wing_state = current_wing_state

        # Schedule color restoration
        pygame.time.set_timer(pygame.USEREVENT, 100)  # 100ms flash

        # Return True if the bee is destroyed
        return self.health <= 0

    def restore_color(self):
        """Restore the bee's original color after being hit"""
        # Store current wing state
        current_wing_state = self.wing_state

        # Reset color based on level
        if self.level == ENEMY_LEVEL_1:
            self.color = YELLOW
        elif self.level == ENEMY_LEVEL_2:
            self.color = ORANGE
        elif self.level == ENEMY_LEVEL_3:
            self.color = RED
        elif self.level == ENEMY_LEVEL_4:
            self.color = PURPLE

        # Recreate the image with the original color
        self.base_image = self.create_bee_image()
        self.image = self.base_image

        # Restore wing state
        self.wing_state = current_wing_state
