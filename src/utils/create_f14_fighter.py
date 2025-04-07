"""
Create a realistic F14 Tomcat fighter jet image
"""
import os
import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH = 80
HEIGHT = 60
WHITE = (255, 255, 255)
DARK_GREY = (50, 50, 50)
GREY = (100, 100, 100)
LIGHT_GREY = (150, 150, 150)
NAVY = (0, 0, 100)
BLUE = (30, 30, 150)
LIGHT_BLUE = (100, 100, 200)
RED = (200, 30, 30)
YELLOW = (255, 255, 0)

def create_f14_fighter():
    """Create a realistic F14 Tomcat fighter jet image"""
    # Create surface with alpha channel
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # F14 has variable-sweep wings (can be extended or swept back)
    # We'll draw it with wings in mid-position
    
    # Main fuselage
    fuselage_points = [
        (40, 5),   # Nose
        (45, 10),  # Front right
        (50, 20),  # Mid right
        (45, 40),  # Rear right
        (40, 45),  # Tail
        (35, 40),  # Rear left
        (30, 20),  # Mid left
        (35, 10)   # Front left
    ]
    pygame.draw.polygon(surface, DARK_GREY, fuselage_points)
    
    # Cockpit canopy
    canopy_points = [
        (40, 12),  # Front
        (45, 15),  # Right
        (43, 25),  # Rear right
        (37, 25),  # Rear left
        (35, 15)   # Left
    ]
    pygame.draw.polygon(surface, LIGHT_BLUE, canopy_points)
    pygame.draw.lines(surface, WHITE, False, canopy_points, 1)
    
    # Left wing (variable sweep)
    left_wing_points = [
        (32, 20),  # Inner front
        (10, 25),  # Outer front
        (5, 35),   # Tip
        (15, 38),  # Outer rear
        (30, 30)   # Inner rear
    ]
    pygame.draw.polygon(surface, NAVY, left_wing_points)
    pygame.draw.lines(surface, LIGHT_GREY, False, left_wing_points, 1)
    
    # Right wing (variable sweep)
    right_wing_points = [
        (48, 20),  # Inner front
        (70, 25),  # Outer front
        (75, 35),  # Tip
        (65, 38),  # Outer rear
        (50, 30)   # Inner rear
    ]
    pygame.draw.polygon(surface, NAVY, right_wing_points)
    pygame.draw.lines(surface, LIGHT_GREY, False, right_wing_points, 1)
    
    # Vertical stabilizers (twin tails)
    # Left stabilizer
    left_stab_points = [
        (35, 35),  # Bottom front
        (30, 20),  # Top front
        (25, 20),  # Top rear
        (30, 35)   # Bottom rear
    ]
    pygame.draw.polygon(surface, RED, left_stab_points)
    
    # Right stabilizer
    right_stab_points = [
        (45, 35),  # Bottom front
        (50, 20),  # Top front
        (55, 20),  # Top rear
        (50, 35)   # Bottom rear
    ]
    pygame.draw.polygon(surface, RED, right_stab_points)
    
    # Horizontal stabilizers
    # Left stabilizer
    pygame.draw.polygon(surface, NAVY, [
        (30, 35),  # Inner
        (20, 40),  # Outer
        (25, 42),  # Rear
        (35, 38)   # Inner rear
    ])
    
    # Right stabilizer
    pygame.draw.polygon(surface, NAVY, [
        (50, 35),  # Inner
        (60, 40),  # Outer
        (55, 42),  # Rear
        (45, 38)   # Inner rear
    ])
    
    # Engine intakes
    pygame.draw.ellipse(surface, DARK_GREY, (30, 25, 8, 5))  # Left intake
    pygame.draw.ellipse(surface, DARK_GREY, (42, 25, 8, 5))  # Right intake
    
    # Engine exhausts
    pygame.draw.ellipse(surface, GREY, (35, 43, 5, 3))  # Left exhaust
    pygame.draw.ellipse(surface, GREY, (40, 43, 5, 3))  # Right exhaust
    pygame.draw.ellipse(surface, YELLOW, (36, 44, 3, 1))  # Left afterburner
    pygame.draw.ellipse(surface, YELLOW, (41, 44, 3, 1))  # Right afterburner
    
    # Cockpit details - pilot
    pygame.draw.circle(surface, DARK_GREY, (40, 18), 2)  # Pilot's helmet
    
    # Nose cone
    pygame.draw.ellipse(surface, LIGHT_GREY, (38, 5, 4, 5))
    
    # Weapons/missiles under wings
    pygame.draw.rect(surface, GREY, (15, 30, 10, 2))  # Left wing missile
    pygame.draw.rect(surface, GREY, (55, 30, 10, 2))  # Right wing missile
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.join("assets", "images"), exist_ok=True)
    
    # Save the image
    pygame.image.save(surface, os.path.join("assets", "images", "f14_fighter.png"))
    print(f"F14 fighter image saved to {os.path.join('assets', 'images', 'f14_fighter.png')}")
    
    return surface

if __name__ == "__main__":
    create_f14_fighter()
    pygame.quit()
