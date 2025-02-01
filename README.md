# Platformer Game
A simple 2D platformer game built using Pygame. The player controls a character that can jump between platforms, collect coins, and score points. The game features moving platforms, gravity, and collision detection.

## Table of Contents
- Features

- Requirements

- Installation

- How to Play

- Controls

- Code Structure

- Contributing

- License

## Features
<b>Player Movement</b>: Move left and right using arrow keys.

<b>Jumping</b>: Jump onto platforms using the spacebar.

<b>Platforms</b>: Randomly generated static and moving platforms.

<b>Coins</b>: Collect coins to increase your score.

<b>Scrolling</b>: Platforms and coins scroll down as the player moves upward.

<b>Game Over</b>: The game ends if the player falls off the screen.

## Requirements
To run this game, you need the following:

<ul>
Python 3.7 or higher

Pygame library (pip install pygame)
</ul>

## Installation
Clone the repository:

```bash Copy
git clone https://github.com/simichanga/platformer-py.git
cd platformer-py
```
Install dependencies:

```bash Copy
pip install pygame
```
Run the game:

```bash Copy
python main.py
```

## How to Play
The goal is to collect as many coins as possible while avoiding falling off the screen.

Platforms will scroll down as you move upward.

Collect coins to increase your score.

The game ends if the player falls below the screen.

## Controls
<b>Left Arrow</b>: Move left

<b>Right Arrow</b>: Move right

<b>Spacebar</b>: Jump

<b>Esc</b>: Quit the game

## Code Structure
The project is organized as follows:

``` graphql
platformer-game/
├── main.py            # Main game script
├── README.md          # Project documentation
├── player.png         # Player character image
├── platform.png       # Platform image
├── coin.png           # Coin image
└── background.png     # Background image
```

## Key Components
<b>Player Class</b>: Handles player movement, jumping, and collision detection.

<b>Platform Class</b>: Represents platforms, including moving platforms.

<b>Coin Class</b>: Represents coins that the player can collect.

<b>Game Loop</b>: Manages rendering, event handling, and game logic.

## Contributing
Contributions are welcome! If you'd like to contribute:


Fork the repository.

Create a new branch: ```git checkout -b feature/YourFeatureName.```

Commit your changes: ```git commit -m 'Add some feature'.```

Push to the branch: ```git push origin feature/YourFeatureName```.

Open a pull request.


## License
This project is licensed under the MIT License. See the LICENSE file for details.