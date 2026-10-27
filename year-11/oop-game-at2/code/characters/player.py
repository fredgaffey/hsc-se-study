"""
Player module.

This module contains the Player class representing the player character.
"""

import pygame
import time
import math
from utils.constants import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, MAPS
from core.game_object import GameObject
from characters.inventory import Inventory_manager,Potions



class Player(GameObject):
    """Represents the player character."""

    
    def __init__(self, x, y, idle_frames, attack_frames):
        """
        Initialise the player.
        
        Args:
            x (int): X-coordinate of the player.
            y (int): Y-coordinate of the player.
            idle_frames (list): List of idle animation frames.
            attack_frames (list): List of attack animation frames.
        """
        # Use a smaller hitbox to allow movement through narrow passages
        hitbox_width = 25  # Reduced from 30
        hitbox_height = 25  # Reduced from 40
        super().__init__(x, y, hitbox_width, hitbox_height)
        
        # Animation frames
        self.idle_frames = idle_frames
        self.attack_frames = attack_frames
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15  # Lower is faster
        self.state = "idle"  # Can be "idle" or "attack"
        self.direction = "right"  # Can be "left" or "right"
        self.attacking = False
        self.attack_start_time = 0
        
        # Health
        self.max_health = 100
        self.health = 100
        
        # Create hitbox with offset from sprite position
        # Adjust hitbox position to be centered on the visible character within the sprite
        # The Knight sprite has empty space around it - actual character is more centered
        # Sprite size is 100x125, but the character's body is positioned more in the middle
        self.hitbox_offset_x = 38  # Adjusted to center the narrower hitbox
        self.hitbox_offset_y = 15  # Shifted up significantly to better match sprite (original: 42)
        self.hitbox = pygame.Rect(x + self.hitbox_offset_x, y + self.hitbox_offset_y, hitbox_width, hitbox_height)
        self.speed = 4
        
        # For attack animation
        self.facing_left = False
        
        # Combat
        self.base_attack_damage = 20
        self.attack_range = 100  # Pixels
        self.attack_cooldown = 0.5  # Seconds
        self.last_attack_time = 0
        
        # inventory
        self.player_inventory = Inventory_manager()  
        
        # Add individual potion instances to inventory (3 of each type)
        # Define the pots that can be brought
        self.rPot = Potions(10,"resistance_potion",5,rBuf=2,key='1')
        self.sPot = Potions(10,"speed_potion",10,sBuf=2.0,key='2')    
        self.gPot = Potions(10,"gold_potion",10,gBuf=2,key='3') 
        self.dPot = Potions(10,"damage_potion",5,dBuf=2,key='4') 
        self.pot_arr = [self.rPot,self.sPot,self.gPot,self.dPot]
        # for _ in range(4):
        #     self.player_inventory.add_item(self.rPot)
        #     self.player_inventory.add_item(self.sPot)
        #     self.player_inventory.add_item(self.gPot)
        #     self.player_inventory.add_item(self.dPot)
  
        
            

            
        
                                   
    def update(self, game_map, enemy=None):
        """
        Update the player position and animation.
        
        Args:
            game_map (list): The game map data.
            enemy: Optional enemy object to check for attacking (no longer used directly).
        """
        # Store reference to game map for enemies to use in collision detection
        self.game_map = game_map
        
        keys = pygame.key.get_pressed()
        current_time = time.time()
        
        # Only process movement if not attacking
        if not self.attacking:
            # Store previous position
            old_x, old_y = self.x, self.y
            
            # Get current speed with buff multiplier
            current_speed = self.speed 
            
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]: # to fix the stop before wall 
                current_speed = self.speed * self.player_inventory.get_active_potion_and_buf()["sBuf"]
            
            # Handle movement
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x -= current_speed
                self.direction = "left"
                self.facing_left = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x += current_speed
                self.direction = "right"
                self.facing_left = False
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.y -= current_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.y += current_speed
                            
            # check pot uesd via key press           
            key_mapping = {
                    '1': pygame.K_1, '2': pygame.K_2, '3': pygame.K_3, '4': pygame.K_4,
                    '5': pygame.K_5, '6': pygame.K_6, '7': pygame.K_7, '8': pygame.K_8, '9': pygame.K_9}
            
            events = pygame.event.get()
            keys_press = pygame.key.get_pressed()
            potion_triggered = False
            if time.time() - self.player_inventory.item_last_used >= 0.5: # cool down time for player_inventory  
                if not self.player_inventory.enable_buy:
                    for i in self.player_inventory.inventory: 
                        key = str(i.key)
                        if key in key_mapping and keys[key_mapping[key]]:  
                            self.player_inventory.activate(i)
                            # Show potion activation message
                            if hasattr(self, 'game') and self.game:
                                self.game.ui.set_message(f"Activated {i.display_name}!")
                            break  # Only activate one potion per frame
                                            
            # These must be restored if the new position is invalid
            self.hitbox.x = self.x + self.hitbox_offset_x
            self.hitbox.y = self.y + self.hitbox_offset_y
            
            # Check collision and revert if needed
            if not self._is_valid_position(game_map):
                self.x, self.y = old_x, old_y
                self.hitbox.x = self.x + self.hitbox_offset_x
                self.hitbox.y = self.y + self.hitbox_offset_y                
        
        # Check for attack
        # Check attack conditions
        attack_key_pressed = keys[pygame.K_SPACE]
        cooldown_elapsed = current_time - self.last_attack_time
        can_attack = cooldown_elapsed >= self.attack_cooldown
        
        if attack_key_pressed and not self.attacking and can_attack:
            # Player is pressing space, not already attacking, and cooldown has elapsed
            self.state = "attack"
            self.attacking = True
            self.attack_start_time = current_time
            self.last_attack_time = current_time
            self.current_frame = 0
            
            # Note: enemy damage is now handled in the game loop to allow attacking any enemy
        
        # Update animation
        self.animation_timer += 1
        
        if self.state == "idle":
            # Continue idle animation
            if self.animation_timer >= 1 / self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                self.animation_timer = 0
        elif self.state == "attack":
            # Attack animation plays at a fixed rate
            frames_per_second = 6  # Slowed down for better visualisation of attack animations
            elapsed = current_time - self.attack_start_time
            new_frame = min(int(elapsed * frames_per_second), len(self.attack_frames) - 1)
            
            # Update the frame if it changed
            if new_frame != self.current_frame:
                self.current_frame = new_frame
            
            # If we've reached the last frame, go back to idle
            if self.current_frame >= len(self.attack_frames) - 1:
                # Finish animation and reset to idle state
                self.state = "idle"
                self.attacking = False
                self.current_frame = 0
                
                # Make sure any custom attributes are removed when animation ends
                if hasattr(self, '_attacked_this_animation'):
                    delattr(self, '_attacked_this_animation')
                    
    def buy_pot(self,amount_of_gold_have):
        amount_of_gold_have = int(amount_of_gold_have)
        # check pot uesd via key press           
        key_mapping = {
                '1': pygame.K_1, '2': pygame.K_2, '3': pygame.K_3, '4': pygame.K_4,
                '5': pygame.K_5, '6': pygame.K_6, '7': pygame.K_7, '8': pygame.K_8, '9': pygame.K_9}
        keys = pygame.key.get_pressed()

        if self.player_inventory.enable_buy and time.time() - self.player_inventory.item_last_added >= 0.5:
            for i in self.pot_arr: 
                key = str(i.key)
                if keys[key_mapping[key]]:
                    if amount_of_gold_have >= i.cost:
                        self.player_inventory.add_to_inventory_with_time_safe(i)
                        print(i.cost)
                        # Show potion activation message
                        if hasattr(self, 'game') and self.game:
                            self.game.ui.set_message(f"Bought {i.display_name}!")
                            return i.cost
                        return i.cost
                    # Show potion activation message
                    if hasattr(self, 'game') and self.game:
                        self.game.ui.set_message(f"You don't have enough gold to by {i.display_name} it cost's {i.cost}!")
                    return 0
        return 0 
    
    def _is_valid_position(self, game_map):
        """
        Check if the current position is valid.
        
        Args:
            game_map (list): The game map data.
            
        Returns:
            bool: True if the position is valid, False otherwise.
        """
        # Use fewer points for more permissive collision to fit through narrow gaps
        # Focus on the corners and centre for essential collision checks
        points = [
            # Corners
            (self.hitbox.left, self.hitbox.top),
            (self.hitbox.right, self.hitbox.top),
            (self.hitbox.left, self.hitbox.bottom),
            (self.hitbox.right, self.hitbox.bottom),
            # Center
            (self.hitbox.centerx, self.hitbox.centery)
        ]
        
        for px, py in points:
            # Convert to tile coordinates
            tile_x = px // TILE_SIZE
            tile_y = py // TILE_SIZE
            
            # Check if tile is a wall using the map's is_wall method if available
            if hasattr(game_map, 'is_wall'):
                if game_map.is_wall(tile_x, tile_y):
                    return False
            # Fallback to the old behavior
            elif (tile_x < 0 or tile_x >= MAP_WIDTH or 
                tile_y < 0 or tile_y >= MAP_HEIGHT):
                # We can't check MAPS here since we don't know which level
                # This will be handled by the is_wall check anyway
                return False
        
        return True
    
    @property
    def attack_damage(self):
        """Get current attack damage with buff multipliers applied."""
        print(self.base_attack_damage * self.player_inventory.get_active_potion_and_buf()["dBuf"])
        return self.base_attack_damage * self.player_inventory.get_active_potion_and_buf()["dBuf"]
    
    def _is_in_attack_range(self, enemy):
        """
        Check if an enemy is within attack range.
        
        Args:
            enemy: The enemy object to check.
            
        Returns:
            bool: True if the enemy is in attack range, False otherwise.
        """
        # Calculate distance from player center to enemy center
        player_center_x = self.hitbox.centerx
        player_center_y = self.hitbox.centery
        enemy_center_x = enemy.hitbox.centerx
        enemy_center_y = enemy.hitbox.centery
        
        # Calculate distance
        dist = math.sqrt((player_center_x - enemy_center_x) ** 2 + 
                         (player_center_y - enemy_center_y) ** 2)
        
        # Check direction - can only attack in the direction facing
        if self.facing_left and enemy_center_x > player_center_x:
            return False
        if not self.facing_left and enemy_center_x < player_center_x:
            return False
        
        in_range = dist <= self.attack_range
        
        return in_range
    
    def draw(self, screen):
        """
        Draw the player with the current animation frame.
        
        Args:
            screen: The pygame surface to draw on.
        """
        # Get the current frame based on state
        if self.state == "idle":
            frame = self.idle_frames[self.current_frame]
        else:  # attack
            frame = self.attack_frames[self.current_frame]
            # Use attack frame
        
        # Flip the frame if facing left
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
        
        # Calculate center point of hitbox (this is the player's "true" position)
        center_x = self.hitbox.centerx
        center_y = self.hitbox.centery
        
        # We want to render the frame centered on the player's hitbox
        # Subtract half the frame dimensions to center it
        render_x = center_x - frame.get_width() // 2
        render_y = center_y - frame.get_height() // 2
        
        # Add a vertical adjustment to make it look better (hitbox is now positioned higher)
        # This moves the frame up, accounting for the adjusted hitbox position
        vertical_adjust = 1
        render_y -= vertical_adjust
        
        # Draw the frame (centered on hitbox)
        screen.blit(frame, (render_x, render_y))
        
        
        # Draw health bar above the hitbox
        health_bar_width = 25  # Match hitbox width
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
    
        pygame.draw.rect(screen,(0,0,0),self.hitbox,2)
        
        
    
    def take_damage(self, amount):
        """
        Take damage.
        
        Args:
            amount (int): The amount of damage to take.
            
        Returns:
            bool: True if the player died, False otherwise.
        """

        
        self.health -= amount / self.player_inventory.get_active_potion_and_buf()["rBuf"]
        if self.health < 0:
            self.health = 0
        return self.health <= 0
    
    def is_alive(self):
        """
        Check if player is alive.
        
        Returns:
            bool: True if the player is alive, False otherwise.
        """
        return self.health > 0
        
    def teleport(self, x, y):
        """
        Teleport the player to a new position.
        
        Args:
            x (int): The new x coordinate.
            y (int): The new y coordinate.
        """
        self.x = x
        self.y = y
        self.hitbox.x = x + self.hitbox_offset_x
        self.hitbox.y = y + self.hitbox_offset_y
        