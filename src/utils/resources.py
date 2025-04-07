"""
Resource loading utilities
"""
import os
import pygame
import random
import math
import logging
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE,
    PURPLE, CYAN, PINK, GREY, LIGHT_BLUE, DARK_BLUE
)

logger = logging.getLogger('bee_shooter.resources')

# Dictionary to store loaded sounds
sounds = {}

def load_image(name, colorkey=None):
    """Load an image, handling file not found and creating default images"""
    logger.debug("Loading image: %s", name)

    # If file doesn't exist, generate images
    if name == "background":
        # Create a seamless tileable background that's larger than the screen
        # Using 3x screen size to ensure smooth scrolling without visible seams
        bg_width = SCREEN_WIDTH * 3
        bg_height = SCREEN_HEIGHT * 3
        surf = pygame.Surface((bg_width, bg_height))

        # Create a dark space gradient from dark blue to black
        # Make the gradient repeat seamlessly by using a sine wave pattern
        for y in range(bg_height):
            # Calculate gradient color using sine wave for seamless tiling
            # This creates a subtle wave pattern that repeats smoothly
            gradient_factor = (math.sin(y * 0.01) + 1) / 2  # Oscillates between 0 and 1
            color_value = int(15 + 10 * gradient_factor)  # Range from 15 to 25
            color = (color_value // 3, color_value // 3, color_value)
            pygame.draw.line(surf, color, (0, y), (bg_width, y))

        # Create a star pattern that will tile seamlessly
        # We'll create a base star pattern and then repeat it with slight variations

        # Create base star pattern in a separate surface
        star_pattern_size = SCREEN_WIDTH
        star_pattern = pygame.Surface((star_pattern_size, star_pattern_size), pygame.SRCALPHA)

        # Add distant stars (small, various brightness)
        for _ in range(300):
            x = random.randrange(0, star_pattern_size)
            y = random.randrange(0, star_pattern_size)
            brightness = random.randrange(100, 256)
            radius = random.randrange(1, 3) / 2  # Smaller stars
            color = (brightness, brightness, brightness)
            pygame.draw.circle(star_pattern, color, (x, y), radius)

        # Add medium stars (slightly larger, with glow)
        for _ in range(50):
            x = random.randrange(0, star_pattern_size)
            y = random.randrange(0, star_pattern_size)
            brightness = random.randrange(180, 256)
            radius = random.randrange(1, 3)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(star_pattern, color, (x, y), radius)

            # Add subtle glow
            glow_radius = radius + 1
            glow_color = (brightness // 4, brightness // 4, brightness // 3)
            pygame.draw.circle(star_pattern, glow_color, (x, y), glow_radius, 1)

        # Add a few bright stars with lens flare
        for _ in range(10):
            x = random.randrange(0, star_pattern_size)
            y = random.randrange(0, star_pattern_size)
            pygame.draw.circle(star_pattern, WHITE, (x, y), 2)

            # Add cross-shaped lens flare
            flare_length = random.randrange(4, 8)
            pygame.draw.line(star_pattern, (100, 100, 150), (x - flare_length, y), (x + flare_length, y))
            pygame.draw.line(star_pattern, (100, 100, 150), (x, y - flare_length), (x, y + flare_length))

        # Make the edges of the star pattern fade out for seamless tiling
        # Create a mask that's fully transparent at the edges and fully opaque in the center
        edge_fade = pygame.Surface((star_pattern_size, star_pattern_size), pygame.SRCALPHA)
        center = star_pattern_size // 2
        max_dist = center * 0.9  # Fade starts at 90% of the distance to the edge

        for x in range(star_pattern_size):
            for y in range(star_pattern_size):
                # Calculate distance from center (normalized to 0-1)
                dx, dy = x - center, y - center
                dist = math.sqrt(dx*dx + dy*dy) / center

                # Calculate alpha (fully opaque in center, transparent at edges)
                if dist > max_dist:
                    # Smooth fade from max_dist to 1.0
                    fade_factor = 1.0 - (dist - max_dist) / (1.0 - max_dist)
                    alpha = int(255 * fade_factor)
                else:
                    alpha = 255

                edge_fade.set_at((x, y), (255, 255, 255, alpha))

        # Apply the fade mask to the star pattern
        star_pattern.blit(edge_fade, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Tile the star pattern across the background with slight variations
        for i in range(0, bg_width, star_pattern_size):
            for j in range(0, bg_height, star_pattern_size):
                # Add some variation to each tile to make it less obvious
                variation = pygame.Surface((star_pattern_size, star_pattern_size), pygame.SRCALPHA)
                variation.blit(star_pattern, (0, 0))

                # Randomly flip or rotate some tiles for more variation
                if random.random() > 0.5:
                    variation = pygame.transform.flip(variation, True, False)
                if random.random() > 0.5:
                    variation = pygame.transform.flip(variation, False, True)

                surf.blit(variation, (i, j))

        # Add larger nebulae that span across tile boundaries
        for _ in range(10):  # More nebulae for a richer background
            x = random.randrange(0, bg_width)
            y = random.randrange(0, bg_height)
            size = random.randrange(100, 300)  # Larger nebulae

            # Create a nebula surface with transparency
            nebula = pygame.Surface((size, size), pygame.SRCALPHA)

            # Choose a random color for the nebula with emphasis on red colors
            nebula_colors = [
                (80, 30, 70, 3),   # Purple
                (70, 30, 80, 3),   # Blue-purple
                (30, 50, 80, 3),   # Blue
                (120, 30, 30, 3),   # Red
                (150, 40, 30, 3),   # Bright red
                (100, 30, 20, 3),   # Dark red
                (130, 50, 30, 3),   # Red-orange
                (140, 30, 40, 3)    # Red-purple
            ]
            # Increase probability of red nebulae (last 5 colors are reddish)
            weights = [1, 1, 1, 3, 3, 3, 3, 3]  # Higher weights for red colors
            nebula_color = random.choices(nebula_colors, weights=weights, k=1)[0]

            # Draw the nebula as a series of transparent circles with gaussian distribution
            center_x, center_y = size // 2, size // 2
            for _ in range(100):  # More circles for denser nebulae
                # Use gaussian distribution to concentrate circles near the center
                nx = int(random.gauss(center_x, size / 6))
                ny = int(random.gauss(center_y, size / 6))

                # Skip if outside the surface
                if nx < 0 or nx >= size or ny < 0 or ny >= size:
                    continue

                # Size also follows gaussian distribution - larger near center
                dist_from_center = math.sqrt((nx - center_x)**2 + (ny - center_y)**2)
                max_radius = max(6, size // 4 * (1 - dist_from_center / (size / 2)))  # Ensure at least 6 for valid range
                nr = random.randrange(5, int(max_radius))

                pygame.draw.circle(nebula, nebula_color, (nx, ny), nr)

            # Apply a radial fade to the nebula for smooth edges
            for x in range(size):
                for y in range(size):
                    # Calculate distance from center (normalized to 0-1)
                    dx, dy = x - center_x, y - center_y
                    dist = math.sqrt(dx*dx + dy*dy) / (size / 2)

                    # Apply fade if near the edge
                    if dist > 0.7:  # Start fading at 70% from center
                        # Get current color
                        r, g, b, a = nebula.get_at((x, y))

                        # Calculate new alpha (fade to transparent at the edge)
                        fade_factor = max(0, 1.0 - (dist - 0.7) / 0.3)
                        new_alpha = int(a * fade_factor)

                        # Set new color with adjusted alpha
                        nebula.set_at((x, y), (r, g, b, new_alpha))

            # Blit the nebula onto the background
            surf.blit(nebula, (x - size // 2, y - size // 2))

    elif name == "player":
        # Try to use the F14 fighter image
        fighter_path = os.path.join('assets', 'images', 'f14_fighter.png')
        if os.path.exists(fighter_path):
            try:
                surf = pygame.image.load(fighter_path).convert_alpha()
                # No need to scale as it's already the right size (80x60)
                return surf
            except pygame.error:
                logger.error("Error loading F14 fighter image, falling back to realistic_fighter.png")

                # Try to use the realistic_fighter.png as fallback
                fighter_path = os.path.join('assets', 'images', 'realistic_fighter.png')
                if os.path.exists(fighter_path):
                    try:
                        surf = pygame.image.load(fighter_path).convert_alpha()
                        # No need to scale as it's already the right size (80x60)
                        return surf
                    except pygame.error:
                        logger.error("Error loading realistic fighter image, falling back to generated image")

        # Fallback to generated image if file loading fails
        surf = pygame.Surface((80, 60), pygame.SRCALPHA)

        # Main body of the ship - sleek fuselage
        ship_color = BLUE

        # Draw the main fuselage (more aerodynamic)
        points = [
            (40, 5),   # Nose
            (60, 25),  # Right side
            (55, 40),  # Right back
            (40, 45),  # Tail
            (25, 40),  # Left back
            (20, 25)   # Left side
        ]
        pygame.draw.polygon(surf, ship_color, points)

        # Add metallic highlights
        highlight_points = [
            (40, 8),   # Nose
            (55, 25),  # Right side
            (52, 37),  # Right back
            (40, 42),  # Tail
        ]
        pygame.draw.polygon(surf, LIGHT_BLUE, highlight_points)

        # Add cockpit (more realistic with canopy)
        cockpit_points = [
            (40, 15),  # Front
            (48, 22),  # Right
            (40, 30),  # Back
            (32, 22)   # Left
        ]
        pygame.draw.polygon(surf, LIGHT_BLUE, cockpit_points)

        # Add wings (more detailed)
        # Left wing
        left_wing_points = [
            (25, 30),  # Inner front
            (5, 35),   # Outer front
            (10, 45),  # Outer back
            (30, 40)   # Inner back
        ]
        pygame.draw.polygon(surf, RED, left_wing_points)

        # Right wing
        right_wing_points = [
            (55, 30),  # Inner front
            (75, 35),  # Outer front
            (70, 45),  # Outer back
            (50, 40)   # Inner back
        ]
        pygame.draw.polygon(surf, RED, right_wing_points)

    elif name == "bullet":
        surf = pygame.Surface((5, 10))
        surf.fill(BLACK)
        pygame.draw.rect(surf, YELLOW, (0, 0, 5, 10))
        pygame.draw.rect(surf, WHITE, (2, 0, 1, 10))

    elif name == "missile":
        surf = pygame.Surface((10, 20))
        surf.fill(BLACK)
        # Missile body
        pygame.draw.rect(surf, GREY, (3, 0, 4, 15))
        # Missile head
        pygame.draw.polygon(surf, RED, [(3, 0), (7, 0), (5, -5)])
        # Missile fins
        pygame.draw.polygon(surf, GREY, [(3, 15), (0, 20), (3, 15)])
        pygame.draw.polygon(surf, GREY, [(7, 15), (10, 20), (7, 15)])
        # Missile engine
        pygame.draw.rect(surf, ORANGE, (4, 15, 2, 5))

    elif name == "explosion":
        surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Create a simple explosion animation frame
        pygame.draw.circle(surf, ORANGE, (15, 15), 15)
        pygame.draw.circle(surf, YELLOW, (15, 15), 10)
        pygame.draw.circle(surf, WHITE, (15, 15), 5)

    else:
        # Default: create a simple colored square
        surf = pygame.Surface((50, 50))
        surf.fill(RED)

    # Apply colorkey if specified
    if colorkey is not None:
        if colorkey == -1:
            colorkey = surf.get_at((0, 0))
        surf.set_colorkey(colorkey, pygame.RLEACCEL)

    return surf

def setup_sound_system(args):
    """Initialize the sound system based on platform and arguments"""
    global sounds

    # Determine if sound should be enabled
    sound_enabled = not args.no_sound

    if sound_enabled:
        try:
            # Initialize mixer with high quality settings
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            logger.info("Sound system initialized with high quality settings")

            # Load sound files
            sound_files = {
                'shoot': 'shoot.wav',
                'explosion': 'explosion.wav',
                'game_over': 'game_over.wav',
                'powerup': 'powerup.wav',
                'bomb': 'bomb.wav',
                'missile': 'missile.wav',
                'background_music': 'background_music.wav'
            }

            # Set volume levels for different sound types
            volume_levels = {
                'shoot': 0.4,      # Lower volume for frequent sounds
                'explosion': 0.7,  # Higher volume for impact
                'game_over': 0.8,  # Important notification
                'powerup': 0.6,    # Medium volume
                'bomb': 0.9,       # Dramatic effect
                'missile': 0.5,    # Medium volume
                'background_music': 0.3  # Background music (quieter)
            }

            for name, filename in sound_files.items():
                sound_path = os.path.join('assets', 'sounds', filename)
                if os.path.exists(sound_path):
                    try:
                        sounds[name] = pygame.mixer.Sound(sound_path)
                        # Set appropriate volume
                        sounds[name].set_volume(volume_levels.get(name, 0.7))
                        logger.debug("Loaded sound: %s at volume %.1f", sound_path, volume_levels.get(name, 0.7))
                    except pygame.error as e:
                        logger.warning("Failed to load sound: %s - %s", sound_path, str(e))
                        sounds[name] = DummySound()
                else:
                    logger.warning("Sound file not found: %s", sound_path)
                    sounds[name] = DummySound()

        except Exception as e:
            logger.error("Failed to initialize sound system: %s", str(e))
            sound_enabled = False

    # If sound is disabled, create dummy sounds
    if not sound_enabled:
        logger.info("Sound disabled, using dummy sound system")
        for sound_name in ['shoot', 'explosion', 'game_over', 'powerup', 'bomb', 'missile', 'background_music']:
            sounds[sound_name] = DummySound()

    return sounds, sound_enabled

class DummySound:
    """Dummy sound class for when sound is disabled"""
    def __init__(self, buffer=None):
        self._volume = 0.0
        self._length = 1.0  # 1 second dummy length
        self._num_channels = 0
        logger.debug("Created DummySound instance")

    def play(self, loops=0, maxtime=0, fade_ms=0):
        logger.debug("DummySound.play called")
        return DummyChannel()

    def stop(self):
        logger.debug("DummySound.stop called")

    def fadeout(self, time):
        logger.debug("DummySound.fadeout called")

    def set_volume(self, value):
        logger.debug("DummySound.set_volume called with %f", value)
        self._volume = value

    def get_volume(self):
        logger.debug("DummySound.get_volume called, returning %f", self._volume)
        return self._volume

    def get_num_channels(self):
        logger.debug("DummySound.get_num_channels called, returning %d", self._num_channels)
        return self._num_channels

    def get_length(self):
        logger.debug("DummySound.get_length called, returning %f", self._length)
        return self._length

class DummyChannel:
    """Dummy channel class for when sound is disabled"""
    def __init__(self):
        self._sound = None
        logger.debug("Created DummyChannel instance")

    def play(self, sound=None, loops=0, maxtime=0, fade_ms=0):
        logger.debug("DummyChannel.play called")
        self._sound = sound
        return self

    def stop(self):
        logger.debug("DummyChannel.stop called")

    def pause(self):
        logger.debug("DummyChannel.pause called")

    def unpause(self):
        logger.debug("DummyChannel.unpause called")

    def fadeout(self, time):
        logger.debug("DummyChannel.fadeout called")

    def set_volume(self, left, right=None):
        logger.debug("DummyChannel.set_volume called")

    def get_busy(self):
        logger.debug("DummyChannel.get_busy called, returning False")
        return False

    def get_sound(self):
        logger.debug("DummyChannel.get_sound called, returning None")
        return self._sound

    def queue(self, sound):
        logger.debug("DummyChannel.queue called")
        pass
