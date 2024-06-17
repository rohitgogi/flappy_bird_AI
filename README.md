# Flappy Bird Game with NEAT and Pygame

## Description
This is a Flappy Bird game implementation using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm for artificial intelligence and Pygame for graphics and interaction. The game features pixel-perfect collision detection using masks and a simple genetic algorithm to train the bird to play and eventually beat the game.

## Features
- NEAT algorithm for training the bird
- Pixel-perfect collision detection
- Graphics using Pygame
- Simple genetic algorithm for training
- Adjustable settings through config files

## Installation
1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/your_username/FlappyBird-NEAT.git
   ```
2. Install the required libraries using pip.
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the main script to start the game.
   ```bash
   python flappy_bird.py
   ```
2. The game window will open, and you can see the birds learning to play Flappy Bird.

## Configuration
- `config.txt`: This file contains the configuration parameters for the NEAT algorithm. You can adjust settings such as population size, mutation rates, and more in this file to customize the training process.

## Credits
- Author: Rohit Prakash Gogi (https://github.com/rohit_gogi)