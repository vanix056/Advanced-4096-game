# Advanced 4096 Game

## Overview

Advanced 4096 is a feature-rich desktop reimagining of the classic 2048 sliding-tile puzzle, built with Python and Pygame. It expands the original concept to a **7×7 grid** and introduces a competitive **AI vs. Player** split-screen mode, where a Minimax-powered AI opponent plays in real time alongside the human player. Three selectable target tiles (1024, 2048, 4096) and three AI difficulty levels make every session uniquely challenging. A weighted scoring system — factoring in move count and elapsed time — determines the final winner objectively.

## Key Features

- **7×7 Grid** — significantly larger than the classic 4×4, raising strategic depth and replayability
- **AI vs. Player Split-Screen** — both grids are rendered side-by-side; AI and player compete simultaneously
- **Minimax AI with Alpha-Beta Pruning** — heuristic board evaluation considers maximum tile, empty cells, and grid smoothness
- **Three Difficulty Levels** — Easy, Medium, and Hard adjust AI search depth and move delay
- **Three Game Modes** — choose a target tile of 1024, 2048, or 4096
- **Weighted Winner Calculation** — final result scored by a 70/30 weighting of moves vs. time
- **Sound Design** — background music loop and tile-merge sound effects
- **Animated Menu** — full-screen background image, styled buttons, and a splash-screen intro

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3 |
| Game Framework | Pygame |
| Numerical Computing | NumPy |
| Standard Library | `random` |
| Assets | MP3 audio, JPEG/PNG images |

## Installation

### Prerequisites

- Python 3.8 or later
- `pip`

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/vanix056/Advanced-4096-game.git
cd Advanced-4096-game

# 2. Install dependencies
pip install pygame numpy

# 3. Run the game
python Main.py
```

> All asset files (`background music.mp3`, `move.mp3`, `backpic.jpg`, `4096icon.png`) must remain in the same directory as `Main.py`.

## Usage

1. Launch the game with `python Main.py`.
2. A splash screen is displayed for 5 seconds while the background music starts.
3. On the main menu:
   - Select a **game mode**: Play 1024, Play 2048, or Play 4096.
   - Select an **AI difficulty**: Easy, Medium, or Hard.
4. Once both selections are made, the game starts automatically.
5. **Player controls** (right-side grid):

   | Key | Action |
   |---|---|
   | `↑` Arrow | Slide tiles up |
   | `↓` Arrow | Slide tiles down |
   | `←` Arrow | Slide tiles left |
   | `→` Arrow | Slide tiles right |

6. The AI plays on the left grid autonomously.
7. The game ends when both sides either reach the target tile or run out of moves. A result message displaying move counts, time, and weighted scores is shown for 5 seconds.

## Project Structure

```
Advanced-4096-game/
├── Main.py                 # Game logic, AI engine, and Pygame rendering
├── backpic.jpg             # Menu background image
├── 4096icon.png            # Splash screen image
├── background music.mp3    # Looping background track
├── move.mp3                # Tile-merge sound effect
└── README.md
```

## Configuration

All tunable constants are defined at the top of `Main.py`:

| Constant | Default | Description |
|---|---|---|
| `WIDTH`, `HEIGHT` | `900 × 540` | Window resolution in pixels |
| `GRID_SIZE` | `7` | Board dimensions (N × N) |
| `TILE_SIZE` | `55` | Pixel size of each tile |
| `MARGIN` | `10` | Gap between tiles |
| `TILE_COLORS` | dict | Color map for each tile value |

AI search depth per difficulty is set in `start_game()`:

| Difficulty | Search Depth | Move Delay |
|---|---|---|
| Easy | 1 | 500 ms |
| Medium | 2 | 300 ms |
| Hard | 3 | 0 ms |

## UI Features

- **Splash Screen** — displays `4096icon.png` for 5 seconds on launch
- **Main Menu** — rounded-corner buttons for mode and difficulty selection; selected option highlighted
- **Split-Screen Gameplay** — AI grid (left) and player grid (right) separated by a vertical divider
- **HUD** — live timer (MM:SS) and move counter displayed below each grid
- **End Screen** — winner announcement with weighted scores rendered on-screen for 5 seconds

## AI Architecture

The AI uses the **Minimax algorithm with Alpha-Beta Pruning** to select the optimal move each turn.

**Board evaluation heuristic:**

```
score = 10 × max_tile + 2 × empty_cells + smoothness
```

- `max_tile` — rewards reaching high tile values
- `empty_cells` — rewards keeping the board open
- `smoothness` — penalizes large value differences between adjacent tiles (encourages ordered stacking)

The search explores all four directions recursively to the configured depth, pruning branches that cannot improve the best-known outcome.

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository and create a feature branch.
2. Keep changes focused; one feature or fix per pull request.
3. Ensure the game runs without errors before submitting.
4. Open a pull request with a clear description of the change and its motivation.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Authors

| Name | Student ID |
|---|---|
| M. Abdullah Waqar | 458785 |
| Aakash | 471368 |
| Alyan Ahmed Memon | 469355 |
| M. Shahzil Asif | 481491 |
