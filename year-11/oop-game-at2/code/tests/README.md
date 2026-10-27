# Dungeon Game Test Suite

This directory contains a comprehensive test suite for the Dungeon Game project. The tests are organised by functionality and purpose, making it easier to maintain, run specific tests, and verify different aspects of the game.

## Test Organisation

### Test Runner Scripts
- `run_all_tests.py`: Executes all test cases in the project with a unified report
- `run_tests.py`: Utility script for running selected test cases with customisable output

### Unit Tests
- `test_character.py`: Tests for the Player class, including initialisation, movement, combat mechanics, and animation states
- `test_wizard.py`: Tests for the Wizard character, covering projectile creation, hitbox properties, and special abilities
- `test_enemy.py`: Tests for Enemy class initialisation, AI behaviour, movement patterns, and combat mechanics
- `test_collision.py`: Tests for the collision detection system, including wall collisions, boundary checks, and edge cases
- `test_map.py`: Tests for the GameMap class, validating tile loading, wall detection, player positioning, and level transitions
- `test_trap.py`: Tests for trap functionality, including activation states, damage mechanics, and visual effects
- `test_chest.py`: Tests for treasure chests, covering opening mechanics, loot generation, and visual states
- `test_coin.py`: Tests for coin collection, animation, and value assignment
- `test_portal.py`: Tests for level transition portals, including player detection and level advancement
- `test_game_object.py`: Tests for the base GameObject class, covering position tracking and collision detection
- `test_screens.py`: Tests for game screens including intro and character selection interfaces
- `test_ui.py`: Tests for UI elements, message display, and health bar rendering
- `test_readme.py`: Validates that the README documentation accurately reflects the codebase

### Demo Tests
These standalone interactive tests demonstrate specific game features:
- `animation_test.py`: Demonstrates the animation system with various character sprites
- `chest_demo.py`: Interactive demo for chest opening and loot acquisition
- `coin_demo.py`: Demo showcasing coin animation and collection mechanics
- `game_coin_test.py`: Extended test integrating coins into the main game environment

## Hitbox Tools

The `hitbox_tools` directory contains specialised tools for adjusting and verifying character hitboxes:

### Adjustment Tools
- `wizard_hitbox_adjuster.py`: Interactive tool for fine-tuning the wizard character's hitbox dimensions and position

### Verification Tools
- `hitbox_comparison_tool.py`: Compares hitbox configurations across different character types
- `wizard_hitbox_verifier.py`: Visual verification tool for wizard hitbox placement

## Detailed Test Descriptions

### Character Tests
`test_character.py` verifies the Player class functionality:
- Initialization with proper attribute values
- Health and damage system
- Movement and collision detection
- Animation state transitions
- Combat mechanics and attack range

### Wizard Tests
`test_wizard.py` tests the specialized Wizard class:
- Custom hitbox dimensions (16x20 pixels)
- Hitbox offsets (43px horizontal, 15px vertical)
- Projectile creation and movement
- Particle effects handling
- Enemy targeting system

### Collision Tests
`test_collision.py` focuses on collision detection:
- Wall collision detection
- Map boundary checks
- Edge case handling for corners and tight spaces
- Hitbox positioning relative to sprite

### Trap Tests
`test_trap.py` validates the Trap class:
- Cyclic activation (spikes up/down states)
- Player damage mechanics
- Trigger cooldown system
- Visual state indication
- Shake effects on activation

### Interactive Demos
The demo tests provide visual feedback for specific components:
- `chest_demo.py`: Shows chest animations, opening mechanics, and loot display
- `coin_demo.py`: Demonstrates coin bobbing animations and collection
- `animation_test.py`: Visualizes character animations for different states

## Running Tests

From the project root directory:

### Run All Tests
```bash
python -m tests.run_all_tests
```

### Run a Specific Test
```bash
python -m tests.run_tests test_wizard
```

### Run an Interactive Demo
```bash
python -m tests.chest_demo
```

### Run Hitbox Adjustment Tool
```bash
python -m tests.hitbox_tools.adjustment.wizard_hitbox_adjuster
```

## Test Development Guidelines

When creating new tests:

1. **Organisation**: Place tests in the appropriate file based on functionality
2. **Structure**: Use proper OOP structure with test classes inheriting from `unittest.TestCase`
3. **Independence**: Ensure tests are independent and can run in isolation
4. **Documentation**: Add docstrings explaining the purpose and approach of each test
5. **Assertions**: Use appropriate assertions to validate expected behaviour
6. **Setup/Teardown**: Properly initialise and clean up test environments
7. **Australian English**: Use Australian English spelling conventions (e.g., "initialise" instead of "initialize")
8. **Hitbox Values**: Use the current hitbox offset values (38px horizontal, 15px vertical for Player)
9. **Visual Verification**: For visual features, create demo scripts that allow manual verification