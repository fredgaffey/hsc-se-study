"""
NPC module.

This module contains the NPC class representing non-player character in the game.

TODO: NPC Class Functionality
- Add support for different NPC types (Merchant, Quest Giver, Trainer)
- Implement dialog system with multiple messages/options
- Add quest giving/tracking capabilities
- Enable inventory for merchant NPCs to buy/sell items
- Support for NPC movement patterns (patrol routes)
- Implement NPC states (idle, talking, working, etc.)
- Add NPC reaction to player actions (friendship/hostility levels)
- Support for NPC schedules based on in-game time
"""

import pygame
import math
import time
from utils.constants import TILE_SIZE
from core.game_object import GameObject

class NPC(GameObject):
    """Represents a non-player character that can be interacted with."""
    
    def __init__(self, x, y, idle_frames):
        """
        Initialise the NPC.
        
        Args:
            x (int): X-coordinate of the NPC.
            y (int): Y-coordinate of the NPC.
            idle_frames (list): List of idle animation frames.
        """
        # Smaller hitbox similar to enemy and player
        hitbox_width = 25
        hitbox_height = 35
        super().__init__(x, y, hitbox_width, hitbox_height)
        
        # Use dimensions from idle frames for consistency
        self.width = idle_frames[0].get_width() if idle_frames else 90
        self.height = idle_frames[0].get_height() if idle_frames else 115
        
        # Animation frames
        self.idle_frames = idle_frames
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.2
        self.facing_left = False  # Priest will face right by default
        
        # Hitbox with offset similar to other characters
        self.hitbox_offset_x = 33
        self.hitbox_offset_y = 37
        self.hitbox = pygame.Rect(x + self.hitbox_offset_x, y + self.hitbox_offset_y, hitbox_width, hitbox_height)
        
        # Interaction state
        self.interacting = False
        self.interaction_cooldown = 1.0  # seconds
        self.last_interaction_time = 0
        self.interaction_range = 100  # pixels

        # shop inventory
        self.shop_inventory = {}
        
    def update(self, player=None):
        """
        Update the NPC's animation.
        
        Args:
            player: The player object for interaction.
        """
        # Update hitbox position
        self.hitbox.x = self.x + self.hitbox_offset_x
        self.hitbox.y = self.y + self.hitbox_offset_y
        
        # Check if we're facing the player
        if player:
            if player.hitbox.centerx < self.hitbox.centerx:
                self.facing_left = True
            else:
                self.facing_left = False
        
        # Update idle animation
        self.animation_timer += 1
        if self.animation_timer >= 1 / self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.animation_timer = 0
            
        # Reset interaction state after cooldown
        current_time = time.time()
        if self.interacting and current_time - self.last_interaction_time >= self.interaction_cooldown:
            self.interacting = False
    
    def is_player_in_range(self, player):
        """
        Check if player is within interaction range.
        
        Args:
            player: The player object.
            
        Returns:
            bool: True if the player is in range, False otherwise.
        """
        # Calculate distance from NPC centre to player centre
        # Note: we're using pygame's centerx/centery properties but using Australian spelling in our variable names
        npc_centre_x = self.hitbox.centerx
        npc_centre_y = self.hitbox.centery
        player_centre_x = player.hitbox.centerx
        player_centre_y = player.hitbox.centery
        
        # Calculate distance
        dist = math.sqrt((npc_centre_x - player_centre_x) ** 2 + 
                         (npc_centre_y - player_centre_y) ** 2)
        
        # Check if player is within range
        return dist <= self.interaction_range
    
    def interact(self, player=None):
        """
        Interact with the NPC.
        
        Args:
            player: The player object.
            
        Returns:
            bool: True if interaction was successful, False otherwise.
        """
        current_time = time.time()
        cooldown_elapsed = current_time - self.last_interaction_time >= self.interaction_cooldown
        
        if cooldown_elapsed and not self.interacting:
            self.interacting = True
            self.last_interaction_time = current_time
            return True
        
        return False
    
    def draw(self, screen):
        """
        Draw the NPC with the current animation frame.
        
        Args:
            screen: The pygame surface to draw on.
        """
        # Get the current frame
        frame = self.idle_frames[self.current_frame]
        
        # Flip the frame if facing left
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
        
        # Draw the frame
        screen.blit(frame, (self.x, self.y))
    
    def draw_interaction_box(self, screen):
        """
        Draw the black interaction box when interacting.
        
        Args:
            screen: The pygame surface to draw on.
        """
        if self.interacting:
            # Calculate box dimensions relative to screen size for better responsiveness
            box_width = min(300, screen.get_width() - 40)  # No wider than screen - 40px
            box_height = 100
            
            # Center the box horizontally and position near bottom of screen
            box_x = (screen.get_width() - box_width) // 2
            box_y = screen.get_height() - box_height - 50
            
            # Create the dialog box with a semi-transparent background
            dialog_box = pygame.Rect(box_x, box_y, box_width, box_height)
            
            # Draw box with a slightly transparent dark background
            box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            box_surface.fill((0, 0, 0, 220))  # Black with 220/255 alpha
            screen.blit(box_surface, (box_x, box_y))
            
            # Add a white border for definition
            pygame.draw.rect(screen, (255, 255, 255), dialog_box, 2)
            
    
    def shop(self, player):
        """

        """
        
        # npc shop items and prices
        # cost items
        
        self.shop_inventory = {
            "potion": 20,
            "gold_multiplier": 50,
            "weapon_damage_increase": 50
        } 
        
        