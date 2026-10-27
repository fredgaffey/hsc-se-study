#!/usr/bin/env python3
"""
Animation Test - Shows frames from all animations.

This script displays all animation frames from the game in a grid.
"""

import pygame
import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, BLACK
from utils.asset_loader import AssetLoader

def main():
    """Initialize and run the animation test."""
    # Initialize pygame
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Animation Frame Test")
    clock = pygame.time.Clock()
    
    # Load assets
    print("Loading assets...")
    asset_loader = AssetLoader()
    
    # Get all animations
    coin_frames = asset_loader.get_coin_frames()
    chest_closed_frames = asset_loader.get_chest_closed_frames()
    chest_open_frames = asset_loader.get_chest_open_frames()
    
    # Create font for labels
    font = pygame.font.Font(None, 24)
    
    # Main loop
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw coin frames
        x, y = 50, 50
        screen.blit(font.render("Coin Animation Frames:", True, (255, 255, 255)), (x, y - 30))
        for i, frame in enumerate(coin_frames):
            screen.blit(frame, (x + i * (TILE_SIZE + 10), y))
            screen.blit(font.render(f"{i+1}", True, (255, 255, 255)), 
                      (x + i * (TILE_SIZE + 10) + TILE_SIZE//2 - 5, y + TILE_SIZE + 5))
        
        # Draw chest closed frames
        y += TILE_SIZE + 60
        screen.blit(font.render("Chest Closed Animation Frames:", True, (255, 255, 255)), (x, y - 30))
        for i, frame in enumerate(chest_closed_frames):
            screen.blit(frame, (x + i * (TILE_SIZE + 10), y))
            screen.blit(font.render(f"{i+1}", True, (255, 255, 255)), 
                      (x + i * (TILE_SIZE + 10) + TILE_SIZE//2 - 5, y + TILE_SIZE + 5))
        
        # Draw chest open frames
        y += TILE_SIZE + 60
        screen.blit(font.render("Chest Open Animation Frames:", True, (255, 255, 255)), (x, y - 30))
        for i, frame in enumerate(chest_open_frames):
            screen.blit(frame, (x + i * (TILE_SIZE + 10), y))
            screen.blit(font.render(f"{i+1}", True, (255, 255, 255)), 
                      (x + i * (TILE_SIZE + 10) + TILE_SIZE//2 - 5, y + TILE_SIZE + 5))
        
        # Instructions
        y = SCREEN_HEIGHT - 50
        screen.blit(font.render("Press ESC to exit", True, (255, 255, 255)), 
                  (SCREEN_WIDTH // 2 - 70, y))
        
        # Update display
        pygame.display.flip()
        clock.tick(30)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()