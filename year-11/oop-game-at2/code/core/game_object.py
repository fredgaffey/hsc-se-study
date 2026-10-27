"""
Base GameObject class module.

This module contains the base GameObject class that all game objects inherit from.
"""

import pygame

class GameObject:
    """Base class for all game objects."""
    
    def __init__(self, x, y, width, height):
        """
        Initialise a game object.
        
        Args:
            x (int): X-coordinate of the object.
            y (int): Y-coordinate of the object.
            width (int): Width of the object's hitbox.
            height (int): Height of the object's hitbox.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(x, y, width, height)
    
    def update(self):
        """
        Update the object state.
        
        This method should be overridden by subclasses.
        """
        # Move hitbox with position
        self.hitbox.x = self.x
        self.hitbox.y = self.y
    
    def draw(self, screen):
        """
        Draw the object.
        
        This method should be overridden by subclasses.
        
        Args:
            screen: The pygame surface to draw on.
        """
        pass
    
    def collides_with(self, other):
        """
        Check if this object collides with another object.
        
        Args:
            other (GameObject): The other game object to check collision with.
            
        Returns:
            bool: True if the objects collide, False otherwise.
        """
        return self.hitbox.colliderect(other.hitbox)