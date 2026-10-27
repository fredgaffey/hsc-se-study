#!/usr/bin/env python3
"""
Game Coin Test - Tests coin spawning within the main game.

This script modifies the game to spawn several coins immediately
for testing purposes.
"""

import pygame
import sys
import os
import random
import math

# Add the project root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from utils.asset_loader import AssetLoader
from core.game import Game
from objects.coin import Coin

class CoinTestGame(Game):
    """Modified game class that spawns additional coins for testing."""
    
    def __init__(self):
        """Initialise the game with extra coins."""
        # Initialise the parent Game class
        super().__init__()
        
        # Spawn additional coins for testing
        self.spawn_test_coins()
        
        # Add a message to the UI
        self.ui.set_message("Coin Test Mode: Collect coins with the player!")
    
    def spawn_test_coins(self):
        """Spawn several coins in different locations for testing."""
        # Clear any existing coins first
        self.coins = []
        
        # Create a pattern of coins
        # Circle pattern
        centre_x, centre_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        radius = 150
        num_coins = 12
        
        for i in range(num_coins):
            angle = 2 * 3.14159 * i / num_coins
            x = centre_x + int(radius * math.cos(angle))
            y = centre_y + int(radius * math.sin(angle))
            
            # Create the coin
            coin = Coin(x, y, self.coin_frames)
            coin.lifetime = 1800  # 30 seconds at 60 FPS
            self.coins.append(coin)
        
        # Add a trail of coins between two random points
        start_x, start_y = random.randint(100, 300), random.randint(100, 300)
        end_x, end_y = random.randint(500, 700), random.randint(400, 500)
        
        num_trail_coins = 10
        for i in range(num_trail_coins):
            t = i / (num_trail_coins - 1)
            x = int(start_x + t * (end_x - start_x))
            y = int(start_y + t * (end_y - start_y))
            
            coin = Coin(x, y, self.coin_frames)
            coin.lifetime = 1800  # 30 seconds at 60 FPS
            self.coins.append(coin)
        
        print(f"Spawned {len(self.coins)} coins for testing")

def main():
    """Run the coin test game."""
    # Create and run the modified game
    game = CoinTestGame()
    game.run()

if __name__ == "__main__":
    main()