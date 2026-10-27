"""
Character module.

This module contains the base Character class that all playable and non-playable characters
inherit from. It provides common functionality for all character types.

TODO: Character Class Functionality
- Implement base stats system (strength, dexterity, intelligence, etc.)
- Add character level and experience system
- Implement skill system with active and passive abilities
- Add inventory management for all character types
- Support equipment slots and item effects
- Implement status effects system (poison, stun, etc.)
- Add character attributes like race, class, alignment
- Implement character progression and skill trees
- Add faction/reputation system for NPCs and players
- Support for character customization
"""

import pygame
import math
import time
from utils.constants import TILE_SIZE
from core.game_object import GameObject

class Character(GameObject):
    """Base class for all characters in the game (players, enemies, NPCs)."""

    
    def __init__(self, x, y, width, height, sprite_width=0, sprite_height=0):
        """
        Initialise a character.
        
        Args:
            x (int): X-coordinate of the character.
            y (int): Y-coordinate of the character.
            width (int): Width of the character's hitbox.
            height (int): Height of the character's hitbox.
            sprite_width (int): Width of the character's sprite (0 means same as hitbox).
            sprite_height (int): Height of the character's sprite (0 means same as hitbox).
        """
        print("Charicter class init"*10000)
        super().__init__(x, y, width, height)
        
        # Character dimensions (for sprite rendering)
        self.sprite_width = sprite_width if sprite_width > 0 else width
        self.sprite_height = sprite_height if sprite_height > 0 else height
        
        # Animation properties
        self.frames = {}  # Dictionary of animation frames by state
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.2  # Lower is faster
        self.state = "idle"  # Default state
        self.facing_left = False
        
        # Positional properties
        self.hitbox_offset_x = 0
        self.hitbox_offset_y = 0
        self.hitbox = pygame.Rect(x + self.hitbox_offset_x, y + self.hitbox_offset_y, width, height)
        
        # Movement properties
        self.speed = 2
        self.moving = False
        
        # Combat properties
        self.max_health = 100
        self.health = 100
        self.attack_damage = 10
        self.defence = 0  # Australian spelling: defence
        self.attack_range = 50
        self.attack_cooldown = 1.0
        self.last_attack_time = 0
        
        # TODO: Implement character stats (str, dex, int, etc.)
        # TODO: Add level and experience system
        # TODO: Implement faction/alignment tracking
        # TODO: Add inventory system
        # TODO: Implement equipment slots and effects
    
    def update(self, game_map=None):
        """
        Update the character's state and position.
        
        Args:
            game_map: The game map for collision detection.
        """
        # Update hitbox position
        self.hitbox.x = self.x + self.hitbox_offset_x
        self.hitbox.y = self.y + self.hitbox_offset_y
        
        # TODO: Implement common update logic for all characters
        # TODO: Add status effect processing
        # TODO: Update cooldowns and regeneration
        
        # Update animation timer
        self.animation_timer += 1
        if self.animation_timer >= 1 / self.animation_speed:
            if self.state in self.frames and self.frames[self.state]:
                self.current_frame = (self.current_frame + 1) % len(self.frames[self.state])
            self.animation_timer = 0
    
    def move(self, dx, dy, game_map=None):
        """
        Move the character if movement is valid.
        
        Args:
            dx (int): X-direction to move (-1, 0, 1).
            dy (int): Y-direction to move (-1, 0, 1).
            game_map: The game map for collision detection.
            
        Returns:
            bool: True if movement was successful, False otherwise.
        """
        # Store previous position
        old_x, old_y = self.x, self.y
        
        # Update position
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Update hitbox position
        self.hitbox.x = self.x + self.hitbox_offset_x
        self.hitbox.y = self.y + self.hitbox_offset_y
        
        # Check if new position is valid
        if game_map and not self._is_valid_position(game_map):
            # Revert to previous position if invalid
            self.x, self.y = old_x, old_y
            self.hitbox.x = self.x + self.hitbox_offset_x
            self.hitbox.y = self.y + self.hitbox_offset_y
            return False
        
        return True
    
    def _is_valid_position(self, game_map):
        """
        Check if the current position is valid.
        
        Args:
            game_map: The game map for collision detection.
            
        Returns:
            bool: True if the position is valid, False otherwise.
        """
        # Check corners and center of hitbox for collision
        points = [
            (self.hitbox.left, self.hitbox.top),
            (self.hitbox.right, self.hitbox.top),
            (self.hitbox.left, self.hitbox.bottom),
            (self.hitbox.right, self.hitbox.bottom),
            (self.hitbox.centerx, self.hitbox.centery)
        ]
        
        for px, py in points:
            # Convert to tile coordinates
            tile_x = px // TILE_SIZE
            tile_y = py // TILE_SIZE
            
            # Check if tile is a wall
            if hasattr(game_map, 'is_wall') and game_map.is_wall(tile_x, tile_y):
                return False
        
        return True
    
    def attack(self, target=None):
        """
        Perform an attack.
        
        Args:
            target: The target character to attack (optional).
            
        Returns:
            bool: True if attack was successful, False otherwise.
        """
        current_time = time.time()
        if current_time - self.last_attack_time < self.attack_cooldown:
            return False  # Still on cooldown
        
        # Update attack state
        self.state = "attack"
        self.current_frame = 0
        self.last_attack_time = current_time
        
        # TODO: Implement attack logic
        # TODO: Calculate damage based on stats and equipment
        # TODO: Apply status effects if applicable
        
        # If target is specified, deal damage
        if target and self._is_in_attack_range(target):
            target.take_damage(self.attack_damage)
            return True
        
        return False
    
    def take_damage(self, amount):
        """
        Take damage from an attack.
        
        Args:
            amount (int): Amount of damage to take.
            
        Returns:
            bool: True if character died from damage, False otherwise.
        """
        # TODO: Calculate actual damage based on defence and resistances
        actual_damage = max(1, amount - self.defence)
        self.health -= actual_damage
        
        if self.health <= 0:
            self.health = 0
            self.state = "death"
            self.current_frame = 0
            return True
        else:
            self.state = "hurt"
            self.current_frame = 0
            return False
    
    def heal(self, amount):
        """
        Heal the character.
        
        Args:
            amount (int): Amount of health to restore.
            
        Returns:
            int: Amount of health actually restored.
        """
        if self.health >= self.max_health:
            return 0
            
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old_health
    
    def is_alive(self):
        """
        Check if the character is alive.
        
        Returns:
            bool: True if alive, False if dead.
        """
        return self.health > 0
    
    def _is_in_attack_range(self, target):
        """
        Check if target is within attack range.
        
        Args:
            target: The target character.
            
        Returns:
            bool: True if in range, False otherwise.
        """
        # Calculate distance from character centre to target centre
        # Note: Using Pygame's centerx/centery properties but Australian English in variable names
        char_centre_x = self.hitbox.centerx
        char_centre_y = self.hitbox.centery
        target_centre_x = target.hitbox.centerx
        target_centre_y = target.hitbox.centery
        
        # Calculate distance
        dist = math.sqrt((char_centre_x - target_centre_x) ** 2 + 
                        (char_centre_y - target_centre_y) ** 2)
        
        # Check direction for melee attacks (facing matters)
        if self.attack_range < 100:  # Assume melee attack
            if self.facing_left and target_centre_x > char_centre_x:
                return False
            if not self.facing_left and target_centre_x < char_centre_x:
                return False
        
        return dist <= self.attack_range
    
    def draw(self, screen):
        """
        Draw the character with the current animation frame.
        
        Args:
            screen: The pygame surface to draw on.
        """
        # Only draw if we have frames for current state
        if self.state in self.frames and self.frames[self.state]:
            # Get current frame
            frame = self.frames[self.state][self.current_frame]
            
            # Flip if facing left
            if self.facing_left:
                frame = pygame.transform.flip(frame, True, False)
            
            # Draw the frame
            screen.blit(frame, (self.x, self.y))
        
        # Draw health bar if alive
        if self.health > 0:
            health_bar_width = self.hitbox.width
            health_bar_height = 5
            health_ratio = self.health / self.max_health
            
            # Position health bar above the hitbox
            health_bar_x = self.hitbox.x
            health_bar_y = self.hitbox.y - 10
            
            # Background
            pygame.draw.rect(screen, (100, 0, 0), 
                            (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            
            # Health
            pygame.draw.rect(screen, (0, 200, 0), 
                            (health_bar_x, health_bar_y, health_bar_width * health_ratio, health_bar_height))