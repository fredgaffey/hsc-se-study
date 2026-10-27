"""
Item module.

This module contains the Item class representing collectible items in the game.

TODO: Item Class Functionality
- Implement item rarity system (common, uncommon, rare, epic, legendary)
- Add item attribute/stat bonuses for equipment
- Support for different item types (weapon, armour, potion, scroll, key)
- Implement item tooltips/descriptions
- Add item durability/uses for consumables
- Support for item stacking in inventory
- Implement item visual effects when used
- Add equipping/unequipping functionality for equipment items
- Support for item sets that provide bonuses when complete
- Implement item level requirements
"""

import pygame
from core.game_object import GameObject

class Item(GameObject):
    """Represents a collectible item in the game."""
    
    def __init__(self, x, y, width, height, item_type, rarity, name, frames=None):
        """
        Initialise the item.
        
        Args:
            x (int): X-coordinate of the item.
            y (int): Y-coordinate of the item.
            width (int): Width of the item's hitbox.
            height (int): Height of the item's hitbox.
            item_type (str): Type of item (weapon, armour, potion, etc.).
            rarity (str): Rarity of the item (common, uncommon, rare, etc.).
            name (str): Name of the item.
            frames (list): List of animation frames for the item (optional).
        """
        super().__init__(x, y, width, height)
        
        # Item properties
        self.item_type = item_type
        self.rarity = rarity
        self.name = name
        self.description = ""
        self.value = 0
        
        # Visual representation
        self.frames = frames if frames else []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.2
        
        # State tracking
        self.collected = False
        self.used = False
        self.equipped = False
        
        # TODO: Implement item stats based on type/rarity
        # TODO: Add durability system for equipment
        # TODO: Configure item effects when used
        # TODO: Implement stacking logic for similar items
    
    def update(self):
        """Update the item's animation and state."""
        # Update hitbox position
        super().update()
        
        # Update animation if item has frames
        if self.frames and not self.collected:
            self.animation_timer += 1
            if self.animation_timer >= 1 / self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_timer = 0
        
        # TODO: Implement item-specific update logic
        # TODO: Update durability if item is currently in use
        # TODO: Handle cooldowns for usable items
    
    def collect(self):
        """
        Mark the item as collected and return its value.
        
        Returns:
            dict: Item properties to add to inventory.
        """
        if not self.collected:
            self.collected = True
            
            # TODO: Implement item collection logic
            # TODO: Return item properties for inventory
            return {"name": self.name, "type": self.item_type, "rarity": self.rarity}
        
        return None
    
    def use(self, player):
        """
        Use the item, applying its effects to the player.
        
        Args:
            player: The player object to apply effects to.
            
        Returns:
            bool: True if successfully used, False otherwise.
        """
        # TODO: Implement usage logic based on item type
        # TODO: Apply effects to player stats/health
        # TODO: Handle consumable items being used up
        # TODO: Trigger visual effects when item is used
        
        return False
    
    def draw(self, screen):
        """
        Draw the item with its current animation frame.
        
        Args:
            screen: The pygame surface to draw on.
        """
        if not self.collected and self.frames:
            # Draw current animation frame
            frame = self.frames[self.current_frame]
            screen.blit(frame, (self.x, self.y))
            
            # TODO: Add rarity-based glow effects
            # TODO: Implement hovering/floating animation
            # TODO: Add visual indicators for special items
            


class Weapon(Item):
    """Represents a weapon item that can be equipped."""
    
    def __init__(self, x, y, width, height, rarity, name, damage, frames=None):
        """
        Initialise a weapon item.
        
        Args:
            x (int): X-coordinate of the weapon.
            y (int): Y-coordinate of the weapon.
            width (int): Width of the weapon's hitbox.
            height (int): Height of the weapon's hitbox.
            rarity (str): Rarity of the weapon.
            name (str): Name of the weapon.
            damage (int): Base damage of the weapon.
            frames (list): Animation frames for the weapon (optional).
        """
        super().__init__(x, y, width, height, "weapon", rarity, name, frames)
        self.damage = damage
        
        # TODO: Implement weapon-specific properties
        # TODO: Add attack speed modifications
        # TODO: Implement special attack effects
        # TODO: Configure critical hit chances


class Potion(Item):
    """Represents a consumable potion item."""
    
    def __init__(self, x, y, width, height, rarity, name, effect_type, effect_amount, frames=None):
        """
        Initialise a potion item.
        
        Args:
            x (int): X-coordinate of the potion.
            y (int): Y-coordinate of the potion.
            width (int): Width of the potion's hitbox.
            height (int): Height of the potion's hitbox.
            rarity (str): Rarity of the potion.
            name (str): Name of the potion.
            effect_type (str): Type of effect (health, mana, strength, etc.).
            effect_amount (int): Amount of effect to apply.
            frames (list): Animation frames for the potion (optional).
        """
        super().__init__(x, y, width, height, "potion", rarity, name, frames)
        self.effect_type = effect_type
        self.effect_amount = effect_amount
        
        # TODO: Implement potion-specific properties
        # TODO: Add duration for effects (temporary vs. permanent)
        # TODO: Configure splash effects for area potions
        # TODO: Implement potion combining/crafting