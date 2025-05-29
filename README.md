# HIT137 Software Now Assignment 3

This repository contains two main projects:

- **Game Project**: A simple arcade-style space shooter game.
- **Image Editor (Tkinter GUI)**: A basic image editor built with Tkinter for simple image manipulations.

---

## 1. Game Project

**Location:** `game_project/`

### Description
A classic 2D space shooter game where the player controls a spaceship, dodges enemy ships, and shoots lasers. The game features:
- Player and enemy ships
- Multiple laser types
- Background graphics

### How to Run
1. Ensure you have Python 3 installed.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python game_project/main.py
   ```

### Assets
All game images are located in `game_project/image/`.

---

## 2. Image Editor (Tkinter GUI)

**Location:** `tkinter-gui/`

### Description
A simple image editor with a graphical user interface built using Tkinter. Features include:
- Loading and displaying images
- Basic image modifications (e.g., grayscale, rotate, resize)
- Saving modified images

### How to Run
1. Ensure you have Python 3 installed.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the editor:
   ```bash
   python tkinter-gui/main.py
   ```

### Resources
Sample images are provided in `tkinter-gui/resources/`.

---

## Requirements
- Python 3.x
- See `requirements.txt` for required Python packages.

---

## Project Structure
```
README.md
requirements.txt
game_project/
    main.py
    image/
        ...game images...
tkinter-gui/
    __init__.py
    ImageEditor.py
    main.py
    resources/
        ...sample images...
```
