"""
Portal module.

This module contains the Portal class representing level exits.
"""

import pygame
import math
from utils.constants import TILE_SIZE

class Portal:
    """Represents a level exit portal."""
    
    def __init__(self, x, y):
        """
        Initialise the portal.
        
        Args:
            x (int): X coordinate of the portal.
            y (int): Y coordinate of the portal.
        """
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.hitbox = pygame.Rect(x, y, self.width, self.height)
        
        # Visual effects
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.glow_alpha = 0
        self.pulse_size = 0
        self.activated = False
    
    def update(self):
        """Update portal state and animations."""
        # Pulsing glow effect
        self.glow_alpha = 128 + 127 * math.sin(pygame.time.get_ticks() / 500)
        
        # Growing/shrinking effect
        self.pulse_size = 3 * math.sin(pygame.time.get_ticks() / 300)
        
        # Update hitbox position
        self.hitbox.x = self.x
        self.hitbox.y = self.y
    
    def draw(self, screen):
        """
        Draw the portal.
        
        Args:
            screen: The pygame surface to draw on.
        """
        # Draw glow effect
        glow_surf = pygame.Surface((self.width + 20 + self.pulse_size, 
                                   self.height + 20 + self.pulse_size), pygame.SRCALPHA)
        glow_surf.fill((100, 100, 255, int(self.glow_alpha * 0.3)))
        screen.blit(glow_surf, (self.x - 10 - self.pulse_size/2, self.y - 10 - self.pulse_size/2))
        
        # Draw inner portal
        portal_surf = pygame.Surface((self.width - 10, self.height - 10), pygame.SRCALPHA)
        
        # Create a swirling effect with changing colors
        t = pygame.time.get_ticks() / 1000
        r = 50 + int(50 * math.sin(t * 2))
        g = 50 + int(50 * math.sin(t * 1.5 + 2))
        b = 200 + int(55 * math.sin(t + 4))
        
        portal_surf.fill((r, g, b, 200))
        
        # Draw portal on screen
        screen.blit(portal_surf, (self.x + 5, self.y + 5))
        
        # Draw portal border
        pygame.draw.rect(screen, (200, 200, 255), 
                         (self.x, self.y, self.width, self.height), 3)
        
        # Draw some runes or symbols around the portal
        for i in range(4):
            angle = t * 2 + i * math.pi / 2
            x = self.x + self.width/2 + math.cos(angle) * (self.width/2 - 5)
            y = self.y + self.height/2 + math.sin(angle) * (self.height/2 - 5)
            
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 3)
    
    def is_player_colliding(self, player):
        """
        Check if the player is colliding with the portal.
        
        Args:
            player: The player object.
            
        Returns:
            bool: True if the player is colliding with the portal.
        """
        return self.hitbox.colliderect(player.hitbox)