#!/usr/bin/env python3
"""
Wizard Hitbox Adjuster - Interactive Tool

This module provides an interactive tool for adjusting the wizard's hitbox.
It allows precise positioning and saving of hitbox configurations.
"""

import os
import sys
import pygame
import time
import json

# Add the project root directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Import game modules
from utils.asset_loader import AssetLoader
from characters.wizard import Wizard
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class HitboxAdjusterTool:
    """Interactive tool for adjusting the wizard's hitbox."""
    
    def __init__(self):
        """Initialize the interactive hitbox adjustment tool."""
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wizard Hitbox Adjuster")
        self.clock = pygame.time.Clock()
        
        # Set up fonts
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 32)
        
        # Create asset loader
        self.asset_loader = AssetLoader()
        
        # Get wizard animation frames
        self.wizard_idle_frames = self.asset_loader.get_player_idle_frames("wizard")
        self.wizard_attack_frames = self.asset_loader.get_player_attack_frames("wizard")
        
        # Position wizard at center of screen
        wizard_x = SCREEN_WIDTH // 2 - 50
        wizard_y = SCREEN_HEIGHT // 2 - 62
        
        # Create wizard
        self.wizard = Wizard(wizard_x, wizard_y, 
                          self.wizard_idle_frames, self.wizard_attack_frames)
        
        # Create a custom hitbox we'll control directly
        self.custom_hitbox = pygame.Rect(
            self.wizard.hitbox.x,
            self.wizard.hitbox.y,
            self.wizard.hitbox.width,
            self.wizard.hitbox.height
        )
        
        # Store original position
        self.original_x = self.wizard.x
        self.original_y = self.wizard.y
        
        # Store original hitbox values
        self.original_hitbox = {
            "width": self.wizard.hitbox.width,
            "height": self.wizard.hitbox.height,
            "offset_x": self.wizard.hitbox_offset_x,
            "offset_y": self.wizard.hitbox_offset_y
        }
        
        # Create a simple map class for wizard updates
        class SimpleMap:
            def is_wall(self, x, y):
                return False
        
        self.game_map = SimpleMap()
        
        # Saved hitbox configurations
        self.saved_configs = self.load_hitbox_configs()
        
        # UI settings
        self.adjustment_speed = 1
        self.show_debug = True
        
    def load_hitbox_configs(self):
        """Load saved hitbox configurations from file."""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    "wizard_hitbox_configs.json")
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading configurations: {e}")
            return []
    
    def save_hitbox_configs(self):
        """Save current hitbox configuration to file."""
        try:
            # Create a new configuration
            new_config = {
                "name": f"Config {len(self.saved_configs) + 1}",
                "width": self.custom_hitbox.width,
                "height": self.custom_hitbox.height,
                "offset_x": self.wizard.hitbox_offset_x,
                "offset_y": self.wizard.hitbox_offset_y,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add to saved configs
            self.saved_configs.append(new_config)
            
            # Save to file
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    "wizard_hitbox_configs.json")
            with open(config_path, 'w') as f:
                json.dump(self.saved_configs, f, indent=2)
                
            print(f"Saved configuration: {new_config}")
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def load_config(self, config):
        """Load a saved hitbox configuration."""
        try:
            # Update hitbox dimensions
            self.custom_hitbox.width = config["width"]
            self.custom_hitbox.height = config["height"]
            
            # Update offsets
            self.wizard.hitbox_offset_x = config["offset_x"]
            self.wizard.hitbox_offset_y = config["offset_y"]
            
            # Update hitbox position
            self.custom_hitbox.x = self.wizard.x + self.wizard.hitbox_offset_x
            self.custom_hitbox.y = self.wizard.y + self.wizard.hitbox_offset_y
            
            print(f"Loaded configuration: {config}")
            return True
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return False
    
    def reset_hitbox(self):
        """Reset hitbox to original values."""
        # Reset dimensions
        self.custom_hitbox.width = self.original_hitbox["width"]
        self.custom_hitbox.height = self.original_hitbox["height"]
        
        # Reset offsets
        self.wizard.hitbox_offset_x = self.original_hitbox["offset_x"]
        self.wizard.hitbox_offset_y = self.original_hitbox["offset_y"]
        
        # Update position
        self.custom_hitbox.x = self.wizard.x + self.wizard.hitbox_offset_x
        self.custom_hitbox.y = self.wizard.y + self.wizard.hitbox_offset_y
    
    def handle_events(self):
        """Handle user input events."""
        # Track if the hitbox was moved this frame
        hitbox_moved = False
        
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
                elif event.key == pygame.K_c:
                    # Center the hitbox on the sprite
                    sprite_center_x = self.wizard.x + 50
                    sprite_center_y = self.wizard.y + 62
                    self.custom_hitbox.x = sprite_center_x - self.custom_hitbox.width // 2
                    self.custom_hitbox.y = sprite_center_y - self.custom_hitbox.height // 2
                    hitbox_moved = True
                elif event.key == pygame.K_r:
                    # Reset hitbox to original values
                    self.reset_hitbox()
                    hitbox_moved = True
                elif event.key == pygame.K_s:
                    # Save current configuration
                    self.save_hitbox_configs()
                elif event.key == pygame.K_l:
                    # Load the last configuration
                    if self.saved_configs:
                        self.load_config(self.saved_configs[-1])
                        hitbox_moved = True
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    # Increase adjustment speed
                    self.adjustment_speed = min(10, self.adjustment_speed + 1)
                elif event.key == pygame.K_MINUS:
                    # Decrease adjustment speed
                    self.adjustment_speed = max(1, self.adjustment_speed - 1)
                
                # Move ONLY the hitbox with arrow keys
                elif event.key == pygame.K_UP:
                    # Move hitbox up or decrease height
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # With SHIFT: adjust height
                        self.custom_hitbox.height = max(10, self.custom_hitbox.height - self.adjustment_speed)
                    else:
                        # Without SHIFT: move hitbox
                        self.custom_hitbox.y -= self.adjustment_speed
                    hitbox_moved = True
                elif event.key == pygame.K_DOWN:
                    # Move hitbox down or increase height
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # With SHIFT: adjust height
                        self.custom_hitbox.height += self.adjustment_speed
                    else:
                        # Without SHIFT: move hitbox
                        self.custom_hitbox.y += self.adjustment_speed
                    hitbox_moved = True
                elif event.key == pygame.K_LEFT:
                    # Move hitbox left or decrease width
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # With SHIFT: adjust width
                        self.custom_hitbox.width = max(10, self.custom_hitbox.width - self.adjustment_speed)
                    else:
                        # Without SHIFT: move hitbox
                        self.custom_hitbox.x -= self.adjustment_speed
                    hitbox_moved = True
                elif event.key == pygame.K_RIGHT:
                    # Move hitbox right or increase width
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # With SHIFT: adjust width
                        self.custom_hitbox.width += self.adjustment_speed
                    else:
                        # Without SHIFT: move hitbox
                        self.custom_hitbox.x += self.adjustment_speed
                    hitbox_moved = True
                
                # Number keys for loading saved configs
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    config_index = event.key - pygame.K_1
                    if config_index < len(self.saved_configs):
                        self.load_config(self.saved_configs[config_index])
                        hitbox_moved = True
        
        # If hitbox was moved, update offsets
        if hitbox_moved:
            self.wizard.hitbox_offset_x = self.custom_hitbox.x - self.wizard.x
            self.wizard.hitbox_offset_y = self.custom_hitbox.y - self.wizard.y
            
        return True  # Continue running
    
    def update(self):
        """Update game state."""
        # Force wizard to stay at original position
        self.wizard.x = self.original_x
        self.wizard.y = self.original_y
        
        # Update wizard animations only
        self.wizard.update(self.game_map)
        
        # Force position again after update
        self.wizard.x = self.original_x
        self.wizard.y = self.original_y
        
        # Use our custom hitbox for wizard
        self.wizard.hitbox = self.custom_hitbox
    
    def draw(self):
        """Draw the current state to the screen."""
        # Clear the screen
        self.screen.fill((30, 30, 40))
        
        # Draw grid in debug mode
        if self.show_debug:
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
            
            # Draw sprite center
            sprite_center_x = self.wizard.x + 50
            sprite_center_y = self.wizard.y + 62
            pygame.draw.circle(self.screen, (255, 255, 0), 
                             (sprite_center_x, sprite_center_y), 3)
            
            # Draw center lines for sprite
            pygame.draw.line(self.screen, (0, 0, 255), 
                           (sprite_center_x, self.wizard.y), 
                           (sprite_center_x, self.wizard.y + 125), 1)
            pygame.draw.line(self.screen, (0, 0, 255), 
                           (self.wizard.x, sprite_center_y), 
                           (self.wizard.x + 100, sprite_center_y), 1)
        
        # Always draw hitbox (red box)
        pygame.draw.rect(self.screen, (255, 0, 0), self.custom_hitbox, 2)
        
        if self.show_debug:
            # Draw hitbox center
            pygame.draw.circle(self.screen, (0, 255, 0), 
                             (self.custom_hitbox.centerx, self.custom_hitbox.centery), 3)
            
            # Draw center lines for hitbox
            pygame.draw.line(self.screen, (255, 0, 0), 
                           (self.custom_hitbox.left, self.custom_hitbox.centery), 
                           (self.custom_hitbox.right, self.custom_hitbox.centery), 1)
            pygame.draw.line(self.screen, (255, 0, 0), 
                           (self.custom_hitbox.centerx, self.custom_hitbox.top), 
                           (self.custom_hitbox.centerx, self.custom_hitbox.bottom), 1)
            
            # Draw info text
            info_text = [
                f"Wizard position: ({self.wizard.x}, {self.wizard.y}) - FIXED, NEVER MOVES",
                f"Hitbox position: ({self.custom_hitbox.x}, {self.custom_hitbox.y})",
                f"Hitbox size: {self.custom_hitbox.width}x{self.custom_hitbox.height}",
                f"Hitbox offset: ({self.wizard.hitbox_offset_x}, {self.wizard.hitbox_offset_y})",
                f"Movement speed: {self.adjustment_speed} pixel(s) per keypress",
                f"Saved configurations: {len(self.saved_configs)}"
            ]
            
            # Draw text background
            text_height = len(info_text) * 25 + 10
            pygame.draw.rect(self.screen, (0, 0, 0, 128), 
                           pygame.Rect(10, 10, 410, text_height))
            
            # Draw text
            for i, text in enumerate(info_text):
                text_surface = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(text_surface, (20, 20 + i * 25))
            
            # Draw controls text
            controls_text = [
                "ARROWS: Move hitbox | SHIFT+ARROWS: Resize hitbox",
                "+/-: Adjust movement speed",
                "C: Center hitbox on sprite | R: Reset to original",
                "S: Save configuration | L: Load last configuration",
                "1-9: Load saved configuration",
                "D: Toggle debug visuals | SPACE: Toggle animation",
                "ESC: Exit"
            ]
            
            # Draw controls background
            controls_height = len(controls_text) * 25 + 10
            pygame.draw.rect(self.screen, (0, 0, 0, 128), 
                           pygame.Rect(SCREEN_WIDTH - 410, 10, 400, controls_height))
            
            # Draw controls text
            for i, text in enumerate(controls_text):
                text_surface = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(text_surface, (SCREEN_WIDTH - 400, 20 + i * 25))
        else:
            # Simple instructions when debug is off
            info_text = [
                "D: Show debug info",
                "ARROWS: Move hitbox | SHIFT+ARROWS: Resize",
                "SPACE: Toggle animation"
            ]
            
            for i, text in enumerate(info_text):
                text_surface = self.font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.bottomleft = (10, SCREEN_HEIGHT - 10 - (i * 25))
                
                # Draw background
                bg_rect = text_rect.inflate(10, 5)
                bg_rect.bottomleft = (5, SCREEN_HEIGHT - 5 - (i * 25))
                pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
                
                # Draw text
                self.screen.blit(text_surface, text_rect)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the hitbox adjustment tool."""
        running = True
        
        print("\nWizard Hitbox Adjuster")
        print("=====================")
        print("This tool allows you to adjust the wizard's hitbox.")
        print("- Use ARROW KEYS to move the hitbox")
        print("- Hold SHIFT + ARROW KEYS to resize the hitbox")
        print("- Press C to center the hitbox on the sprite")
        print("- Press R to reset to original values")
        print("- Press S to save the current configuration")
        print("- Press D to toggle debug visuals")
        print("- Press SPACE to toggle animation")
        print("- Press ESC to exit")
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        # Clean up
        pygame.quit()
        
        # Return final settings
        return {
            "width": self.custom_hitbox.width,
            "height": self.custom_hitbox.height,
            "offset_x": self.wizard.hitbox_offset_x,
            "offset_y": self.wizard.hitbox_offset_y
        }


def main():
    """Run the tool and display results."""
    # Run the tool
    tool = HitboxAdjusterTool()
    final_settings = tool.run()
    
    print("\nFinal Hitbox Settings:")
    print(f"Width: {final_settings['width']} pixels")
    print(f"Height: {final_settings['height']} pixels")
    print(f"Offset X: {final_settings['offset_x']} pixels")
    print(f"Offset Y: {final_settings['offset_y']} pixels")
    
    print("\nCopy this code to update the wizard class:")
    print("# Update the wizard hitbox position")
    print(f"hitbox_width = {final_settings['width']}  # Custom hitbox width")
    print(f"hitbox_height = {final_settings['height']}  # Custom hitbox height")
    print(f"self.hitbox_offset_x = {final_settings['offset_x']}  # Custom X offset")
    print(f"self.hitbox_offset_y = {final_settings['offset_y']}  # Custom Y offset")


if __name__ == "__main__":
    main()