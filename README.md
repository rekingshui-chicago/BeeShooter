# Retro Bee Shooter Game

A simple retro-style game where you control a spaceship and shoot bees.

## How to Play

1. Use the arrow keys (UP, DOWN, LEFT, RIGHT) to move your spaceship in all directions
2. Press SPACEBAR to shoot
3. Press B to use a bomb (clears all enemies from the screen)
4. Press M to launch a missile (auto-tracks and follows enemies)
5. Collect power-ups to upgrade your weapons, bombs, and missiles
6. Avoid getting hit by the bees
7. Score points by shooting bees - higher level bees are worth more points!

## Controls

- UP/DOWN/LEFT/RIGHT arrows: Move spaceship in all directions
- SPACEBAR: Shoot
- B: Use bomb weapon (if available)
- M: Launch tracking missile (if available)
- ESC: Quit game
- ENTER: Start game / Restart after game over

## Requirements

- Python 3.x
- Pygame

## Running the Game

### Using the run script (recommended)

```bash
./run_game.sh
```

### Manual method

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the game
python main.py

# Deactivate when done
deactivate
```

## Game Features

- Full directional movement - control your fighter in all directions
- Four different enemy types with varying difficulty:
  - Level 1: Basic Bee - Low health, slow movement
  - Level 2: Soldier Bee - Medium health, faster movement
  - Level 3: Elite Bee - High health, special movement patterns
  - Level 4: Queen Bee - Very high health, special abilities
- Weapon upgrade system with 5 different weapon levels
- Bomb weapon that clears all enemies from the screen
- Auto-tracking missiles that follow enemies
  - Missiles fire automatically when shooting (20% chance)
  - Can still be fired manually with the M key
  - Missile upgrade system with 4 levels:
    - Level 1: Single missile with basic damage
    - Level 2: Dual missiles with increased damage
    - Level 3: Triple missiles with high damage
    - Level 4: Quad missiles with maximum damage
- Three types of power-ups: weapon upgrades, bombs, and missiles
- Dynamic power-up drops based on enemy level:
  - Higher level enemies drop more valuable power-ups
  - Different enemies have different drop rates and preferences
  - Different weapons have different chances of generating power-ups
- Advanced enemy movement patterns for higher-level enemies
- Detailed graphics with animations and particle effects
- Sound effects for all game actions

- Simple retro-style graphics
- Increasing difficulty as you play
- Score tracking
- Game over screen with restart option

Enjoy the game!
