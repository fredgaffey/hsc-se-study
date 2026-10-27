#!/usr/bin/env python3
"""
Main entry point for the Dungeon Game.

This module initializes and runs the game.
Usage:
  python main.py             # Run tests then game
  python main.py --no-tests  # Run only the game
  python main.py --tests-only # Run only the tests
"""

import sys
import os
import pygame
import traceback
import unittest
import time
import argparse

# Import the logger
from utils.logger import game_logger as logger, exception

# Add the current directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class ColoredTextTestResult(unittest.TextTestResult):
    """Custom test result class that displays colored dots."""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.pass_count = 0
        self.fail_count = 0
        self.error_count = 0
        self.skipped_count = 0
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.pass_count += 1
        self.stream.write('\033[92m●\033[0m')  # Green dot
        self.stream.flush()
    
    def addError(self, test, err):
        super().addError(test, err)
        self.error_count += 1
        self.stream.write('\033[91mE\033[0m')  # Red E
        self.stream.flush()
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.fail_count += 1
        self.stream.write('\033[91m●\033[0m')  # Red dot
        self.stream.flush()
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.skipped_count += 1
        self.stream.write('\033[93mS\033[0m')  # Yellow S
        self.stream.flush()

    def printSummary(self):
        """Print test summary."""
        self.stream.writeln('\n')
        self.stream.writeln(f'Tests: {self.testsRun}')
        self.stream.writeln(f'\033[92mPassed: {self.pass_count}\033[0m')
        if self.fail_count > 0:
            self.stream.writeln(f'\033[91mFailed: {self.fail_count}\033[0m')
        else:
            self.stream.writeln(f'Failed: {self.fail_count}')
        if self.error_count > 0:
            self.stream.writeln(f'\033[91mErrors: {self.error_count}\033[0m')
        else:
            self.stream.writeln(f'Errors: {self.error_count}')
        if self.skipped_count > 0:
            self.stream.writeln(f'\033[93mSkipped: {self.skipped_count}\033[0m')
        else:
            self.stream.writeln(f'Skipped: {self.skipped_count}')

class ColoredTextTestRunner(unittest.TextTestRunner):
    """Test runner that uses ColoredTextTestResult."""
    
    def __init__(self, stream=None, descriptions=True, verbosity=1):
        if stream is None:
            stream = sys.stderr
        self.stream = stream
        super().__init__(stream, descriptions, verbosity, 
                        resultclass=ColoredTextTestResult)
    
    def run(self, test):
        """Run the test with our custom result class."""
        result = super().run(test)
        result.printSummary()
        return result

def run_tests():
    """Run all tests and display colored results."""
    logger.info("=== Running Tests Before Game Launch ===")
    
    # Create a loader to discover tests
    loader = unittest.TestLoader()
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(tests_dir)
    
    # Run the tests with our custom runner
    runner = ColoredTextTestRunner(verbosity=1)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_game():
    """Initialize and run the game."""
    try:
        # Import Game class here to avoid circular imports
        from core.game import Game
        
        # Create and run the game
        game = Game()
        game.run()
    except Exception as e:
        exception(f"Error running game: {e}")
    finally:
        # Ensure pygame is properly quit
        pygame.quit()
        sys.exit()

def main():
    """
    Main function that processes command line arguments and runs appropriate components.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Dungeon Game with optional test execution.')
    parser.add_argument('--no-tests', action='store_true', help='Run the game without running tests')
    parser.add_argument('--tests-only', action='store_true', help='Run only the tests without starting the game')
    args = parser.parse_args()
    
    # Handle different modes based on arguments
    if args.tests_only:
        # Run only the tests
        run_tests()
    elif args.no_tests:
        # Make sure pygame and display are properly initialized before running the game
        logger.info("Ensuring pygame is initialized before running the game...")
        
        # Reset any environment variables that might affect display
        if 'SDL_VIDEODRIVER' in os.environ:
            logger.info("Removing SDL_VIDEODRIVER from environment before game start")
            os.environ.pop('SDL_VIDEODRIVER')
        
        # Initialize pygame first in this thread
        pygame.init()
        temp_screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Initializing...")
        temp_screen.fill((0, 0, 0))
        pygame.display.flip()
        
        # Brief pause to ensure window is created
        time.sleep(0.5)
        
        # Now run the game
        run_game()
    else:
        # Run tests first, then game
        tests_passed = run_tests()
        if not tests_passed:
            prompt = input("\nSome tests failed. Run the game anyway? (y/n): ")
            if prompt.lower() != 'y':
                logger.info("Exiting...")
                return
        
        # Pause briefly so user can see test results
        logger.info("Starting game in 3 seconds...")
        time.sleep(3)
        
        # Make sure pygame and display are properly initialized before running the game
        logger.info("Ensuring pygame is initialized before running the game...")
        
        # Reset any environment variables that might affect display
        if 'SDL_VIDEODRIVER' in os.environ:
            logger.info("Removing SDL_VIDEODRIVER from environment before game start")
            os.environ.pop('SDL_VIDEODRIVER')
        
        # Initialize pygame first in this thread
        pygame.init()
        temp_screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Initializing...")
        temp_screen.fill((0, 0, 0))
        pygame.display.flip()
        
        # Brief pause to ensure window is created
        time.sleep(0.5)
        
        # Now run the game
        run_game()

if __name__ == "__main__":
    main()