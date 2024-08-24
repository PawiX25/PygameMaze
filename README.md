# Maze Game

This is a Python-based maze game created using the Pygame library. The player navigates through a randomly generated maze to reach a goal within a limited time.

## Table of Contents

- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Controls](#game-controls)
- [Features](#features)
- [Game Flow](#game-flow)
- [Dependencies](#dependencies)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/PawiX25/PygameMaze.git
   cd PygameMaze
   ```

2. **Install Pygame:**

   Make sure you have Python installed, then install Pygame using pip:

   ```bash
   pip install pygame
   ```

3. **Run the Game:**

   Execute the `game.py` script to start the game:

   ```bash
   python game.py
   ```

## How to Play

The objective of the game is to navigate the red square (the player) through the maze to reach the green square (the goal) before time runs out. The maze is randomly generated each time you start a new game.

## Game Controls

- **Move:** Arrow keys or `WASD`
- **Pause/Unpause:** `P`
- **Restart:** `R`
- **Quit:** `Q`

## Features

- **Randomly Generated Maze:** Each game presents a new maze.
- **Blinking Goal:** The goal position blinks to make it more noticeable.
- **Timer:** You must reach the goal within the time limit.
- **Game Over Screen:** Displays when you win or lose, offering options to restart or quit.
- **Main Menu:** Start the game, view instructions, or quit.

## Game Flow

1. **Main Menu:** 
   - Press `S` to start the game.
   - Press `I` to view the instructions.
   - Press `Q` to quit.

2. **Instructions:** 
   - The instructions screen provides basic controls and gameplay tips.
   - Press `Q` to return to the main menu.

3. **In-Game:**
   - Navigate through the maze using the arrow keys or `WASD`.
   - The timer counts down from 60 seconds.
   - If you reach the goal within the time limit, a congratulatory message will appear.
   - If time runs out, a game over message is displayed.

4. **Game Over:**
   - After winning or losing, you can restart or quit the game.

## Dependencies

- **Pygame:** This game requires the Pygame library, which can be installed via pip:

  ```bash
  pip install pygame
  ```