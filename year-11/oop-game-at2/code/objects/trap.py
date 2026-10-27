"""
Trap module.

This module contains the Trap class representing traps in the game.
"""

import pygame
import random
import time
import math
from utils.constants import TILE_SIZE
from core.game_object import GameObject

class Trap(GameObject):
    """Represents a trap that damages the player."""
    
    def __init__(self, x, y, inactive_image, active_image):
        """
        Initialise the trap.
        
        Args:
            x (int): X coordinate of the trap.
            y (int): Y coordinate of the trap.
            inactive_image: The image for the inactive trap.
            active_image: The image for the active trap.
        """
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        
        # Trap images
        self.inactive_image = inactive_image
        self.active_image = active_image
        
        
        # Trap properties
        self.damage = 10
        self.is_visible = random.random() < 0.7  # 70% chance to be visible
        self.is_active = False  # Spikes down initially
        self.was_triggered = False  # For damage cooldown
        self.triggered_time = 0  # When the trap was last triggered for damage
        self.trigger_cooldown = 3.0  # Seconds before it can cause damage again
        
        # Cycle timing (spikes alternating up and down)
        self.cycle_time = random.uniform(2.0, 4.0)  # Random cycle time between 2-4 seconds
        self.cycle_start = time.time() + random.uniform(0, self.cycle_time)  # Randomize initial phase
        self.active_duration = self.cycle_time * 0.4  # Spikes are up 40% of cycle time
        
        # Visual effects
        self.shake_offset = [0, 0]
        self.shake_intensity = 0
        self.shake_duration = 0.3  # seconds
        self.warning_alpha = 0
        self.warning_time = 0.5  # Seconds of warning before spikes come up
        
    def update(self):
        """Update trap state."""
        # Move hitbox with position
        super().update()
        
        current_time = time.time()
        
        # Update active state based on cycle time
        elapsed_in_cycle = (current_time - self.cycle_start) % self.cycle_time
        
        # Determine if spikes should be up or down
        was_active = self.is_active
        self.is_active = elapsed_in_cycle < self.active_duration
        
        # If spikes just went up, shake the trap
        if not was_active and self.is_active:
            self.start_shake()
        
        # Reset damage trigger after cooldown
        if self.was_triggered and current_time - self.triggered_time > self.trigger_cooldown:
            self.was_triggered = False
            
        # Handle trap shake animation
        if self.shake_intensity > 0:
            elapsed_shake = current_time - self.shake_start_time
            if elapsed_shake < self.shake_duration:
                # Shake decreases over time
                remaining = 1 - (elapsed_shake / self.shake_duration)
                self.shake_intensity = 3 * remaining
                self.shake_offset = [
                    random.uniform(-self.shake_intensity, self.shake_intensity),
                    random.uniform(-self.shake_intensity, self.shake_intensity)
                ]
            else:
                self.shake_offset = [0, 0]
                self.shake_intensity = 0
                
        # No warning flash for hidden traps (removed)
        
        # No warning flash before spikes come up (removed)
    
    def start_shake(self):
        """Start the trap shaking animation."""
        self.shake_intensity = 3
        self.shake_start_time = time.time()
            
    def draw(self, screen):
        """
        Draw the trap.
        
        Args:
            screen: The pygame surface to draw on.
        """
        draw_x = self.x + self.shake_offset[0]
        draw_y = self.y + self.shake_offset[1]
        
        if self.is_visible:
            # Draw visible trap based on active state
            if self.is_active:
                # Draw active trap (spikes up)
                screen.blit(self.active_image, (draw_x, draw_y))
                
                # Add blood effect if recently triggered player damage
                if self.was_triggered and time.time() - self.triggered_time < 0.5:
                    blood_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                    blood_alpha = int(100 * (1 - ((time.time() - self.triggered_time) / 0.5)))
                    blood_surf.fill((200, 0, 0, blood_alpha))
                    screen.blit(blood_surf, (draw_x, draw_y))
            else:
                # Draw inactive trap (spikes down)
                screen.blit(self.inactive_image, (draw_x, draw_y))
                
                # No glow effect on traps as requested
        else:
            # Draw hidden trap (very subtle)
            # Create a slightly darker floor tile
            base_img = self.inactive_image.copy()
            dark_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 200))  # Very dark overlay
            base_img.blit(dark_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # No warning flash as requested
            
            screen.blit(base_img, (draw_x, draw_y))
    
    def trigger(self, player):
        """
        Trigger the trap if it's active and not already triggered.
        Only damages the player when spikes are up.
        
        Args:
            player: The player object that triggered the trap.
            
        Returns:
            int: The amount of damage dealt, or 0 if no damage.
        """
        # SAFETY CHECK - Only allow damage when spikes are up
        if not self.is_active:
            return 0
            
        # Check cooldown state
        current_time = time.time()
        in_cooldown = self.was_triggered and (current_time - self.triggered_time <= self.trigger_cooldown)
        
        # If in cooldown, don't deal damage again
        if in_cooldown:
            return 0
            
        # If we get here, trap is active and not in cooldown - deal damage!
        self.was_triggered = True
        self.triggered_time = current_time
        
        # Start shake effect
        self.start_shake()
        
        # Damage the player
        if player:
            player.take_damage(self.damage)
            return self.damage
            
        return 0