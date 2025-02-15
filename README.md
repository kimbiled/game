# Space Halo - Arcade Shooter Game

## Overview
**Space Halo** is a fast-paced arcade shooter built with **Python and Pygame**. The player controls a spaceship, moves around the screen, shoots enemies, and collects bonuses. The game includes various enemy behaviors and power-ups that enhance the gameplay.

## Features
- **Player movement:** Navigate using `WASD` or arrow keys.
- **Shooting mechanics:** Press `SPACE` to fire bullets.
- **Enemies:** Randomly generated enemies with movement patterns.
- **Enemy shooting:** Enemies fire bullets at the player.
- **Bonuses:** Destroy special blocks to gain extra lives, double points, or faster shooting.
- **Score tracking:** Earn points by destroying enemies.
- **Lives system:** Player starts with 3 lives and loses when they reach 0.
- **Main Menu & Game Over screen:** Press `Enter` to start and `R` to restart after losing.

## Controls
- **Move:** `WASD` or `Arrow Keys`
- **Shoot:** `Space`
- **Exit Game:** `Esc`
- **Start Game:** `Enter` (from menu)
- **Restart:** `R` (from Game Over screen)

## Installation & Setup
1. Install Python (if not already installed)
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Game Mechanics
### Player
- Moves around the screen
- Fires bullets upwards
- Has 3 lives initially

### Enemies
- Move in random patterns
- Fire bullets at intervals
- If they reach the bottom, player loses a life

### Bonuses
- Appear randomly
- Collect by shooting them
- Effects:
  - `extra_life`: +1 life
  - `double_points`: Doubles score for 10 seconds
  - `fast_shooting`: Reduces bullet cooldown for 5 seconds

## Future Improvements
- Add more enemy types
- Implement wave-based levels
- Add sound effects and music
- Improve animations and UI

## Contributors
- **Your Name** - Developer

## License
This project is open-source and available under the MIT License.

