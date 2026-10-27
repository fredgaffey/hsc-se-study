# Wizard Hitbox Tools

This directory contains tools for adjusting, verifying, and comparing the wizard's hitbox settings in the game.

## Directory Structure

```
hitbox_tools/
├── adjustment/
│   └── wizard_hitbox_adjuster.py  - Interactive tool for adjusting the wizard's hitbox
├── verification/
│   ├── hitbox_comparison_tool.py  - Tool for comparing original and new hitbox settings
│   └── wizard_hitbox_verifier.py  - Simple tool for verifying hitbox position
└── README.md
```

## Adjustment Tools

### Wizard Hitbox Adjuster

The Wizard Hitbox Adjuster is an interactive tool that allows you to adjust the wizard's hitbox size and position. It provides real-time visualization of the changes and allows you to save and load configurations.

**Features:**
- Move the hitbox with arrow keys
- Resize the hitbox with Shift+arrow keys
- Centre the hitbox on the sprite
- Reset to original values
- Save and load configurations
- Toggle debug information
- Toggle animation

**Usage:**
```bash
python tests/hitbox_tools/adjustment/wizard_hitbox_adjuster.py
```

**Controls:**
- ARROWS: Move hitbox
- SHIFT+ARROWS: Resize hitbox
- C: Centre hitbox on sprite
- R: Reset to original values
- S: Save configuration
- L: Load last configuration
- 1-9: Load saved configuration
- D: Toggle debug visuals
- SPACE: Toggle animation
- ESC: Exit

## Verification Tools

### Hitbox Comparison Tool

This tool provides a side-by-side comparison of the original and new hitbox settings, allowing you to visualise the differences between different configurations.

**Features:**
- View original hitbox (red)
- View new hitbox (green)
- Toggle between original, new, or both
- Toggle animation
- Detailed information display

**Usage:**
```bash
python tests/hitbox_tools/verification/hitbox_comparison_tool.py
```

**Controls:**
- 1: Show only original hitbox (RED)
- 2: Show only new hitbox (GREEN)
- 3: Show both hitboxes
- SPACE: Toggle animation
- ESC: Exit

### Wizard Hitbox Verifier

A simpler tool that shows the current wizard hitbox configuration as implemented in the game.

**Features:**
- View current hitbox settings
- Toggle animation
- Toggle debug information
- Take screenshots

**Usage:**
```bash
python tests/hitbox_tools/verification/wizard_hitbox_verifier.py
```

**Controls:**
- SPACE: Toggle animation
- D: Toggle debug info
- H: Toggle help text
- F1: Take screenshot
- ESC: Exit

## Development Notes

These tools were developed to facilitate the adjustment and verification of the wizard character's hitbox in the OOP dungeon game. The hitbox dimensions and offsets can be carefully tuned to ensure proper collision detection while maintaining intuitive gameplay.

When modifying the wizard's hitbox, use these tools in the following order:

1. Use the **Wizard Hitbox Adjuster** to find appropriate hitbox dimensions and offsets
2. Update the wizard class with the new values
3. Verify the changes with the **Wizard Hitbox Verifier**
4. Compare before and after changes with the **Hitbox Comparison Tool**