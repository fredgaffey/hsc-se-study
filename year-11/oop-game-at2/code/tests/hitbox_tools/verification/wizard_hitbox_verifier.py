#!/usr/bin/env python3
"""
Wizard Hitbox Verifier

This module provides a simple visualization tool to verify the wizard's
hitbox position and size relative to the sprite.
"""

import os
import sys
import pygame
import time

# Add the project root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Import game modules
from utils.asset_loader import AssetLoader
from characters.wizard import Wizard
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class HitboxVerifier:
    """Tool for verifying the wizard's hitbox configuration."""
    
    def __init__(self):
        """Initialize the hitbox verification tool."""
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wizard Hitbox Verifier")
        self.clock = pygame.time.Clock()
        
        # Set up font
        self.font = pygame.font.Font(None, 24)
        
        # Create asset loader
        self.asset_loader = AssetLoader()
        
        # Get wizard frames
        self.wizard_idle_frames = self.asset_loader.get_player_idle_frames("wizard")
        self.wizard_attack_frames = self.asset_loader.get_player_attack_frames("wizard")
        
        # Position wizard at center of screen
        wizard_x = SCREEN_WIDTH // 2 - 50
        wizard_y = SCREEN_HEIGHT // 2 - 62
        
        # Create wizard
        self.wizard = Wizard(wizard_x, wizard_y, 
                          self.wizard_idle_frames, self.wizard_attack_frames)
        
        # Store original position
        self.original_x = self.wizard.x
        self.original_y = self.wizard.y
        
        # Create a simple map class for wizard updates
        class SimpleMap:
            def is_wall(self, x, y):
                return False
        
        self.game_map = SimpleMap()
        
        # Display settings
        self.show_debug = True
        self.show_help = True
    
    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    # Toggle animation
                    if self.wizard.state == "idle":
                        self.wizard.state = "attack"
                        self.wizard.attacking = True
                        self.wizard.attack_start_time = time.time()
                    else:
                        self.wizard.state = "idle"
                        self.wizard.attacking = False
                        self.wizard.current_frame = 0
                elif event.key == pygame.K_d:
                    # Toggle debug info
                    self.show_debug = not self.show_debug
                elif event.key == pygame.K_h:
                    # Toggle help text
                    self.show_help = not self.show_help
                elif event.key == pygame.K_F1:
                    # Take screenshot
                    pygame.image.save(self.screen, "wizard_hitbox_verification.png")
                    print("Screenshot saved as wizard_hitbox_verification.png")
        
        return True
    
    def update(self):
        """Update the wizard state."""
        # Force wizard to stay at original position
        self.wizard.x = self.original_x
        self.wizard.y = self.original_y
        
        # Update wizard for animation
        self.wizard.update(self.game_map)
        
        # Ensure wizard position remains fixed
        self.wizard.x = self.original_x
        self.wizard.y = self.original_y
    
    def draw(self):
        """Draw the current state to the screen."""
        # Clear the screen
        self.screen.fill((30, 30, 40))
        
        # Draw grid
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, (50, 50, 60), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (50, 50, 60), (0, y), (SCREEN_WIDTH, y))
        
        # Draw the wizard
        self.wizard.draw(self.screen)
        
        if self.show_debug:
            # Draw sprite boundaries (blue box)
            sprite_rect = pygame.Rect(self.wizard.x, self.wizard.y, 100, 125)
            pygame.draw.rect(self.screen, (0, 0, 255), sprite_rect, 1)
            
            # Draw center lines for sprite
            sprite_center_x = self.wizard.x + 50
            sprite_center_y = self.wizard.y + 62
            pygame.draw.line(self.screen, (0, 0, 255), 
                           (sprite_center_x, self.wizard.y), 
                           (sprite_center_x, self.wizard.y + 125), 1)
            pygame.draw.line(self.screen, (0, 0, 255), 
                           (self.wizard.x, sprite_center_y), 
                           (self.wizard.x + 100, sprite_center_y), 1)
            
            # Draw sprite center
            pygame.draw.circle(self.screen, (255, 255, 0), 
                             (sprite_center_x, sprite_center_y), 3)
        
        # Always draw hitbox (red box)
        pygame.draw.rect(self.screen, (255, 0, 0), self.wizard.hitbox, 2)
        
        if self.show_debug:
            # Draw hitbox center
            pygame.draw.circle(self.screen, (0, 255, 0), 
                             (self.wizard.hitbox.centerx, self.wizard.hitbox.centery), 3)
            
            # Draw center lines for hitbox
            pygame.draw.line(self.screen, (255, 0, 0), 
                           (self.wizard.hitbox.left, self.wizard.hitbox.centery), 
                           (self.wizard.hitbox.right, self.wizard.hitbox.centery), 1)
            pygame.draw.line(self.screen, (255, 0, 0), 
                           (self.wizard.hitbox.centerx, self.wizard.hitbox.top), 
                           (self.wizard.hitbox.centerx, self.wizard.hitbox.bottom), 1)
            
            # Draw info text
            info_text = [
                f"Wizard position: ({self.wizard.x}, {self.wizard.y})",
                f"Sprite center: ({sprite_center_x}, {sprite_center_y})",
                f"Hitbox position: ({self.wizard.hitbox.x}, {self.wizard.hitbox.y})",
                f"Hitbox size: {self.wizard.hitbox.width}x{self.wizard.hitbox.height}",
                f"Hitbox offset: ({self.wizard.hitbox_offset_x}, {self.wizard.hitbox_offset_y})",
                f"Animation: {self.wizard.state.upper()} (Frame: {self.wizard.current_frame})"
            ]
            
            # Draw text background
            text_height = len(info_text) * 25 + 10
            pygame.draw.rect(self.screen, (0, 0, 0, 128), 
                           pygame.Rect(10, 10, 380, text_height))
            
            # Draw text
            for i, text in enumerate(info_text):
                text_surface = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(text_surface, (20, 20 + i * 25))
        
        # Draw help text if enabled
        if self.show_help:
            help_text = [
                "SPACE: Toggle animation",
                "D: Toggle debug info",
                "H: Toggle help text",
                "F1: Take screenshot",
                "ESC: Exit"
            ]
            
            # Draw help text at bottom of screen
            help_height = len(help_text) * 25 + 10
            pygame.draw.rect(self.screen, (0, 0, 0, 128), 
                           pygame.Rect(10, SCREEN_HEIGHT - help_height - 10, 220, help_height))
            
            for i, text in enumerate(help_text):
                text_surface = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(text_surface, (20, SCREEN_HEIGHT - help_height + i * 25))
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the hitbox verification tool."""
        running = True
        
        print("\nWizard Hitbox Verifier")
        print("=====================")
        print("This tool shows the wizard's hitbox configuration.")
        print("Current hitbox settings:")
        print(f"Width: {self.wizard.hitbox.width} pixels")
        print(f"Height: {self.wizard.hitbox.height} pixels")
        print(f"Offset X: {self.wizard.hitbox_offset_x} pixels")
        print(f"Offset Y: {self.wizard.hitbox_offset_y} pixels")
        print("\nControls:")
        print("- Press SPACE to toggle animation")
        print("- Press D to toggle debug info")
        print("- Press H to toggle help text")
        print("- Press F1 to take a screenshot")
        print("- Press ESC to exit")
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update
            self.update()
            
            # Draw
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        # Clean up
        pygame.quit()


def main():
    """Run the verification tool."""
    verifier = HitboxVerifier()
    verifier.run()


if __name__ == "__main__":
    main()