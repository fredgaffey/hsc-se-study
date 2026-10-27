"""
Test package for Adventure Game

This module contains initialization settings for tests, but ensures
these settings only apply during test runs and not when running the main game.
"""

import os
import sys

# Only set dummy video driver when actually running test modules directly,
# not when imported from the main game or other modules
if __name__ != "__main__" and (
    'unittest' in sys.modules or
    any(arg.startswith('test') for arg in sys.argv) or
    any('pytest' in arg for arg in sys.argv) or
    any('unittest' in arg for arg in sys.argv)):
    # Use dummy video driver to prevent visible windows during tests
    os.environ['SDL_VIDEODRIVER'] = 'dummy'