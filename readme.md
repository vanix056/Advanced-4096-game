# 4096 Game

An AI-powered implementation of the 4096 puzzle game, where players merge tiles to reach higher values on a 7x7 grid. The game features both player vs AI mode and implements the Minimax algorithm with Alpha-Beta pruning for AI decision-making.

## Features

- **Multiple Game Modes**
  - Player vs AI gameplay
  - Configurable maximum tiles: 1024, 2048, or 4096

- **Advanced AI Implementation**
  - Minimax algorithm with Alpha-Beta pruning
  - Three difficulty levels:
    - Easy: Shallow search depth
    - Medium: Moderate search depth
    - Hard: Deep search with optimized pruning
  - Custom heuristic evaluation considering:
    - Empty cells availability
    - Board smoothness (tile gradient)
    - Maximum tile value

- **Polished User Interface**
  - Built with Pygame
  - Dynamic board visualization
  - Side-by-side player and AI boards
  - Move counters and timers
  - Interactive menu with background images
  - Sound effects and background music

## Game Rules

1. Play takes place on a 7x7 grid
2. Players can slide tiles up, down, left, or right
3. Tiles with identical values merge upon collision, doubling their value
4. Each move spawns a new tile (2 with 90% probability, 4 with 10% probability)
5. Game ends when no valid moves remain

## Requirements

- Python 3.x
- Required libraries:
  - pygame
  - numpy
  - random

## Implementation Details

The AI uses a Minimax algorithm with Alpha-Beta pruning to make decisions. The evaluation function considers multiple factors:
- Number of empty cells
- Board smoothness
- Maximum tile value
- Strategic tile positioning

## Challenges and Solutions

1. **Performance Optimization**
   - Challenge: High computational costs with deep searches
   - Solution: Implemented Alpha-Beta pruning and optimized evaluation functions

2. **Random Element Handling**
   - Challenge: Unpredictable tile spawning
   - Solution: Enhanced scoring to prioritize moves maintaining empty cells

3. **Game End Detection**
   - Challenge: Complex end-game state detection
   - Solution: Implemented comprehensive move validation checks

## Future Improvements

1. Machine learning implementation for adaptive AI strategies
2. Enhanced graphical user interface
3. Alternative algorithm exploration (Monte Carlo Tree Search, ExpectiMinimax)

## Contributors

- Alyan Ahmed Memon (469355)
- Aakash (471368)
- Muhammad Abdullah Waqar (458785)
- Muhammad Shahzil Asif (481491)

## Course Information

- Course: Artificial Intelligence
- Section: BSCS-13B
- Date: December 2024