# Retro Bee Shooter

A retro-style arcade game where you control a spaceship and shoot bees, built with Python and Pygame.

![Bee Shooter Game](https://github.com/yourusername/bee-shooter/raw/main/screenshot.png)

## Features

- Full directional movement - control your fighter in all directions
- Four different enemy types with varying difficulty:
  - Level 1: Basic Bee - Low health, slow movement
  - Level 2: Soldier Bee - Medium health, faster movement
  - Level 3: Elite Bee - High health, special movement patterns
  - Level 4: Queen Bee - Very high health, special abilities
- Weapon upgrade system with 5 different weapon levels
- Special weapons:
  - Bomb weapon that clears all enemies from the screen
  - Auto-tracking missiles that follow enemies
- Three types of power-ups: weapon upgrades, bombs, and missiles
- Dynamic power-up drops based on enemy level
- Advanced enemy movement patterns
- Detailed graphics with animations and particle effects
- Sound effects for all game actions

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/bee-shooter.git
   cd bee-shooter
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install pygame numpy scipy
   ```

3. Run the game:
   ```
   python main.py
   ```

## Controls

- **Arrow Keys**: Move spaceship in all directions
- **Spacebar**: Shoot
- **B**: Use bomb weapon (if available)
- **M**: Launch tracking missile (if available)
- **ESC**: Quit game
- **ENTER**: Start game / Restart after game over

## Requirements

- Python 3.x
- Pygame
- NumPy (for sound generation)
- SciPy (for sound generation)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created as a learning project for Python game development
- Inspired by classic arcade shooters
