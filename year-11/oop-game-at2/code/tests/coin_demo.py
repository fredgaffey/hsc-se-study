#!/usr/bin/env python3
"""
Coin Demo - Demonstrates animated coin functionality.

This script creates a simple demo that displays an animated coin using
the coin assets from the assets/world/coin directory.
"""

import pygame
import sys
import os
import time

# Add the project root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from utils.asset_loader import AssetLoader
from objects.coin import Coin

def main():
    """Initialise and run the coin demo."""
    # Initialise pygame
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Coin Animation Demo")
    clock = pygame.time.Clock()
    
    # Load assets
    print("Loading assets...")
    asset_loader = AssetLoader()
    
    # Get coin frames
    coin_frames = asset_loader.get_coin_frames()
    
    # Create multiple coins at different positions
    coins = [
        # Centre coin
        Coin(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, coin_frames),
        # Top-left coin
        Coin(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, coin_frames),
        # Top-right coin 
        Coin(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, coin_frames),
        # Bottom-left coin
        Coin(SCREEN_WIDTH // 4, 3 * SCREEN_HEIGHT // 4, coin_frames),
        # Bottom-right coin
        Coin(3 * SCREEN_WIDTH // 4, 3 * SCREEN_HEIGHT // 4, coin_frames)
    ]
    
    # Set longer lifetime for demo
    for coin in coins:
        coin.lifetime = 1800  # 30 seconds at 60 FPS
    
    # Create a font for displaying information
    font = pygame.font.Font(None, 36)
    
    # Main loop
    running = True
    start_time = time.time()
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Collect the centre coin when space is pressed
                    centre_coin = coins[0]
                    if not centre_coin.collected:
                        value = centre_coin.collect()
                        print(f"Collected coin! Value: {value} gold")
        
        # Update coins
        for coin in coins:
            coin.update()
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw coins
        for coin in coins:
            coin.draw(screen)
        
        # Draw instructions
        text = font.render("Press SPACE to collect the centre coin", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 30))
        
        # Draw elapsed time
        elapsed = time.time() - start_time
        time_text = font.render(f"Elapsed Time: {elapsed:.1f}s", True, (255, 255, 255))
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT - 50))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()