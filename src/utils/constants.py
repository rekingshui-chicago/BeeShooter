"""
Game constants
"""
import pygame
from pygame.locals import K_b

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
GREY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 40)

# Key constants
B_KEY = K_b  # Use pygame's lowercase b key code
B_KEY_UPPER = ord('B')  # Uppercase B key ASCII code

# Enemy levels
ENEMY_LEVEL_1 = 1
ENEMY_LEVEL_2 = 2
ENEMY_LEVEL_3 = 3
ENEMY_LEVEL_4 = 4

# Weapon levels
WEAPON_LEVEL_1 = 1
WEAPON_LEVEL_2 = 2
WEAPON_LEVEL_3 = 3
WEAPON_LEVEL_4 = 4
WEAPON_LEVEL_5 = 5

# Missile levels
MISSILE_LEVEL_1 = 1
MISSILE_LEVEL_2 = 2
MISSILE_LEVEL_3 = 3
MISSILE_LEVEL_4 = 4

# Level thresholds
LEVEL_THRESHOLDS = [10000, 20000, 50000]
