# Bee Shooter Game

A retro-style arcade shooter game where you control an F14 fighter jet to shoot down enemy bees.

## Table of Contents
- [Features](#features)
- [Controls](#controls)
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux/Ubuntu](#linuxubuntu)
- [Game Mechanics](#game-mechanics)
  - [Weapons](#weapons)
  - [Upgrades](#upgrades)
  - [Enemies](#enemies)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Credits](#credits)

## Features

- Fast-paced arcade shooter gameplay
- Multiple weapon systems: bullets, missiles, and bombs
- Weapon and missile upgrades
- Enemy progression with different bee types
- Boss battles at specific score thresholds
- Dynamic background with parallax scrolling
- Realistic sound effects and background music
- F14 fighter jet with detailed graphics

## Controls

- **Arrow Keys**: Move the fighter
- **Space**: Shoot bullets
- **M**: Launch missiles
- **B**: Use bomb (clears all enemies)
- **ESC**: Quit game
- **Enter**: Restart after game over

## Installation

### Requirements

- Python 3.6 or higher
- Pygame

### Windows

1. Make sure you have Python 3.6 or higher installed
2. Clone or download this repository
3. Double-click on `BeeShooter.bat` to start the game

### Linux/Ubuntu

1. Make sure you have Python 3.6 or higher installed
2. Clone or download this repository
3. Make the launcher executable:
   ```
   chmod +x BeeShooter.sh
   ```
4. Run the launcher:
   ```
   ./BeeShooter.sh
   ```

## Game Mechanics

### Weapons

- **Bullets**: Basic weapon, unlimited ammo
- **Missiles**: Homing projectiles that track enemies, limited supply
- **Bombs**: Clear all enemies on screen, very limited supply

### Upgrades

- **Weapon Upgrades**: Increase bullet spread and damage
- **Missile Upgrades**: Increase missile count and damage
- **Pickup Items**: Collect items dropped by enemies for extra missiles, bombs, and upgrades

### Enemies

- **Basic Bee**: Standard enemy with low health
- **Soldier Bee**: Tougher enemy with more health
- **Elite Bee**: Fast-moving enemy with high health
- **Queen Bee**: Boss enemy with very high health, appears at specific score thresholds

## Troubleshooting

If you encounter any issues:

1. Make sure Python 3.6+ is installed and in your PATH
2. Check that Pygame is installed (`pip install pygame`)
3. Look at the `game_debug.log` file for error details
4. If the game crashes on startup, try running it from the command line:
   ```
   python main_new.py
   ```

### Command-Line Options

You can pass additional options to the launcher:

- `--debug`: Enable debug mode
- `--no-sound`: Disable sound
- `--platform [windows|linux]`: Specify platform

Example:
```
BeeShooter.bat --no-sound
```

## Development

This game is built with Python and Pygame. The main components are:

- `main_new.py`: Entry point for the game
- `src/game/game_manager.py`: Main game loop and state management
- `src/entities/`: Game entities (player, enemies, projectiles)
- `src/utils/`: Utility functions and resource management

## Credits

- Game Design & Programming: Reking Shui
- Graphics: Procedurally generated with Pygame
- Sound Effects: Generated with Python wave module

---

Enjoy the game!