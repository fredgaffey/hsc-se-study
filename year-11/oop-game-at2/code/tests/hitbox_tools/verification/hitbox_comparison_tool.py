#!/usr/bin/env python3
"""
Wizard Hitbox Comparison Tool

This module provides a tool for comparing different wizard hitbox configurations.
It allows visualization of both original and new hitbox positions relative to the sprite.
"""

import os
import sys
import pygame
import time

# Add the project root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Import game modules
from utils.asset_loader import AssetLoader
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class HitboxComparisonTool:
    """Tool for comparing different wizard hitbox positions."""
    
    def __init__(self):
        """Initialize the comparison tool."""
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wizard Hitbox Comparison")
        self.clock = pygame.time.Clock()
        
        # Set up fonts
        self.font = pygame.font.Font(None, 24)
        
        # Create asset loader
        self.asset_loader = AssetLoader()
        
        # Get wizard frames directly from asset loader
        self.idle_frames = self.asset_loader.get_player_idle_frames("wizard")
        self.attack_frames = self.asset_loader.get_player_attack_frames("wizard")
        
        # Fixed position for sprite (center of screen)
        self.sprite_x = SCREEN_WIDTH // 2 - 50
        self.sprite_y = SCREEN_HEIGHT // 2 - 62
        
        # Current animation state
        self.state = "idle"
        self.current_frame = 0
        self.frame_time = 0
        self.attacking = False
        self.attack_start_time = 0
        
        # Original hitbox settings
        self.original_hitbox = {
            "width": 16,
            "height": 20,
            "offset_x": 42,
            "offset_y": 65  # Original value before adjustments
        }
        
        # New hitbox settings
        self.new_hitbox = {
            "width": 16,
            "height": 20,
            "offset_x": 43,
            "offset_y": 50  # Adjusted value from our tool
        }
        
        # Create original hitbox rectangle (RED)
        self.original_hitbox_rect = pygame.Rect(
            self.sprite_x + self.original_hitbox["offset_x"],
            self.sprite_y + self.original_hitbox["offset_y"],
            self.original_hitbox["width"],
            self.original_hitbox["height"]
        )
        
        # Create new hitbox rectangle (GREEN)
        self.new_hitbox_rect = pygame.Rect(
            self.sprite_x + self.new_hitbox["offset_x"],
            self.sprite_y + self.new_hitbox["offset_y"],
            self.new_hitbox["width"],
            self.new_hitbox["height"]
        )
        
        # Display mode
        self.show_mode = "both"  # Can be "original", "new", or "both"
    
    def update_animation(self):
        """Update the animation state and frame."""
        current_time = time.time()
        
        if self.attacking:
            # Attack animation
            frames = self.attack_frames
            animation_time = 0.7  # Total time for attack animation
            frame_duration = animation_time / len(frames)
            
            # Calculate current frame based on time since attack started
            elapsed = current_time - self.attack_start_time
            
            if elapsed >= animation_time:
                # Animation finished
                self.attacking = False
                self.state = "idle"
                self.current_frame = 0
            else:
                # Set current frame based on elapsed time
                self.current_frame = min(int(elapsed / frame_duration), len(frames) - 1)
        else:
            # Idle animation
            frames = self.idle_frames
            frame_duration = 0.1  # Time per frame for idle animation
            
            # Update frame based on time
            if current_time - self.frame_time > frame_duration:
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.frame_time = current_time
    
    def draw_sprite(self):
        """Draw the sprite at its fixed position."""
        # Select current frame based on state
        if self.state == "idle":
            current_image = self.idle_frames[self.current_frame]
        else:
            current_image = self.attack_frames[self.current_frame]
        
        # Draw the current frame
        self.screen.blit(current_image, (self.sprite_x, self.sprite_y))
    
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
                    if not self.attacking:
                        self.attacking = True
                        self.state = "attack"
                        self.attack_start_time = time.time()
                elif event.key == pygame.K_1:
                    # Show only original hitbox
                    self.show_mode = "original"
                elif event.key == pygame.K_2:
                    # Show only new hitbox
                    self.show_mode = "new"
                elif event.key == pygame.K_3:
                    # Show both hitboxes
                    self.show_mode = "both"
        
        return True
    
    def draw(self):
        """Draw the current state to screen."""
        # Clear the screen
        self.screen.fill((30, 30, 40))
        
        # Draw grid
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, (50, 50, 60), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (50, 50, 60), (0, y), (SCREEN_WIDTH, y))
        
        # Draw the sprite at its fixed position
        self.draw_sprite()
        
        # Draw sprite boundaries (blue box)
        sprite_rect = pygame.Rect(self.sprite_x, self.sprite_y, 100, 125)
        pygame.draw.rect(self.screen, (0, 0, 255), sprite_rect, 1)
        
        # Draw sprite center
        sprite_center_x = self.sprite_x + 50
        sprite_center_y = self.sprite_y + 62
        pygame.draw.circle(self.screen, (255, 255, 0), 
                         (sprite_center_x, sprite_center_y), 3)
        
        # Draw center lines for sprite
        pygame.draw.line(self.screen, (0, 0, 255), 
                       (sprite_center_x, self.sprite_y), 
                       (sprite_center_x, self.sprite_y + 125), 1)
        pygame.draw.line(self.screen, (0, 0, 255), 
                       (self.sprite_x, sprite_center_y), 
                       (self.sprite_x + 100, sprite_center_y), 1)
        
        # Draw hitboxes based on mode
        if self.show_mode in ["original", "both"]:
            # Draw original hitbox (red)
            pygame.draw.rect(self.screen, (255, 0, 0), self.original_hitbox_rect, 2)
            # Draw original hitbox center
            pygame.draw.circle(self.screen, (255, 100, 100), 
                             (self.original_hitbox_rect.centerx, self.original_hitbox_rect.centery), 3)
        
        if self.show_mode in ["new", "both"]:
            # Draw new hitbox (green)
            pygame.draw.rect(self.screen, (0, 255, 0), self.new_hitbox_rect, 2)
            # Draw new hitbox center
            pygame.draw.circle(self.screen, (100, 255, 100), 
                             (self.new_hitbox_rect.centerx, self.new_hitbox_rect.centery), 3)
        
        # Draw info text
        info_text = [
            f"Sprite position: ({self.sprite_x}, {self.sprite_y})",
            f"Sprite center: ({sprite_center_x}, {sprite_center_y})",
            "",
            "Original Hitbox (RED):",
            f"Width: {self.original_hitbox['width']} | Height: {self.original_hitbox['height']}",
            f"Offset X: {self.original_hitbox['offset_x']} | Offset Y: {self.original_hitbox['offset_y']}",
            f"Position: ({self.original_hitbox_rect.x}, {self.original_hitbox_rect.y})",
            "",
            "New Hitbox (GREEN):",
            f"Width: {self.new_hitbox['width']} | Height: {self.new_hitbox['height']}",
            f"Offset X: {self.new_hitbox['offset_x']} | Offset Y: {self.new_hitbox['offset_y']}",
            f"Position: ({self.new_hitbox_rect.x}, {self.new_hitbox_rect.y})"
        ]
        
        # Draw text background
        text_height = len(info_text) * 25 + 10
        pygame.draw.rect(self.screen, (0, 0, 0, 128), 
                       pygame.Rect(10, 10, 400, text_height))
        
        # Draw text
        for i, text in enumerate(info_text):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20 + i * 25))
        
        # Draw controls text
        controls_text = [
            "1: Show only original hitbox (RED)",
            "2: Show only new hitbox (GREEN)",
            "3: Show both hitboxes",
            "SPACE: Toggle animation",
            "ESC: Exit"
        ]
        
        # Draw controls background
        controls_height = len(controls_text) * 25 + 10
        pygame.draw.rect(self.screen, (0, 0, 0, 128), 
                       pygame.Rect(SCREEN_WIDTH - 290, 10, 280, controls_height))
        
        # Draw controls text
        for i, text in enumerate(controls_text):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (SCREEN_WIDTH - 280, 20 + i * 25))
        
        # Draw current mode indicator
        mode_text = f"Current Display Mode: {self.show_mode.upper()}"
        mode_surface = self.font.render(mode_text, True, (255, 255, 255))
        mode_rect = mode_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        mode_bg = mode_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), mode_bg)
        self.screen.blit(mode_surface, mode_rect)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the comparison tool."""
        running = True
        
        print("\nWizard Hitbox Comparison")
        print("=======================")
        print("This tool shows a comparison between original and adjusted hitboxes.")
        print("Original hitbox: RED")
        print("New hitbox: GREEN")
        print("- Press 1 to show only the original hitbox")
        print("- Press 2 to show only the new hitbox")
        print("- Press 3 to show both hitboxes")
        print("- Press SPACE to toggle animation")
        print("- Press ESC to exit")
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update animation
            self.update_animation()
            
            # Draw everything
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        # Clean up
        pygame.quit()


def main():
    """Run the comparison tool."""
    tool = HitboxComparisonTool()
    tool.run()


if __name__ == "__main__":
    main()