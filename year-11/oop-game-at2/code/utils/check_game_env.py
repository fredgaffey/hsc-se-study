#!/usr/bin/env python3
"""
Helper script to check environment variables in the game
"""

import os
import sys

def check_env():
    """Print environment variables and imported modules"""
    print("=" * 50)
    print("ENVIRONMENT CHECK")
    print("=" * 50)
    print("Environment variables:")
    print(f"SDL_VIDEODRIVER: {os.environ.get('SDL_VIDEODRIVER', 'Not set')}")
    
    # Check if tests module is imported
    print("\nIs 'tests' module imported?")
    if 'tests' in sys.modules:
        print("  YES - tests module is imported")
        print(f"  tests module path: {sys.modules['tests'].__file__}")
        
        # If tests is imported, check its content
        import tests
        print("\nChecking tests module attributes:")
        print(f"  tests.__name__ = {tests.__name__}")
        
        # Check if the SDL_VIDEODRIVER is set in the tests module
        try:
            import inspect
            source = inspect.getsource(tests)
            print("\nChecking tests module source:")
            if "SDL_VIDEODRIVER" in source:
                print("  SDL_VIDEODRIVER is set in tests module source")
            else:
                print("  SDL_VIDEODRIVER is NOT found in tests module source")
        except Exception as e:
            print(f"  Error inspecting tests module: {e}")
    else:
        print("  NO - tests module is not imported")
    
    print("=" * 50)
    print("END OF ENVIRONMENT CHECK")
    print("=" * 50)

# Call this from game.py's __init__ 
check_env()