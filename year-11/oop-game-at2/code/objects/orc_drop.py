"""
orc drop module.

This module contains the orc_drop class representing a obgect that lets the player leavle up to a better verson.
"""

import pygame
import random
from core.game_object import GameObject


class Orc_drop(GameObject):
    """Represents a obgect that lets the plyer leavle up and gain new abitys."""
    
    cost = 0
    name = None
    quantity  = None
    start_time = None
    duration = None
    key = ""
    gBuf = None
    dBuf = None
    rBuf = None
    sBuf = None
    
    def __init__(self, x, y, frames):
        """
        Initialise the orc drop.
        
        Args:
            x (int): X coordinate of the orc drop.
            y (int): Y coordinate of the orc drop.
            frames (list): List of animation frames for the orc drop.
        """
        # Calculate dimensions based on first frame
        width = frames[0].get_width()
        height = frames[0].get_height()
        super().__init__(x, y, width, height)
        
        self.frames = frames
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15  # Animation speed (lower is faster)
        self.lifetime = 600  # 10 seconds at 60 FPS
        self.bobbing_offset = 0
        self.bobbing_direction = 1
        self.bob_speed = 0.2
        self.collected = False
        self.name = "Orc drop"
        self.cost = None
        self.start_time = None
        self.sBuf = 2
        self.dBuf = 2
        self.rBuf = 2
        self.gBuf = 2
        self.duration = 1000000000000000 # last for ever
        self.key = str("")
        
        
    
    def update(self):
        """Update the orc drop animation and state."""
        if self.collected:
            return
            
        # Update lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.collected = True
            return
        
        # Update bobbing animation
        self.bobbing_offset += self.bobbing_direction * self.bob_speed
        if abs(self.bobbing_offset) > 3:
            self.bobbing_direction *= -1
        
        # Update animation frame
        self.animation_timer += 1
        if self.animation_timer >= 1 / self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_timer = 0
            
        # Update hitbox position
        self.hitbox.x = self.x
        self.hitbox.y = self.y + self.bobbing_offset
    
    def draw(self, screen):
        """
        Draw the orc drop with its current animation frame.
        
        Args:
            screen: The pygame surface to draw on.
        """
        if self.collected:
            return
            
        # Draw current frame with bobbing effect
        screen.blit(self.frames[self.current_frame], (self.x, self.y + self.bobbing_offset))
    
    def collect(self):
        """
        Mark the orc drop as collected and return bool.
        
        Returns:
            bool: The orc drop.
        """
        
        if not self.collected:
            self.collected = True
            self.Orc_drop
            return True
        return False