"""
Character Select module.

This module contains the CharacterSelect class for handling the character selection screen.
"""

import pygame
import math
import time
import random
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLUE, PURPLE

class CharacterSelect:
    """Manages the character selection screen."""
    
    def __init__(self, screen, asset_loader):
        """
        Initialise the character selection screen.
        
        Args:
            screen: The pygame surface to draw on.
            asset_loader: The asset loader instance.
        """
        self.screen = screen
        self.asset_loader = asset_loader
        
        # Fonts with carefully calibrated sizes for proper fit
        self.font_large = pygame.font.Font(None, 64)  # Header font
        self.font_medium = pygame.font.Font(None, 36) # Character names and button text
        self.font_small = pygame.font.Font(None, 24)  # Stats text - smaller to fit within card
        
        # Load or create background
        self.background = self._create_background()
        
        # Character options - with precise dimensions and spacing for perfect alignment
        # Calculate card dimensions and spacing for optimal layout
        card_width = 200  # Width for character cards
        card_height = 260  # Reduced height to ensure no vertical overflow
        card_spacing = 100  # Horizontal spacing between cards
        
        # Calculate vertical position to ensure cards are properly centered in upper portion
        # This ensures enough space for info panel and button below
        vertical_space_needed = card_height + 180  # Height for cards + space needed below
        card_y = (SCREEN_HEIGHT - vertical_space_needed) // 2
        
        # Calculate x positions for centered layout
        total_width = (card_width * 2) + card_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        self.characters = [
            {
                "name": "Knight",
                "type": "knight",
                "description": "Strong melee fighter with high health",
                "stats": {
                    "health": 100,
                    "damage": 20,
                    "speed": 4, 
                    "range": "Short"
                },
                "special": "Shield Block",  # Added special ability for more character info
                "frames": asset_loader.get_player_idle_frames("knight"),
                "color": BLUE,
                "rect": pygame.Rect(start_x, card_y, card_width, card_height)
            },
            {
                "name": "Wizard",
                "type": "wizard",
                "description": "Magic user with ranged attacks",
                "stats": {
                    "health": 80,
                    "damage": 15,
                    "speed": 3,
                    "range": "Long"
                },
                "special": "Magic Projectiles",  # Added special ability for more character info
                "frames": asset_loader.get_player_idle_frames("wizard"),
                "color": PURPLE,
                "rect": pygame.Rect(start_x + card_width + card_spacing, card_y, card_width, card_height)
            }
        ]
        
        # Selection state
        self.selected_character = 0
        self.animation_frame = 0
        self.animation_timer = 0
        # Initial position for confirm button - will be properly positioned in draw method
        self.confirm_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 150, 160, 38)
        self.button_highlighted = False
        self.pulse_timer = 0
        
    def update(self, dt):
        """
        Update character selection animations.
        
        Args:
            dt: Time delta in seconds.
        """
        # Update character animation
        self.animation_timer += dt
        if self.animation_timer >= 0.15:  # Frame rate for character idle animation
            self.animation_frame = (self.animation_frame + 1) % len(self.characters[self.selected_character]["frames"])
            self.animation_timer = 0
            
        # Update pulse effect for selected character
        self.pulse_timer += dt * 3  # Speed of pulse
        
    def _create_background(self):
        """Create a stylish background for the character selection screen."""
        import os
        
        # Create a gradient stone-like background surface
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Draw a gradient from dark gray to deeper gray for stone/dungeon effect
        for y in range(SCREEN_HEIGHT):
            # Calculate the color for this row
            ratio = y / SCREEN_HEIGHT
            r = int(40 + 20 * (1 - ratio))
            g = int(40 + 20 * (1 - ratio))
            b = int(50 + 20 * (1 - ratio))
            color = (r, g, b)
            
            # Draw a horizontal line with this color
            pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))
        
        # Add a "stone texture" pattern
        for i in range(200):  # Increased number of stones for more texture
            # Random stone positions
            stone_x = random.randint(0, SCREEN_WIDTH)
            stone_y = random.randint(0, SCREEN_HEIGHT)
            stone_size = random.randint(5, 25)  # Slightly larger stones for more visible texture
            
            # Stone color (slight variation)
            stone_color = (
                random.randint(45, 75),
                random.randint(45, 75),
                random.randint(55, 85)
            )
            
            # Draw stone
            pygame.draw.rect(
                background, 
                stone_color, 
                (stone_x, stone_y, stone_size, stone_size),
                border_radius=stone_size // 3
            )
            
            # Add highlights to some stones for more dimension
            if random.random() > 0.7:  # 30% of stones get highlights
                highlight_color = (
                    min(255, stone_color[0] + 15),
                    min(255, stone_color[1] + 15),
                    min(255, stone_color[2] + 15)
                )
                pygame.draw.rect(
                    background,
                    highlight_color,
                    (stone_x, stone_y, stone_size // 2, stone_size // 2),
                    border_radius=stone_size // 6
                )
        
        # Add some design elements to make it look dungeon-like
        # Torch-like yellow-orange glow in corners
        for corner in [(50, 50), (SCREEN_WIDTH - 50, 50), 
                       (50, SCREEN_HEIGHT - 50), (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)]:
            # Create glow effect surfaces with alpha
            glow_size = 150
            glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            
            # Draw multiple circles for gradient effect
            pygame.draw.circle(glow, (100, 70, 0, 30), (glow_size//2, glow_size//2), glow_size//2)
            pygame.draw.circle(glow, (150, 100, 0, 20), (glow_size//2, glow_size//2), glow_size//3)
            pygame.draw.circle(glow, (200, 150, 0, 10), (glow_size//2, glow_size//2), glow_size//4)
            
            # Blit the glow onto the background
            background.blit(glow, (corner[0] - glow_size//2, corner[1] - glow_size//2))
            
        # Create tile pattern along the borders
        tile_size = 20
        border_width = 3
        
        # Top and bottom borders
        for x in range(0, SCREEN_WIDTH, tile_size):
            # Top border
            pygame.draw.rect(background, (60, 60, 70), 
                           (x, 0, tile_size, tile_size), border_width)
            
            # Bottom border
            pygame.draw.rect(background, (60, 60, 70), 
                           (x, SCREEN_HEIGHT - tile_size, tile_size, tile_size), border_width)
        
        # Left and right borders
        for y in range(0, SCREEN_HEIGHT, tile_size):
            # Left border
            pygame.draw.rect(background, (60, 60, 70), 
                           (0, y, tile_size, tile_size), border_width)
            
            # Right border
            pygame.draw.rect(background, (60, 60, 70), 
                           (SCREEN_WIDTH - tile_size, y, tile_size, tile_size), border_width)
            
        # Add a darker semi-transparent overlay to make text more readable
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))  # More opaque black for better contrast
        background.blit(overlay, (0, 0))
        
        return background
        
    def handle_events(self):
        """
        Handle pygame events for the character selection screen.
        
        Returns:
            dict or None: Selected character data if confirmed, None otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.selected_character = max(0, self.selected_character - 1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.selected_character = min(len(self.characters) - 1, self.selected_character + 1)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return self.characters[self.selected_character]
            
            elif event.type == pygame.MOUSEMOTION:
                # Check if mouse is over a character
                mouse_pos = pygame.mouse.get_pos()
                for i, character in enumerate(self.characters):
                    if character["rect"].collidepoint(mouse_pos):
                        self.selected_character = i
                
                # Check if mouse is over confirm button
                self.button_highlighted = self.confirm_button_rect.collidepoint(mouse_pos)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if confirm button was clicked
                if self.confirm_button_rect.collidepoint(mouse_pos):
                    # Visual feedback for button click
                    pygame.draw.rect(self.screen, (255, 255, 255), self.confirm_button_rect, border_radius=10)
                    pygame.display.flip()  # Show the white flash
                    pygame.time.delay(100)  # Brief delay for visual feedback
                    return self.characters[self.selected_character]
                
                # Check if a character was clicked
                for i, character in enumerate(self.characters):
                    if character["rect"].collidepoint(mouse_pos):
                        if self.selected_character == i:  # Double-click on already selected character
                            # If it's already selected, clicking again is like hitting confirm
                            return self.characters[self.selected_character]
                        else:
                            self.selected_character = i  # Just select this character
        
        return None
        
    def draw(self):
        """Draw the character selection screen."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw header text with background for better visibility
        header_text = self.font_large.render("Select Your Character", True, WHITE)
        header_rect = header_text.get_rect(center=(SCREEN_WIDTH//2, 60))  # Higher position
        
        # Create a background for header text
        header_bg_rect = header_rect.inflate(40, 20)  # Make background larger than text
        header_bg = pygame.Surface((header_bg_rect.width, header_bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(header_bg, (0, 0, 0, 180), (0, 0, header_bg_rect.width, header_bg_rect.height), border_radius=10)
        self.screen.blit(header_bg, header_bg_rect.topleft)
        
        # Draw decorative line under header
        line_y = header_rect.bottom + 5
        line_width = SCREEN_WIDTH // 2
        pygame.draw.line(self.screen, (200, 200, 200, 150), 
                      (SCREEN_WIDTH//2 - line_width//2, line_y), 
                      (SCREEN_WIDTH//2 + line_width//2, line_y), 
                      2)
        
        self.screen.blit(header_text, header_rect)
        
        # Draw character options
        for i, character in enumerate(self.characters):
            # Draw character card
            card_color = character["color"]
            # Highlight selected character with pulsing effect
            if i == self.selected_character:
                # Calculate pulse effect - intensity changes over time
                pulse = (math.sin(self.pulse_timer) * 0.2) + 0.8
                # Apply to RGB components separately to maintain color hue
                r = min(255, int(card_color[0] * pulse) + 30)
                g = min(255, int(card_color[1] * pulse) + 30)
                b = min(255, int(card_color[2] * pulse) + 30)
                card_color = (r, g, b)
                # Thicker border for selected
                border_width = 3
            else:
                border_width = 1
                
            # Draw character card background with better contrast
            # First draw a solid background
            pygame.draw.rect(self.screen, (20, 20, 30), character["rect"], border_radius=10)
            # Then draw a colored border
            pygame.draw.rect(self.screen, card_color, character["rect"], border_width + 2, border_radius=10)
            # Finally, draw white outline for emphasis
            pygame.draw.rect(self.screen, WHITE, character["rect"], border_width, border_radius=10)
            
            # Draw character name with title banner
            # Create title banner (reduced height)
            title_rect = pygame.Rect(
                character["rect"].left, 
                character["rect"].top + 12, 
                character["rect"].width, 
                40  # Reduced height for better spacing
            )
            
            # Draw title background
            title_bg = pygame.Surface((title_rect.width, title_rect.height), pygame.SRCALPHA)
            title_color = tuple(list(card_color[:3]) + [220])  # Color with alpha
            pygame.draw.rect(title_bg, title_color, (0, 0, title_rect.width, title_rect.height), border_radius=8)
            self.screen.blit(title_bg, title_rect.topleft)
            
            # Draw character name
            name_text = self.font_medium.render(character["name"], True, WHITE)
            name_rect = name_text.get_rect(center=(character["rect"].centerx, title_rect.centery))
            self.screen.blit(name_text, name_rect)
            
            # Draw character sprite
            if i == self.selected_character:
                # Use animation for selected character
                frame = character["frames"][self.animation_frame]
            else:
                # Use first frame for non-selected characters
                frame = character["frames"][0]
                
            # Create a more compact character sprite display area
            sprite_area_width = 100  # Reduced width
            sprite_area_height = 100 # Reduced height
            
            # Calculate how much height we need to reserve for the stats panel
            stats_height_needed = 100  # Estimate of stats panel height plus padding
            
            # Position sprite area to leave enough room for stats panel
            sprite_area_top = character["rect"].top + 55
            
            sprite_area_rect = pygame.Rect(
                character["rect"].centerx - sprite_area_width//2,
                sprite_area_top,
                sprite_area_width,
                sprite_area_height
            )
            
            # Create circular background for character
            sprite_bg = pygame.Surface((sprite_area_width, sprite_area_height), pygame.SRCALPHA)
            pygame.draw.ellipse(sprite_bg, (50, 50, 70, 150), (0, 0, sprite_area_width, sprite_area_height))
            self.screen.blit(sprite_bg, sprite_area_rect.topleft)
            
            # Add subtle glow effect for selected character (reduced size)
            if i == self.selected_character:
                glow_radius = sprite_area_width // 2 + 5  # Smaller glow radius
                glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
                glow_color = tuple(list(card_color[:3]) + [80])  # Character color with alpha (more subtle)
                
                # Create circular gradient (fewer iterations for performance)
                for rad in range(glow_radius, 0, -3):  # Larger step for fewer iterations
                    alpha = 80 - (rad * 70 // glow_radius)  # Lower maximum alpha
                    if alpha > 0:
                        pygame.draw.circle(glow_surface, (glow_color[0], glow_color[1], glow_color[2], alpha), 
                                        (glow_radius, glow_radius), rad)
                
                glow_pos = (sprite_area_rect.centerx - glow_radius, sprite_area_rect.centery - glow_radius)
                self.screen.blit(glow_surface, glow_pos, special_flags=pygame.BLEND_ALPHA_SDL2)
            
            # Scale character sprite to fit properly within the smaller display area
            scaled_frame = pygame.transform.scale(frame, (80, 95))
            frame_rect = scaled_frame.get_rect(center=sprite_area_rect.center)
            self.screen.blit(scaled_frame, frame_rect)
            
            # Create a highly compact stats panel that fits perfectly within the card
            stats_panel_width = character["rect"].width - 24  # More margin for better containment
            stats_panel_height = 85  # Smaller height to ensure it fits in the card
            
            # Calculate remaining space in the card and position accordingly
            remaining_vertical_space = character["rect"].bottom - sprite_area_rect.bottom
            stats_panel_top = sprite_area_rect.bottom + 5  # Less spacing above panel
            
            # Create panel rect ensuring it stays within card bounds
            stats_panel_rect = pygame.Rect(
                character["rect"].centerx - stats_panel_width//2,
                stats_panel_top,
                stats_panel_width,
                min(stats_panel_height, character["rect"].bottom - stats_panel_top - 5)  # Ensure it stays within card
            )
            
            # Draw stats panel background
            stats_bg = pygame.Surface((stats_panel_width, stats_panel_height), pygame.SRCALPHA)
            pygame.draw.rect(stats_bg, (30, 30, 50, 180), (0, 0, stats_panel_width, stats_panel_height), border_radius=8)
            self.screen.blit(stats_bg, stats_panel_rect.topleft)
            
            # Draw stats title - smaller and more compact
            title_font = pygame.font.Font(None, 22)  # Tiny font for consistency
            stats_title = title_font.render("Character Stats", True, WHITE)
            stats_title_rect = stats_title.get_rect(center=(stats_panel_rect.centerx, stats_panel_rect.top + 8))
            self.screen.blit(stats_title, stats_title_rect)
            
            # Draw stats with more compact visual bars
            bar_width = 60  # Even smaller bar width
            bar_height = 6  # Smaller bar height for better fit
            stats_y = stats_panel_rect.top + 20  # Start stats higher due to smaller title font
            
            # Define max values for stats to scale bars
            max_stats = {"health": 100, "damage": 25, "speed": 5}
            
            # Draw each stat (except range which gets special treatment)
            for stat_name, stat_value in character["stats"].items():
                if stat_name != "range":  # Handle range separately
                    # Create text label with less left padding - using tiny font
                    # Create tiny font for consistency
                    tiny_font = pygame.font.Font(None, 22)  # Smaller font for stat labels
                    stat_label = tiny_font.render(f"{stat_name.capitalize()}:", True, WHITE)
                    label_rect = stat_label.get_rect(left=stats_panel_rect.left + 10, centery=stats_y)
                    self.screen.blit(stat_label, label_rect)
                    
                    # Draw the bar background with less spacing between label and bar
                    bar_bg_rect = pygame.Rect(label_rect.right + 5, stats_y - bar_height//2, bar_width, bar_height)
                    pygame.draw.rect(self.screen, (70, 70, 70), bar_bg_rect, border_radius=3)  # Smaller corner radius
                    
                    # Draw the filled portion of the bar
                    if stat_name in max_stats and max_stats[stat_name] > 0:
                        fill_width = int(bar_width * (stat_value / max_stats[stat_name]))
                        fill_rect = pygame.Rect(bar_bg_rect.left, bar_bg_rect.top, fill_width, bar_height)
                        
                        # Choose color based on stat (health=green, damage=red, speed=blue)
                        if stat_name == "health":
                            fill_color = (20, 180, 20)  # Green for health
                        elif stat_name == "damage":
                            fill_color = (180, 20, 20)  # Red for damage
                        else:  # speed
                            fill_color = (20, 20, 180)  # Blue for speed
                            
                        pygame.draw.rect(self.screen, fill_color, fill_rect, border_radius=4)
                    
                    # Draw numeric value with even smaller font
                    # Create an even smaller font for the numeric values
                    value_font = pygame.font.Font(None, 22)  # Smaller than the regular small font
                    value_text = value_font.render(str(stat_value), True, WHITE)
                    
                    # Position value closer to the bar
                    value_rect = value_text.get_rect(left=bar_bg_rect.right + 5, centery=stats_y)
                    self.screen.blit(value_text, value_rect)
                    
                    stats_y += 15  # Tighter spacing between stats to ensure they fit in panel
            
            # Handle range and special ability with ultra-compact layout
            range_y = stats_y
            
            # Create even smaller fonts for range and special
            tiny_font = pygame.font.Font(None, 22)  # Tiny font for stats values and labels
            
            # Range on left side with less padding - using tiny font
            range_label = tiny_font.render("Range:", True, WHITE)
            range_value = tiny_font.render(character['stats']['range'], True, WHITE)
            
            # Position range label
            range_label_rect = range_label.get_rect(left=stats_panel_rect.left + 10, centery=range_y)
            self.screen.blit(range_label, range_label_rect)
            
            # Position range value
            range_value_rect = range_value.get_rect(left=range_label_rect.right + 5, centery=range_y)
            self.screen.blit(range_value, range_value_rect)
            
            # Create more compact special ability display
            if "special" in character:
                # If we have very limited space, abbreviate the special ability text
                if character["rect"].bottom - range_y < 25:  # Very tight space
                    # Create special ability on same line as range to save space
                    spec_label = tiny_font.render("Special:", True, (220, 220, 100))  # Gold "Special:" label
                    
                    # Position special label to the right of range value
                    spec_label_rect = spec_label.get_rect(left=range_value_rect.right + 15, centery=range_y)
                    self.screen.blit(spec_label, spec_label_rect)
                    
                    # Position special value
                    spec_text = tiny_font.render(character['special'], True, (220, 220, 100))  # Gold value text
                    spec_text_rect = spec_text.get_rect(left=spec_label_rect.right + 3, centery=spec_label_rect.centery)
                    self.screen.blit(spec_text, spec_text_rect)
                else:
                    # Regular display with enough space
                    spec_label = tiny_font.render("Special:", True, (220, 220, 100))  # Gold "Special:" label
                    spec_text = tiny_font.render(character['special'], True, (220, 220, 100))  # Gold value text
                    
                    # Position label
                    spec_label_rect = spec_label.get_rect(left=stats_panel_rect.left + 10, centery=range_y + 14)
                    self.screen.blit(spec_label, spec_label_rect)
                    
                    # Position value
                    spec_text_rect = spec_text.get_rect(left=spec_label_rect.right + 5, centery=spec_label_rect.centery)
                    self.screen.blit(spec_text, spec_text_rect)
        
        # Create an info panel with character description and icon - with precise positioning
        info_panel_width = 500  # Smaller width for better proportions
        info_panel_height = 70
        
        # Calculate the exact bottom position of the character cards
        # Verify that both cards have the same bottom position
        bottom_positions = [char["rect"].bottom for char in self.characters]
        char_card_bottom = max(bottom_positions)
        
        # Make sure we have enough space to place info panel and confirm button
        info_panel_rect = pygame.Rect(
            SCREEN_WIDTH//2 - info_panel_width//2,
            char_card_bottom + 25,  # Carefully measured spacing from cards
            info_panel_width,
            info_panel_height
        )
        
        # Draw info panel background
        info_bg = pygame.Surface((info_panel_width, info_panel_height), pygame.SRCALPHA)
        selected_color = self.characters[self.selected_character]["color"]
        # Create gradient panel with character's color influence
        pygame.draw.rect(
            info_bg, 
            (int(selected_color[0]*0.3), int(selected_color[1]*0.3), int(selected_color[2]*0.3), 220),
            (0, 0, info_panel_width, info_panel_height),
            border_radius=15
        )
        self.screen.blit(info_bg, info_panel_rect.topleft)
        
        # Draw decorative border
        pygame.draw.rect(
            self.screen,
            selected_color,
            info_panel_rect,
            3,  # Border width
            border_radius=15
        )
        
        # Draw character icon next to description
        icon_size = 60
        icon_frame = self.characters[self.selected_character]["frames"][0]
        icon = pygame.transform.scale(icon_frame, (icon_size, icon_size))
        icon_rect = icon.get_rect(left=info_panel_rect.left + 20, centery=info_panel_rect.centery)
        
        # Add a circular background for the icon
        icon_bg = pygame.Surface((icon_size+10, icon_size+10), pygame.SRCALPHA)
        pygame.draw.circle(icon_bg, (50, 50, 60, 200), (icon_size//2+5, icon_size//2+5), icon_size//2+5)
        self.screen.blit(icon_bg, (icon_rect.left-5, icon_rect.top-5))
        self.screen.blit(icon, icon_rect)
        
        # Draw character description with title
        desc_title = self.font_medium.render(self.characters[self.selected_character]["name"] + ":", True, WHITE)
        desc_title_rect = desc_title.get_rect(left=icon_rect.right + 20, top=info_panel_rect.top + 15)
        self.screen.blit(desc_title, desc_title_rect)
        
        desc_text = self.font_small.render(self.characters[self.selected_character]["description"], True, WHITE)
        desc_rect = desc_text.get_rect(left=icon_rect.right + 20, top=desc_title_rect.bottom + 5)
        self.screen.blit(desc_text, desc_rect)
        
        # Create a perfectly positioned confirm button
        # Calculate spacing to ensure button is properly placed below info panel
        button_width = 160  # Smaller width for better proportions
        button_height = 38  # Slightly smaller height
        
        # Position button with exact spacing
        self.confirm_button_rect = pygame.Rect(
            SCREEN_WIDTH//2 - button_width//2, 
            info_panel_rect.bottom + 20, 
            button_width, 
            button_height
        )
        
        # Choose button color with pulsing effect when highlighted
        base_color = (0, 180, 0)  # Base green color
        if self.button_highlighted:
            # Add pulsing effect
            pulse_intensity = (math.sin(self.pulse_timer * 2) * 0.2) + 0.8
            button_color = (
                min(255, int(base_color[0] + 40 * pulse_intensity)),
                min(255, int(base_color[1] + 40 * pulse_intensity)),
                min(255, int(base_color[2] + 40 * pulse_intensity))
            )
        else:
            button_color = base_color
            
        # Draw button shadow for depth
        shadow_rect = self.confirm_button_rect.inflate(6, 6)
        shadow_rect.move_ip(3, 3)  # Offset shadow
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 150), (0, 0, shadow_rect.width, shadow_rect.height), border_radius=10)
        self.screen.blit(shadow_surface, shadow_rect.topleft)
        
        # Create button with gradient effect
        button_surface = pygame.Surface((self.confirm_button_rect.width, self.confirm_button_rect.height), pygame.SRCALPHA)
        for y in range(self.confirm_button_rect.height):
            # Create gradient from bottom to top
            ratio = y / self.confirm_button_rect.height
            r = int(button_color[0] * (0.8 + 0.2 * ratio))
            g = int(button_color[1] * (0.8 + 0.2 * ratio))
            b = int(button_color[2] * (0.8 + 0.2 * ratio))
            color = (r, g, b)
            pygame.draw.line(button_surface, color, 
                         (0, self.confirm_button_rect.height - y), 
                         (self.confirm_button_rect.width, self.confirm_button_rect.height - y))
        
        # Apply rounded corners to the button gradient
        pygame.draw.rect(button_surface, (0, 0, 0, 0), (0, 0, self.confirm_button_rect.width, self.confirm_button_rect.height), border_radius=10)
        self.screen.blit(button_surface, self.confirm_button_rect.topleft)
        
        # Add highlight effect when button is highlighted (with proper alpha)
        if self.button_highlighted:
            # Add outer glow effect with smaller size
            glow_size = 4  # Reduced glow size
            glow_rect = self.confirm_button_rect.inflate(glow_size*2, glow_size*2)
            # Create glow surface with alpha for proper transparency
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (100, 255, 100, 80), (0, 0, glow_rect.width, glow_rect.height), 
                          glow_size, border_radius=14)
            self.screen.blit(glow_surface, glow_rect.topleft)
            
            # Add arrow icon before text
            confirm_text = self.font_medium.render("▶ Confirm", True, WHITE)
        else:
            confirm_text = self.font_medium.render("Confirm", True, WHITE)
            
        # Draw white outline
        pygame.draw.rect(self.screen, WHITE, self.confirm_button_rect, 2, border_radius=10)
        
        # Position and draw text
        confirm_text_rect = confirm_text.get_rect(center=self.confirm_button_rect.center)
        self.screen.blit(confirm_text, confirm_text_rect)
    
    def run(self):
        """
        Run the character selection screen.
        
        Returns:
            dict, "back", or "quit": Selected character data if a character was selected,
                                     "back" to go back to main menu, or "quit" to exit.
        """
        clock = pygame.time.Clock()
        
        while True:
            # Handle events
            result = self.handle_events()
            if result is not None:
                return result
            
            # Update and draw
            dt = clock.tick(60) / 1000.0
            self.update(dt)
            self.draw()
            
            # Update display
            pygame.display.flip()