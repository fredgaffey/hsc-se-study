"""
Skeleton module.

This module contains the Skeleton class representing a skeleton enemy type in the game.

TODO: Skeleton Class Functionality
- Implement skeleton-specific attacks and abilities
- Add bone shield ability that blocks incoming damage
- Implement skeleton regeneration when near other skeletons
- Add ability to resurrect after a delay if not fully destroyed
- Implement archer/mage/warrior skeleton variants
- Add bone projectiles for ranged skeleton attacks
- Implement bone pile mechanic that spawns new skeletons
- Add vulnerability to holy/fire damage
"""

import pygame
import math
import time
from utils.constants import FPS
from characters.enemy import Enemy

class Skeleton(Enemy):
    """Represents a Skeleton enemy type."""
    
    def __init__(self, x, y, frames):
        """
        Initialize the Skeleton.
        
        Args:
            x (int): X-coordinate of the Skeleton.
            y (int): Y-coordinate of the Skeleton.
            frames (dict): Dictionary of animation frames for different states.
        """
        super().__init__(x, y, frames)
        
        # Skeleton-specific attributes
        self.max_health = 40  # Skeletons have less health
        self.health = 40
        self.attack_damage = 15
        self.speed = 1.5  # Slightly faster than regular enemies
        self.aggro_range = 220  # Better sight range
        self.attack_range = 70
        
        # Special abilities
        self.resurrection_chance = 0.25  # 25% chance to resurrect once
        self.has_resurrected = False
        self.bone_shield_active = False
        self.bone_shield_cooldown = 10.0  # Seconds
        self.last_shield_time = 0
        
        # TODO: Implement skeleton-specific abilities
        # TODO: Add resurrection mechanic
        # TODO: Configure bone shield mechanics
        # TODO: Implement skeleton type variations
    
    def update(self, player):
        """
        Update the Skeleton based on its state and the player.
        
        Args:
            player: The player object to interact with.
        """
        # TODO: Implement skeleton-specific behavior
        # TODO: Add bone shield activation logic
        # TODO: Check for nearby skeletons for regeneration
        # TODO: Handle different skeleton variants
        
        current_time = time.time()
        
        # Try to activate bone shield when low on health
        if (not self.bone_shield_active and self.health < self.max_health * 0.3 and
            current_time - self.last_shield_time > self.bone_shield_cooldown):
            self.bone_shield_active = True
            self.defence += 10  # Temporarily increase defence
            # Shield will last for 5 seconds
            self.last_shield_time = current_time
        
        # Deactivate bone shield after duration
        if self.bone_shield_active and current_time - self.last_shield_time > 5.0:
            self.bone_shield_active = False
            self.defence -= 10  # Remove defence bonus
        
        # Call parent update method
        super().update(player)
    
    def take_damage(self, amount):
        """
        Take damage with potential resurrection when killed.
        
        Args:
            amount (int): The amount of damage to take.
            
        Returns:
            bool: True if the Skeleton died permanently, False otherwise.
        """
        # TODO: Implement resurrection mechanics
        # TODO: Add damage type vulnerabilities
        # TODO: Implement bone shield damage reduction
        
        # Reduce damage if bone shield is active
        if self.bone_shield_active:
            amount = max(1, amount // 2)
        
        # Call parent take_damage method
        died = super().take_damage(amount)
        
        # Check for resurrection chance
        if died and not self.has_resurrected and random.random() < self.resurrection_chance:
            # Resurrect with partial health
            self.health = self.max_health // 3
            self.is_dying = False
            self.state = "idle"
            self.has_resurrected = True
            return False
        
        return died
    
    def draw(self, screen):
        """
        Draw the Skeleton with its current animation frame.
        
        Args:
            screen: The pygame surface to draw on.
        """
        # Call parent draw method
        super().draw(screen)
        
        # TODO: Add skeleton-specific visual effects
        # TODO: Draw bone shield when active
        # TODO: Add resurrection animation
        # TODO: Implement variant-specific visual elements
        
        # Draw bone shield effect when active
        if self.bone_shield_active:
            # Create a bone shield circle around the skeleton
            shield_radius = max(self.hitbox.width, self.hitbox.height) + 10
            shield_surface = pygame.Surface((shield_radius*2, shield_radius*2), pygame.SRCALPHA)
            shield_colour = (220, 220, 220, 150)  # Bone white with transparency
            pygame.draw.circle(shield_surface, shield_colour, (shield_radius, shield_radius), shield_radius, 3)
            
            # Draw zigzag pattern to represent bones
            segments = 16
            for i in range(segments):
                angle1 = i * (2 * math.pi / segments)
                angle2 = (i + 0.5) * (2 * math.pi / segments)
                x1 = shield_radius + int(math.cos(angle1) * shield_radius)
                y1 = shield_radius + int(math.sin(angle1) * shield_radius)
                x2 = shield_radius + int(math.cos(angle2) * (shield_radius - 5))
                y2 = shield_radius + int(math.sin(angle2) * (shield_radius - 5))
                pygame.draw.line(shield_surface, shield_colour, (x1, y1), (x2, y2), 2)
            
            # Draw the shield (using Pygame's centerx/centery properties)
            screen.blit(shield_surface, 
                      (self.hitbox.centerx - shield_radius, self.hitbox.centery - shield_radius))