"""
UI module.

This module contains the UI class for rendering game user interface elements.
"""

import pygame
import time
import math
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW
from characters.player import Player



class UI:
    """Handles game user interface rendering."""
    
    def __init__(self):
        """Initialise the UI."""
        self.font = pygame.font.SysFont(None, 24)
        self.message = ""
        self.message_timer = 0
        self.message_duration = 3.0  # seconds
    
    def set_message(self, message):
        """
        Set a temporary message to display.
        
        Args:
            message (str): The message to display.
        """
        self.message = message
        self.message_timer = time.time()
    
    def draw(self, screen, player, inventory, score, enemy=None, level_num=1):
        """
        Draw the game UI.
        
        Args:
            screen: The pygame surface to draw on.
            player: The player object.
            inventory (dict): Player's inventory.
            score (int): Current game score.
            enemy: Optional enemy object for targeting information.
            level_num (int): Current level number.
        """
        # Health text
        health_text = self.font.render(f"Health: {round(player.health)}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (10, 10))
        
        # Level and score
        level_text = self.font.render(f"Level: {level_num}", True, WHITE)
        screen.blit(level_text, (10, 40))
        
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 70))
        
        # Inventory
        inventory_text = self.font.render(f"Gold: {inventory['gold']} | Health Potions: {inventory['health_potions']}", True, WHITE)
        screen.blit(inventory_text, (10, 100))
        
        # Buff Potions Display
        self.draw_buff_potions(screen, player)
        
        # Show message if active
        if self.message and time.time() - self.message_timer < self.message_duration:
            # Create a semi-transparent background
            message_bg = pygame.Surface((len(self.message) * 10, 30), pygame.SRCALPHA)
            message_bg.fill((0, 0, 0, 150))
            screen.blit(message_bg, (SCREEN_WIDTH//2 - len(self.message)*5, SCREEN_HEIGHT - 100))
            
            # Draw message
            message_surf = self.font.render(self.message, True, YELLOW)
            screen.blit(message_surf, (SCREEN_WIDTH//2 - message_surf.get_width()//2, SCREEN_HEIGHT - 95))
        
        # Draw instructions
        self.draw_instructions(screen)
    
    def draw_buff_potions(self, screen, player):
        """
        Draw buff potion inventory and active buffs.
        
        Args:
            screen: The pygame surface to draw on.
            player: The player object with inventory.
        """
        # Get potion counts
        inventory_counts = player.player_inventory.display_contents_count()
        
        # Display available buff potions
        y_offset = 130
        buff_title = self.font.render("Buff Potions:", True, WHITE)
        screen.blit(buff_title, (10, y_offset))
        
        potion_display = [
            ("1: Resistance", inventory_counts.get("resistance_potion", 0)),
            ("2: Speed", inventory_counts.get("speed_potion", 0)),
            ("3: Gold", inventory_counts.get("gold_potion", 0)),
            ("4: Damage", inventory_counts.get("damage_potion", 0))]
        
        for i, (name, count) in enumerate(potion_display):
            y_pos = y_offset + 25 + (i * 20)
            color = WHITE if count > 0 else (100, 100, 100)  # Grey out if none available
            potion_text = self.font.render(f"{name}: {count}", True, color)
            screen.blit(potion_text, (10, y_pos))
        
        # Display active buffs
        self.draw_active_buffs(screen, player)
    
    def draw_active_buffs(self, screen, player):
        """
        Draw currently active buff effects.
        
        Args:
            screen: The pygame surface to draw on.
            player: The player object with active buffs.
        """
        buffs = player.player_inventory.get_active_potion_and_buf()
        active_buffs = []
        
        # Check which buffs are active (not equal to 1.0)
        if buffs["rBuf"] != 1.0:
            active_buffs.append(f"Resistance: {buffs['rBuf']:.1f}x")
        if buffs["sBuf"] != 1.0:
            active_buffs.append(f"Speed: {buffs['sBuf']:.1f}x")
        if buffs["gBuf"] != 1.0:
            active_buffs.append(f"Gold: {buffs['gBuf']:.1f}x")
        if buffs["dBuf"] != 1.0:
            active_buffs.append(f"Damage: {buffs['dBuf']:.1f}x")
        
        if active_buffs:
            # Display active buffs in top right corner
            x_start = SCREEN_WIDTH - 150
            y_start = 200 # lower display text
            
            active_title = self.font.render("Active Buffs:", True, YELLOW)
            screen.blit(active_title, (x_start, y_start))
            
            for i, buff_text in enumerate(active_buffs):
                y_pos = y_start + 25 + (i * 20)
                buff_surface = self.font.render(buff_text, True, YELLOW)
                screen.blit(buff_surface, (x_start, y_pos))
    
    def draw_instructions(self, screen):
        """
        Draw game instructions.
        
        Args:
            screen: The pygame surface to draw on.
        """
        instructions = [
            "Controls:",
            "WASD/Arrows: Move",
            "SPACE: Attack",
            "E: Open Chests",
            "H: Use Health Potion",
            "1-4: Buff Potions",
            "Shift: Disable speed buff",
            "ESC: Quit"
        ]
        
        for i, line in enumerate(instructions):
            text = self.font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - 150, 10 + i * 20))
    
    def draw_debug_info(self, screen, player, enemy=None):
        """
        Draw debug information.
        
        This method has been removed for production.
        
        Args:
            screen: The pygame surface to draw on.
            player: The player object.
            enemy: Optional enemy object.
        """
        # Debug visualization removed for production
        pass