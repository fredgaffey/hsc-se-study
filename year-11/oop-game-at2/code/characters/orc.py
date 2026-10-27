"""
Orc module.

This module contains the Orc class representing an orc enemy type in the game.

TODO: Orc Class Functionality
- Implement unique Orc attack patterns with higher damage but slower speed
- Add berserker mechanic where Orc becomes stronger at low health
- Implement Orc-specific death and hurt animations
- Add area-of-effect attacks for larger Orc variants
- Support for different Orc types (warrior, archer, shaman)
- Implement rage mechanic that builds up during combat
- Add unique sound effects for Orc vocalizations
- Implement Orc pack behavior when multiple Orcs are nearby
"""

import pygame
import math
import time
from utils.constants import FPS
from characters.enemy import Enemy

class Orc(Enemy):
    """Represents an Orc enemy type."""    
    def __init__(self, x, y, frames):
        """
        Initialize the Orc.
        
        Args:
            x (int): X-coordinate of the Orc.
            y (int): Y-coordinate of the Orc.
            frames (dict): Dictionary of animation frames for different states.
        """
        super().__init__(x, y, frames)
        
        # TODO: Override enemy attributes for Orc
        self.max_health = 100  # orc's have more health
        self.health = 100
        self.attack_damage = 22 # orc's have more damage
        self.speed = 2.3  # much much slower than regular enemies
        self.attack_range = 40 # worse then regular enemies
        self.attack_cooldown = 2.5 # worse then regular enemies
        
        # TODO: Implement Orc-specific stats and abilities
        # all are much harder to beat then a regular skeleton
        self.aggro_range = 200
        self.agro_health_activate = 50
        self.aggro_speed = 4
        self.aggro_attack_cooldown = 1.0
        self.aggro_attack_damage = 25
        self.aggro_true = False
        self.type_of_enemy = "orc"
        
        # TODO: Configure area-of-effect attacks
        
    def check_agro_state(self):
        if self.health <= self.agro_health_activate:
            self.aggro_true = True
            return True
        return False
    
    def update(self, player):
        """
        Update the Orc based on its state and the player.
        
        Args:
            player: The player object to interact with.
        """
        # TODO: Implement Orc-specific update logic
        # TODO: Handle berserker state at low health
        # TODO: Manage rage buildup during combat
        # TODO: Implement pack behavior with nearby Orcs
        
        # For now, use the base enemy update functionality
        if self.check_agro_state():
            self.speed = self.aggro_speed
            self.attack_cooldown = self.aggro_attack_cooldown
            self.attack_range = self.aggro_range
            
        super().update(player)
    
    def take_damage(self, amount):
        """
        Take damage, possibly entering berserker rage at low health.
        
        Args:
            amount (int): The amount of damage to take.
            
        Returns:
            bool: True if the Orc died, False otherwise.
        """
        
        # TODO: Implement berserker rage when health is low
        # TODO: Add rage mechanics for increased damage/speed
        # TODO: Implement unique hurt reactions
        
        # For now, use the base enemy damage handling
        
        return super().take_damage(amount)
    
    def draw(self, screen):
        """
        Draw the Orc with its current animation frame.
        
        Args:
            screen: The pygame surface to draw on.
        """
        # TODO: Add Orc-specific visual effects
        # TODO: Implement rage visual indicators
        # TODO: Add berserker state visuals
        
        # For now, use the base enemy drawing functionality
        super().draw(screen)