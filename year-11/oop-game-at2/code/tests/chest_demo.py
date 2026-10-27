#!/usr/bin/env python3
"""
Chest Demo - Demonstrates animated chest functionality.

This script creates a simple demo that displays animated chests using
the chest assets from the assets/world/chest directory.
"""

import pygame
import sys
import os
import time

# Add the project root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, TILE_SIZE
from utils.asset_loader import AssetLoader
from objects.chest import Chest

def main():
    """Initialise and run the chest demo."""
    # Initialise pygame
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chest Animation Demo")
    clock = pygame.time.Clock()
    
    # Load assets
    print("Loading assets...")
    asset_loader = AssetLoader()
    
    # Get chest frames
    chest_closed_frames = asset_loader.get_chest_closed_frames()
    chest_open_frames = asset_loader.get_chest_open_frames()
    
    # Create chests at different positions
    chests = [
        # Centre chest - this one can be opened
        Chest(SCREEN_WIDTH // 2 - TILE_SIZE // 2, SCREEN_HEIGHT // 2 - TILE_SIZE // 2, 
             chest_closed_frames, chest_open_frames),
        
        # Four corner chests
        Chest(100, 100, chest_closed_frames, chest_open_frames),
        Chest(SCREEN_WIDTH - 100 - TILE_SIZE, 100, chest_closed_frames, chest_open_frames),
        Chest(100, SCREEN_HEIGHT - 100 - TILE_SIZE, chest_closed_frames, chest_open_frames),
        Chest(SCREEN_WIDTH - 100 - TILE_SIZE, SCREEN_HEIGHT - 100 - TILE_SIZE, 
             chest_closed_frames, chest_open_frames)
    ]
    
    # Create font for displaying information
    font = pygame.font.Font(None, 36)
    
    # Main loop
    running = True
    message = "Press SPACE to open the centre chest"
    message_timer = 0
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Open the centre chest when space is pressed
                    chest_contents = chests[0].open()
                    if chest_contents:
                        message = f"Found {chest_contents['gold']} gold"
                        if chest_contents['health_potion']:
                            message += " and a health potion!"
                        else:
                            message += "!"
                        message_timer = 3  # Display for 3 seconds
        
        # Update chests
        for chest in chests:
            chest.update()
        
        # Update message timer
        if message_timer > 0:
            message_timer -= 1/FPS
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw chests
        for chest in chests:
            chest.draw(screen)
        
        # Draw instructions
        text = font.render("Press SPACE to open the centre chest", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 30))
        
        # Draw message if active
        if message_timer > 0:
            msg_text = font.render(message, True, (255, 215, 0))  # Gold color text
            screen.blit(msg_text, (SCREEN_WIDTH // 2 - msg_text.get_width() // 2, SCREEN_HEIGHT - 60))
        
        # Display status
        if chests[0].is_open:
            status = "Chest is open!"
        else:
            status = "Chest is closed"
        status_text = font.render(status, True, (255, 255, 255))
        screen.blit(status_text, (SCREEN_WIDTH // 2 - status_text.get_width() // 2, SCREEN_HEIGHT - 100))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()