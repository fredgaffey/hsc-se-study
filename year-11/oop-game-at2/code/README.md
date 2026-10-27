[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/_CO-BjsT)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19633133&assignment_repo_type=AssignmentRepo)
# Dungeon Game

A 2D dungeon exploration game built with Python and Pygame, implementing object-oriented programming principles.

## Project Overview

This game is a 2D adventure where players navigate through a dungeon filled with enemies, traps, and interactive objects. Players can choose different character types, each with unique abilities and characteristics. The Knight provides strong melee combat capabilities, while the Wizard offers magical ranged attacks. The game features real-time combat, procedurally generated levels, and various interactive elements like chests, coins, and portals.

## Installation

### Requirements

- Python 3.11+
- Pygame 2.5.2+
- NumPy 1.26.0+

### Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/dungeon-game.git
cd dungeon-game
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the game:
```
python main.py
```

To run the game without running tests first:
```
python main.py --no-tests
```

To run only the tests:
```
python main.py --tests-only
```

### macOS Launcher

On macOS, you can use the included launcher script:
```
./launcher.command
```

This script provides executable permissions and launches the game with the proper Python environment.

## Game Controls

- **Menu Navigation**: Arrow keys to navigate, Enter to select
- **Character Movement**: WASD or Arrow keys
- **Attack**: Spacebar (performs melee attack or launches projectiles, depending on character)
- **Use Item/Interact**: E key (open chests, interact with NPCs)
- **Use Health Potion**: H key
- **Exit/Go Back**: Escape key
- **Character Selection**: Select character type at the start of the game

## Game Features

- Multiple character types with different abilities:
  - Knight/Warrior: Strong melee fighter with higher health
  - Wizard: Ranged spellcaster with magical projectiles
- Interactive world elements:
  - Chests containing loot
  - Coins to collect
  - Portals to advance between levels
  - Traps that damage the player when triggered
  - Torches that provide lighting effects
- Enemy combat system:
  - Various enemy types with different behaviours
  - Combat with melee and ranged attacks
  - Health management
- Procedurally generated dungeon levels
- Real-time combat mechanics
- Character selection screen
- Interactive introduction screen

## Code Structure

The game follows object-oriented programming principles with a focus on inheritance, encapsulation, and polymorphism. The main components are organised into packages:

### Core Package
- **Game Class**: Implemented in `core/game.py`, managing the game loop, state transitions, and input handling
- **GameObject Class**: Base class in `core/game_object.py` for all game objects with common properties
- **Map Class**: Handles level generation and rendering in `core/map.py`

### Characters Package
- **Player Class**: Base class for player characters in `characters/player.py`
- **Wizard Class**: Specialised player class with ranged attacks in `characters/wizard.py`
- **Enemy Class**: Handles enemy behaviour and AI in `characters/enemy.py`
- **Character Class**: Abstract base for characters in `characters/character.py`
- **NPC Class**: Non-player characters for interactions in `characters/npc.py`

### Objects Package
- **Chest Class**: Interactive treasure chests in `objects/chest.py`
- **Coin Class**: Collectible coins in `objects/coin.py`
- **Portal Class**: Level transition portals in `objects/portal.py`
- **Torch Class**: Decorative light sources in `objects/torch.py`
- **Trap Class**: Damaging floor traps in `objects/trap.py`

### UI Package
- **UI Class**: Manages in-game interface elements in `ui/ui.py`
- **IntroScreen Class**: Game introduction screen in `ui/intro_screen.py`
- **CharacterSelect Class**: Character selection interface in `ui/character_select.py`

### Utils Package
- **AssetLoader Class**: Centralised asset loading in `utils/asset_loader.py`
- **Constants**: Game constants in `utils/constants.py` and `constants.py`
- **Environment Checker**: Runtime environment validation in `utils/check_game_env.py`

## Project Structure

```
dungeon-game/
│
├── main.py                  # Entry point for the game
├── constants.py             # Global constants (screen dimensions, etc.)
├── launcher.command         # macOS launcher script
├── requirements.txt         # pip dependencies
├── FIXES.md                 # Documentation of bug fixes and improvements
│
├── core/                    # Core game functionality
│   ├── __init__.py
│   ├── game.py              # Main game class
│   ├── game_object.py       # Base game object class
│   └── map.py               # Game map and tile management
│
├── characters/              # Character classes
│   ├── __init__.py
│   ├── character.py         # Abstract Character class
│   ├── player.py            # Player character
│   ├── wizard.py            # Wizard player subclass with projectiles
│   ├── enemy.py             # Enemy character
│   └── npc.py               # Non-player characters
│
├── objects/                 # Game world objects
│   ├── __init__.py
│   ├── chest.py             # Treasure chests
│   ├── coin.py              # Collectible coins
│   ├── portal.py            # Level transition portals
│   ├── torch.py             # Light sources
│   └── trap.py              # Damaging traps
│
├── ui/                      # User interface
│   ├── __init__.py
│   ├── ui.py                # Main UI elements and HUD
│   ├── intro_screen.py      # Game introduction screen
│   └── character_select.py  # Character selection screen
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── asset_loader.py      # Asset loading functionality
│   ├── check_game_env.py    # Runtime environment checker
│   ├── constants.py         # Additional constants
│   └── logger.py            # Game logger
│
├── assets/                  # Game assets
│   ├── Archer/              # Archer character sprites
│   ├── Armored Axeman/      # Armored Axeman character sprites
│   ├── Armored Orc/         # Armored Orc character sprites
│   ├── Wizard/              # Wizard character sprites
│   ├── character and tileset/ # Tileset sprites
│   ├── interface/           # UI elements
│   ├── items and trap_animation/ # Item and trap sprites
│   └── main_menu_background.png  # Menu background
│
└── tests/                   # Test suite
    ├── __init__.py
    ├── README.md            # Test documentation
    ├── run_all_tests.py     # Run all tests
    ├── run_tests.py         # Run specific tests
    ├── test_character.py    # Player character tests
    ├── test_collision.py    # Collision detection tests
    ├── test_enemy.py        # Enemy behavior tests
    ├── test_wizard.py       # Wizard specific tests
    ├── test_trap.py         # Trap functionality tests
    ├── test_chest.py        # Chest functionality tests
    ├── test_coin.py         # Coin functionality tests
    ├── animation_test.py    # Animation system tests
    ├── coin_demo.py         # Coin demo
    ├── chest_demo.py        # Chest demo
    └── hitbox_tools/        # Hitbox adjustment tools
        ├── README.md
        ├── adjustment/      # Tools for hitbox adjustment
        └── verification/    # Tools for hitbox verification
```

## Class Descriptions

### Core Package Classes

#### GameObject (core/game_object.py)
The base class for all interactive game objects. Provides fundamental functionality:
- Position tracking with x, y coordinates
- Hitbox management for collision detection
- Update and draw method interfaces for the game loop
- Collision detection between objects

**Key Functions:**
```python
def collides_with(self, other):
    """Check if this object collides with another game object.
    
    Args:
        other: Another GameObject to check collision with.
        
    Returns:
        True if hitboxes collide, False otherwise.
    """
    # Simple rectangle collision using hitboxes
    # Pygame's colliderect method efficiently checks if two rectangles overlap
    # This is the foundation of all collision detection in the game
    return self.hitbox.colliderect(other.hitbox)

def update(self, game_map):
    """Update the game object state.
    
    Args:
        game_map: The game map this object exists in.
    """
    # Update hitbox position based on object position
    # Every GameObject has a hitbox which is offset from the visual sprite
    # These offsets (hitbox_offset_x/y) allow fine-tuning of collision areas
    # The hitbox is automatically repositioned when the object moves
    self.hitbox.x = self.x + self.hitbox_offset_x
    self.hitbox.y = self.y + self.hitbox_offset_y
```

#### Game (core/game.py)
The central game engine that manages all game elements and flow:
- Main game loop implementation
- State management (intro, character select, gameplay, game over)
- Level transitions
- Object creation and management
- Input handling
- Rendering pipeline

**Key Functions:**
```python
def run(self):
    """Main game loop that handles state transitions and updates."""
    # Game loop continues until exit - this is the heart of the game
    # The game loop pattern is fundamental to game development:
    # 1. Process input/events
    # 2. Update game state
    # 3. Render to screen
    # 4. Repeat until game ends
    while self.running:
        # Get time elapsed since last frame for consistent gameplay regardless of FPS
        # Converting to seconds from milliseconds for easier time calculations
        self.delta_time = self.clock.tick(self.FPS) / 1000.0
        
        # Handle events based on current game state
        # The game uses a state machine pattern to manage different screens/modes
        # Each state has its own event handling logic
        if self.state == "intro":
            self.intro_screen.handle_events()  # Title screen events
        elif self.state == "character_select":
            self.character_select.handle_events()  # Character selection events
        elif self.state == "gameplay":
            self.handle_events()  # Main gameplay events
        elif self.state == "game_over":
            self.handle_game_over_events()  # Game over screen events
            
        # Update and render based on current state
        # These methods contain state-specific logic for updating and drawing
        self.update()
        self.render()
            
    # Clean up resources when the game exits
    pygame.quit()

def handle_events(self):
    """Process input events during gameplay."""
    # Process all pending events in the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Window close button clicked
            self.running = False  # Exit the game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # ESC key returns to the intro/title screen
                self.state = "intro"
            elif event.key == pygame.K_SPACE and not self.current_character.attacking:
                # Space triggers the player's attack if not already attacking
                # This calls the appropriate attack method based on character type
                self.current_character.attack()
                # Other keys for movement are handled in the update method
```

#### GameMap (core/map.py)
Handles map generation and management:
- Level data loading from constants
- Procedural map generation with variations
- Tile-based collision detection
- Player start and exit portal positioning
- Wall type determination for visual variety

**Key Functions:**
```python
def is_wall(self, x, y):
    """Check if a given tile position is a wall.
    
    Args:
        x: Grid x-coordinate to check
        y: Grid y-coordinate to check
        
    Returns:
        True if position contains a wall, False otherwise
    """
    # Check if coordinates are out of map bounds
    # This boundary check is important for preventing index errors
    # It also ensures that the game world is properly bounded by invisible walls
    if x < 0 or x >= self.width or y < 0 or y >= self.height:
        return True  # Treat out-of-bounds as walls (creates boundary)
    
    # Check if this position is a wall (1) in the map data
    # The map is represented as a 2D array where 1 indicates a wall
    # This simple representation allows for easy level design and collision detection
    return self.map_data[y][x] == 1  # Note y is first since arrays are [row][column]

def get_player_start_position(self):
    """Find a safe starting position for the player.
    
    Returns:
        tuple: (x, y) pixel coordinates for player placement
    """
    # Try to find a position that isn't a wall
    # This algorithm searches the map from top-left to bottom-right
    # looking for the first open space to place the player
    for y in range(self.height):
        for x in range(self.width):
            if not self.is_wall(x, y):
                # Convert grid coordinates to pixel coordinates
                # Multiply by tile size to get actual screen position
                # This translates from the tile-based map to the pixel-based game world
                return x * self.tile_size, y * self.tile_size
                
    # Fallback to default position if no suitable position found
    # This should rarely happen with properly designed levels
    # but provides a safety net in case of level design issues
    return 100, 100
```

### Character Classes

#### Player (characters/player.py)
Base player character class:
- Movement with physics and collision detection
- Animation state management (idle, attack)
- Health system with damage handling
- Combat mechanics with melee attacks
- Directional facing and sprite flipping
- Hitbox positioning tailored to sprite dimensions

**Key Functions:**
```python
def move(self, dx, dy, game_map):
    """Move the player with collision detection.
    
    Args:
        dx: Change in x position
        dy: Change in y position
        game_map: The game map for wall collision detection
    """
    # Store original position for collision recovery
    # This lets us revert to a safe position if a movement would cause a collision
    original_x, original_y = self.x, self.y
    
    # Try to move horizontally first (x-axis)
    # This is a key part of the game's movement system:
    # 1. Try to move in one axis
    # 2. Check for collisions
    # 3. If collision detected, revert that movement
    # 4. Try the other axis independently
    self.x += dx
    self.update_hitbox()  # Update hitbox to new position
    
    # Check if we'd hit a wall with this x movement
    if self.check_wall_collision(game_map):
        self.x = original_x  # Revert x position if we hit a wall
    
    # Try to move vertically next (y-axis)
    # This independent axis movement allows sliding along walls
    # when moving diagonally, creating smoother gameplay
    self.y += dy
    self.update_hitbox()  # Update hitbox again
    
    # Check if we'd hit a wall with this y movement
    if self.check_wall_collision(game_map):
        self.y = original_y  # Revert y position if we hit a wall
    
    # Update facing direction based on horizontal movement
    # This affects which way sprites are drawn and which direction attacks go
    if dx > 0:
        self.facing_right = True  # Moving right
    elif dx < 0:
        self.facing_right = False  # Moving left

def attack(self):
    """Initiate an attack and check for enemies in range."""
    # Start attack animation sequence
    # The state change triggers different sprite rendering
    self.attacking = True
    self.attack_start_time = time.time()  # Track when attack started
    self.current_frame = 0  # Reset animation to first frame
    self.state = "attack"  # Change character state
    
    # If no enemies or game map, we can't attack anything
    # This safety check prevents errors if called in an invalid context
    if not self.game_map or not self.game_map.enemies:
        return
        
    # Calculate attack hitbox based on facing direction
    # The attack area is a rectangle extending from the player
    # in the direction they're facing
    attack_range = 50  # Pixels - how far the attack reaches
    if self.facing_right:
        # Create attack area to the right of player
        attack_rect = pygame.Rect(
            self.hitbox.right,  # Start at right edge of player
            self.hitbox.y,      # Same vertical position as player
            attack_range,       # Extend forward by attack range
            self.hitbox.height) # Same height as player
    else:
        # Create attack area to the left of player
        attack_rect = pygame.Rect(
            self.hitbox.x - attack_range,  # Start attack range left of player
            self.hitbox.y,                 # Same vertical position
            attack_range,                  # Extend by attack range
            self.hitbox.height)            # Same height as player
    
    # Check for enemies in attack range
    # Iterate through all enemies to see if they're hit
    for enemy in self.game_map.enemies:
        # Only hit enemies that are alive and within range
        if attack_rect.colliderect(enemy.hitbox) and not enemy.is_dying:
            # Apply damage to the enemy
            enemy.take_damage(self.attack_damage)
            # Note: We don't stop at the first enemy - can hit multiple enemies at once
```

#### Wizard (characters/wizard.py)
Specialised player class extending Player:
- Ranged magical projectile attacks
- Special projectile class for spell effects
- Particle effects for visual enhancement
- Custom hitbox sizing (smaller than knight)
- Specialised attack range calculation
- Auto-targeting of nearest enemy

**Key Functions:**
```python
def attack(self):
    """Override Player attack to cast a magical projectile."""
    # Start attack animation sequence - similar to the base Player class
    # but with different visual effects and projectile creation
    self.attacking = True
    self.attack_start_time = time.time()
    self.current_frame = 0
    self.state = "attack"
    
    # Target selection logic - this is what makes the Wizard unique
    # Unlike the melee Player class, Wizard needs to determine where to shoot
    if not self.game_map or not self.game_map.enemies:
        # If no targets available, just fire in the facing direction
        # This allows attacking even when no enemies are visible
        target_x = self.x + 200 if self.facing_right else self.x - 200
        target_y = self.y
    else:
        # Auto-targeting system to find the nearest enemy in range
        # This is a key advantage of the Wizard class - smart targeting
        nearest_enemy = None
        min_distance = float('inf')
        
        # Loop through all enemies to find the closest one
        for enemy in self.game_map.enemies:
            # Skip enemies that are already dying
            if enemy.is_dying:
                continue
                
            # Calculate distance to this enemy using Pythagorean theorem
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Keep track of the closest enemy within attack range
            if distance < min_distance and distance < self.attack_range:
                nearest_enemy = enemy
                min_distance = distance
        
        # Determine projectile target position
        if nearest_enemy:
            # If we found a valid target, aim directly at its center
            # This auto-aiming is what makes the Wizard powerful
            target_x = nearest_enemy.hitbox.centerx
            target_y = nearest_enemy.hitbox.centery
        else:
            # No viable target in range, fire in facing direction as fallback
            target_x = self.x + 200 if self.facing_right else self.x - 200
            target_y = self.y
    
    # Calculate projectile starting position
    # Offset from the wizard's center to look like it's coming from their hands
    start_x = self.hitbox.centerx + (20 if self.facing_right else -20)
    start_y = self.hitbox.centery - 10  # Slightly above center for visual effect
    
    # Create and add projectile to the game
    # The Projectile class handles movement, collision detection, and visual effects
    projectile = Projectile(
        start_x, start_y,           # Starting position
        target_x, target_y,         # Target position
        damage=self.attack_damage,  # Same damage as the wizard's attack stat
        effect_images=self.projectile_effect_images  # Visual effect sprites
    )
    # Add to projectiles list so it can be updated and drawn
    self.projectiles.append(projectile)
    # Note: The projectiles will be updated in the wizard's update method
```

#### Enemy (characters/enemy.py)
Enemy character implementation:
- AI movement toward player
- Attack behaviour with melee combat
- Health and damage systems
- Death animation and state management
- Sprite handling with multiple animation states

**Key Functions:**
```python
def update(self, game_map):
    """Update enemy state, movement, and actions.
    
    Args:
        game_map: The game map with player and walls.
    """
    # Death animation handling
    # If this enemy is dying, we only need to advance the death animation
    # This creates a smooth visual transition when enemies are defeated
    if self.is_dying:
        current_time = time.time()
        if current_time - self.death_start_time > self.frame_duration:
            # Advance the death animation, but don't go beyond the last frame
            self.current_frame = min(self.current_frame + 1, len(self.death_frames) - 1)
            self.death_start_time = current_time
        return  # Skip all other logic if dying
    
    # Safety check - if missing required references, do nothing
    if not game_map or not game_map.player:
        return
        
    # Calculate distance to player - this is the core of enemy AI
    # Enemies are aware of the player's position and respond to it
    player = game_map.player
    dx = player.x - self.x  # X distance to player
    dy = player.y - self.y  # Y distance to player
    distance = math.sqrt(dx * dx + dy * dy)  # Euclidean distance
    
    # Update hitbox position to match enemy sprite position
    self.hitbox.x = self.x + self.hitbox_offset_x
    self.hitbox.y = self.y + self.hitbox_offset_y
    
    # Enemy AI decision making
    # If close enough to attack, try to attack the player
    if distance < self.attack_range:
        # Only attack if not already attacking and cooldown has elapsed
        # This prevents enemies from attacking too rapidly
        if not self.attacking and time.time() - self.last_attack_time > self.attack_cooldown:
            self.attack(player)
    else:
        # Not in attack range, so pursue the player
        if distance > 0:
            # Normalize the direction vector for consistent movement speed
            # This ensures enemies move at their defined speed regardless of distance
            dx /= distance
            dy /= distance
            
            # Move toward player using pathfinding with wall collision detection
            # The move method handles wall avoidance
            self.move(dx * self.speed, dy * self.speed, game_map)
        
    # Update facing direction to always face the player
    # This makes the enemy always visually oriented toward the player
    if player.x < self.x:
        self.facing_right = False  # Face left
    else:
        self.facing_right = True   # Face right

def take_damage(self, damage):
    """Take damage and potentially die.
    
    Args:
        damage: Amount of damage to take
    """
    # Reduce health by damage amount
    self.health -= damage
    
    # Visual feedback for being hit - flash or color change
    # This provides player feedback that their attack connected
    self.hurt_flash = True
    self.hurt_flash_start = time.time()
    
    # Death check - if health is depleted, begin death sequence
    if self.health <= 0 and not self.is_dying:
        # Initiate death sequence
        self.is_dying = True  # Change state to dying
        self.current_frame = 0  # Start death animation from beginning
        self.death_start_time = time.time()
        
        # Drop rewards for the player
        # This creates the game's reward loop - defeat enemies to get coins
        self.drop_loot()  # Spawn coins or other items
        
        # Note: The enemy isn't immediately removed - it plays a death animation
        # The actual removal happens in the game's update loop based on is_dying flag
```

#### NPC (characters/npc.py)
Non-player character for interactions:
- Proximity-based interaction with player
- Dialog system
- Visual indicators for interactive state

### Object Classes

#### Chest (objects/chest.py)
Interactive treasure containers:
- Open/closed states with animations
- Contains randomised loot (gold and potions)
- Visual effects (glow, bobbing animation)
- Player interaction handling

**Key Functions:**
```python
def interact(self, player):
    """Open the chest and give contents to player.
    
    Args:
        player: The player character interacting with the chest
    
    Returns:
        str: A message describing what was in the chest
    """
    # If already open, do nothing
    if self.is_open:
        return "This chest is already open."
    
    # Open the chest
    self.is_open = True
    self.current_frame = 0  # Start open animation
    
    # Generate random loot (coins and potions)
    gold_amount = random.randint(5, 20)
    potion_chance = random.random()
    
    # Add gold to player
    player.gold += gold_amount
    message = f"Found {gold_amount} gold!"
    
    # Maybe add a health potion (20% chance)
    if potion_chance < 0.2:
        player.potions += 1
        message += " And a health potion!"
    
    # Play sound effect
    if self.open_sound:
        self.open_sound.play()
    
    return message

def update(self, game_map):
    """Update chest state and animations.
    
    Args:
        game_map: The game map this chest exists in
    """
    # Update animation frame
    current_time = time.time()
    
    # If opening, advance the animation
    if self.is_open and self.current_frame < len(self.open_frames) - 1:
        if current_time - self.frame_time > self.frame_duration:
            self.current_frame += 1
            self.frame_time = current_time
    
    # If not open, do bobbing animation
    if not self.is_open:
        self.bob_offset = math.sin(current_time * 2) * 2  # Gentle bobbing effect
    else:
        self.bob_offset = 0  # No bobbing when open
    
    # Update hitbox position
    self.hitbox.x = self.x + self.hitbox_offset_x
    self.hitbox.y = self.y + self.hitbox_offset_y + self.bob_offset
```

#### Coin (objects/coin.py)
Collectible game currency:
- Animation with spinning frames
- Collection detection with player
- Value assignment
- Visual effects (bobbing movement)

**Key Functions:**
```python
def update(self, game_map):
    """Update coin animation and check for collection.
    
    Args:
        game_map: The game map with player
        
    Returns:
        bool: True if the coin was collected (should be removed)
    """
    # Update animation frame
    current_time = time.time()
    if current_time - self.frame_time > self.frame_duration:
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.frame_time = current_time
    
    # Apply bobbing effect using sine wave
    self.bob_offset = math.sin(current_time * 3) * 2
    
    # Update hitbox position
    self.hitbox.x = self.x + 5  # Offset to center hitbox on visual coin
    self.hitbox.y = self.y + 5 + self.bob_offset  # Include bobbing
    
    # Check if player collected the coin
    if game_map and game_map.player:
        if self.collides_with(game_map.player):
            # Add coin value to player's gold
            game_map.player.gold += self.value
            
            # Play collect sound if available
            if self.collect_sound:
                self.collect_sound.play()
                
            # Return True to indicate coin should be removed
            return True
    
    # Coin wasn't collected
    return False
```

#### Portal (objects/portal.py)
Level transition objects:
- Visual effects with animated glow
- Player collision detection for level advancement
- Swirling particle effects

**Key Functions:**
```python
def update(self, game_map):
    """Update portal animation and check for player entry.
    
    Args:
        game_map: The game map with player and game reference
        
    Returns:
        bool: True if player entered portal and level should change
    """
    # Update animation frame
    current_time = time.time()
    if current_time - self.frame_time > self.frame_duration:
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.frame_time = current_time
    
    # Update particle effects
    self.update_particles()
    
    # Check if player entered the portal
    if game_map and game_map.player:
        if self.collides_with(game_map.player):
            if game_map.game:  # If we have a reference to the game
                # Go to next level
                game_map.game.next_level()
                # Play portal sound if available
                if self.portal_sound:
                    self.portal_sound.play()
                return True
    
    return False

def update_particles(self):
    """Update swirling particle effects around the portal."""
    current_time = time.time()
    
    # Create new particles occasionally
    if current_time - self.last_particle_time > self.particle_spawn_rate:
        self.last_particle_time = current_time
        
        # Add a new particle with random attributes
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(15, 30)
        lifetime = random.uniform(0.5, 1.5)
        size = random.uniform(2, 5)
        
        self.particles.append({
            'x': self.hitbox.centerx + math.cos(angle) * distance,
            'y': self.hitbox.centery + math.sin(angle) * distance,
            'angle': angle,
            'distance': distance,
            'creation_time': current_time,
            'lifetime': lifetime,
            'size': size,
            'alpha': 255  # Full opacity to start
        })
    
    # Update existing particles
    for particle in self.particles[:]:
        # Calculate how far through lifetime (0.0 to 1.0)
        age = (current_time - particle['creation_time']) / particle['lifetime']
        
        if age >= 1.0:
            # Remove expired particles
            self.particles.remove(particle)
        else:
            # Move particle in spiral pattern
            particle['distance'] -= 0.5  # Move toward center
            particle['angle'] += 0.1  # Rotate around center
            
            # Update position based on spiral pattern
            particle['x'] = self.hitbox.centerx + math.cos(particle['angle']) * particle['distance']
            particle['y'] = self.hitbox.centery + math.sin(particle['angle']) * particle['distance']
            
            # Fade out as particle gets older
            particle['alpha'] = 255 * (1 - age)
```

#### Torch (objects/torch.py)
Decorative light source:
- Animated flame effect
- Dynamic lighting with glow radius
- Particle system for embers
- Flicker effects for realism

**Key Functions:**
```python
def update(self, game_map):
    """Update torch animation and particle effects.
    
    Args:
        game_map: The game map this torch exists in
    """
    # Update animation frame
    current_time = time.time()
    if current_time - self.frame_time > self.frame_duration:
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.frame_time = current_time
        
        # Occasionally add a random flicker effect
        if random.random() < 0.1:  # 10% chance each frame change
            self.light_intensity = random.uniform(0.8, 1.2)
        else:
            self.light_intensity = 1.0
    
    # Update ember particles
    self.update_particles()

def update_particles(self):
    """Update ember particles rising from torch."""
    current_time = time.time()
    
    # Create new ember particles occasionally
    if random.random() < 0.05:  # 5% chance each update
        # Create a new ember at torch position
        self.particles.append({
            'x': self.x + random.randint(7, 12),  # Centered horizontally on flame
            'y': self.y + 5,  # Near top of torch
            'dx': random.uniform(-0.2, 0.2),  # Slight horizontal drift
            'dy': random.uniform(-0.5, -0.8),  # Upward movement
            'size': random.uniform(1, 3),
            'color': random.choice([(255, 180, 0), (255, 100, 0), (200, 50, 0)]),  # Ember colors
            'creation_time': current_time,
            'lifetime': random.uniform(1.0, 2.0)  # How long the ember lasts
        })
    
    # Update existing particles
    for particle in self.particles[:]:
        # Calculate age of particle
        age = (current_time - particle['creation_time']) / particle['lifetime']
        
        if age >= 1.0:
            # Remove expired particles
            self.particles.remove(particle)
        else:
            # Move particle
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Fade out over lifetime
            particle['alpha'] = int(255 * (1 - age))
```

#### Trap (objects/trap.py)
Hazardous floor elements:
- Cycling between active and inactive states
- Player damage on contact when active
- Visual state indication
- Shake effects when triggered

**Key Functions:**
```python
def update(self, game_map):
    """Update trap state and check for player collision.
    
    Args:
        game_map: The game map with player reference
    """
    current_time = time.time()
    
    # Update animation frame
    if current_time - self.frame_time > self.frame_duration:
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.frame_time = current_time
    
    # Check if it's time to toggle active state
    if current_time - self.last_toggle_time > self.toggle_interval:
        self.active = not self.active
        self.last_toggle_time = current_time
        
        # If activating, add shake effect
        if self.active:
            self.shaking = True
            self.shake_start_time = current_time
            self.shake_duration = 0.3  # Seconds
    
    # Update shake effect
    if self.shaking:
        if current_time - self.shake_start_time > self.shake_duration:
            self.shaking = False
            self.shake_offset_x = 0
            self.shake_offset_y = 0
        else:
            # Calculate random shake offset
            self.shake_offset_x = random.randint(-2, 2)
            self.shake_offset_y = random.randint(-2, 2)
    
    # Check for player collision only when active
    if self.active and game_map and game_map.player:
        if self.collides_with(game_map.player):
            self.trigger(game_map.player)

def trigger(self, player):
    """Trigger the trap effect on a player.
    
    Args:
        player: The player to damage
    """
    # Only damage player if active and cooldown has elapsed
    current_time = time.time()
    if not self.active or current_time - self.last_trigger_time < self.trigger_cooldown:
        return
    
    # Apply damage and set last trigger time
    player.take_damage(self.damage)
    self.last_trigger_time = current_time
    
    # Play sound effect if available
    if self.trigger_sound:
        self.trigger_sound.play()
```

### UI Classes

#### UI (ui/ui.py)
In-game user interface:
- Health display
- Message system for game events
- Inventory display (gold, potions)
- Score tracking

**Key Functions:**
```python
def draw_health_bar(self, screen, player):
    """Draw the player's health bar.
    
    Args:
        screen: The pygame screen to draw on
        player: The player whose health to display
    """
    # Health bar dimensions and positioning
    # These values define the size and position of the health bar on screen
    bar_width = 200  # Width in pixels
    bar_height = 20  # Height in pixels
    bar_x = 20       # X position (from left)
    bar_y = 20       # Y position (from top)
    
    # Draw border and background
    # First a dark border slightly larger than the bar for visual clarity
    pygame.draw.rect(screen, (50, 50, 50),  # Dark gray border 
                   (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
    # Then a medium gray background for the bar itself
    pygame.draw.rect(screen, (100, 100, 100),  # Medium gray background
                   (bar_x, bar_y, bar_width, bar_height))
    
    # Calculate health ratio and width of filled portion
    # This converts the player's health percentage to a width in pixels
    health_ratio = player.health / player.max_health  # 0.0 to 1.0
    health_width = int(bar_width * health_ratio)      # Scale to bar width
    
    # Choose color based on health level - visual feedback on status
    # Green for healthy, yellow for caution, red for danger
    if health_ratio > 0.7:
        color = (0, 255, 0)     # Green (>70% health)
    elif health_ratio > 0.3:
        color = (255, 255, 0)   # Yellow (30-70% health)
    else:
        color = (255, 0, 0)     # Red (<30% health)
    
    # Draw the filled portion of the health bar in the appropriate color
    pygame.draw.rect(screen, color, 
                   (bar_x, bar_y, health_width, bar_height))
    
    # Add text label showing exact health values
    # This provides precise numerical feedback to the player
    health_text = f"Health: {player.health}/{player.max_health}"
    text_surface = self.font.render(health_text, True, (255, 255, 255))  # White text
    # Center text vertically within the bar for clean appearance
    screen.blit(text_surface, (bar_x + 10, bar_y + (bar_height - text_surface.get_height()) // 2))

def show_message(self, message, duration=3.0, color=(255, 255, 255)):
    """Display a timed message to the player.
    
    Args:
        message: The text to display
        duration: How long to show the message (seconds)
        color: RGB color tuple for the message
    """
    # Add message to the queue with all its properties
    # Messages are stored as dictionaries with text, color, timing info
    self.messages.append({
        'text': message,          # The message content
        'color': color,           # Text color (default white)
        'start_time': time.time(),  # When message was created
        'duration': duration      # How long to display (default 3 sec)
    })
    
    # Limit queue size to prevent memory build-up and screen crowding
    # If too many messages, remove the oldest one (FIFO queue)
    if len(self.messages) > 5:  # Maximum 5 messages on screen
        self.messages.pop(0)    # Remove oldest message

def update(self):
    """Update UI elements and remove expired messages."""
    current_time = time.time()
    
    # Remove expired messages using list comprehension
    # This efficiently filters out any messages that have exceeded their duration
    # Only messages that are still within their display time remain
    self.messages = [msg for msg in self.messages 
                   if current_time - msg['start_time'] < msg['duration']]
    
    # Note: The actual drawing of messages happens in the draw method
    # This update method just manages which messages should still be displayed
```

#### IntroScreen (ui/intro_screen.py)
Game introduction interface:
- Background rendering with fallback generation
- Menu options (start, quit)
- Event handling for selection
- Visual effects and styling

#### CharacterSelect (ui/character_select.py)
Character selection interface:
- Character option display with stats
- Preview animations
- Selection highlighting
- Confirmation mechanism

### Utility Classes

#### AssetLoader (utils/asset_loader.py)
Centralised asset management:
- Sprite loading for characters, objects and UI
- Animation frame extraction and processing
- Caching for performance
- Fallback generation for missing assets

## Testing

The game includes a comprehensive test suite to ensure functionality works as expected. Tests are organized by component in the `tests` directory.

### Running Tests

Tests are automatically run when starting the game but can be individually executed:

```
# Run all tests
python -m tests.run_all_tests

# Run a specific test file
python -m tests.run_tests test_wizard
```

### Test Categories

- **Unit Tests**: Test individual classes and methods
- **Integration Tests**: Test interactions between components
- **Hitbox Tools**: Special tools for adjusting and verifying hitboxes
- **Demo Tests**: Interactive demos for visual components

## Extending the Game

The game is designed with extensibility in mind through a robust object-oriented structure.

### Adding New Content

#### New Character Types
1. Create a new class that inherits from `Player` in the characters package
2. Override necessary methods for specialised behaviour
3. Add custom animation handling and combat mechanics
4. Update the `CharacterSelect` class to include the new character
5. Add appropriate sprites to the assets directory

#### New Enemy Types
1. Create a new specialized enemy class that inherits from `Enemy`
2. Configure health, damage, and movement parameters
3. Add custom animations and behavior patterns
4. Update the Game class to spawn the new enemy type

#### New Interactive Objects
1. Create a new class inheriting from `GameObject` in the objects package
2. Implement update and draw methods
3. Add interaction logic with the player
4. Create appropriate sprites and animations
5. Update the Game class to create instances of the new object

### Customising Game Behaviour

- **Game Balance**: Adjust parameters in the constants.py files
- **Visual Style**: Replace or modify assets in the assets directory
- **Map Design**: Edit the map data in the constants.py file
- **Game Mechanics**: Modify the relevant class methods

### Hitbox Adjustment

For fine-tuning character hitboxes, use the hitbox tools in the tests directory:

```
python -m tests.hitbox_tools.adjustment.wizard_hitbox_adjuster
```

This provides an interactive interface for adjusting hitbox dimensions and positions to match character sprites.

### Adding New Levels

1. Add new level data to the `MAPS` list in constants.py
2. Configure appropriate enemy and object placements
3. Add level-specific features or mechanics if needed

## Acknowledgements

- [Pygame](https://www.pygame.org/) - The game framework used
- [Python](https://www.python.org/) - The programming language
