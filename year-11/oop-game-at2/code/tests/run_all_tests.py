#!/usr/bin/env python3
"""
Script to run all tests for the game.
"""

import unittest
import os
import sys
import importlib

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests(verbosity=2):
    """
    Run all test cases in the tests directory.
    
    Args:
        verbosity: Level of test output verbosity (1-3)
    """
    # Discover all tests in the current directory
    loader = unittest.TestLoader()
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(tests_dir)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Print summary
    print("\nTest Summary:")
    print(f"  Ran {result.testsRun} tests")
    print(f"  {len(result.errors)} errors")
    print(f"  {len(result.failures)} failures")
    print(f"  {len(result.skipped)} skipped")
    
    # Return the result to allow CI integration
    return result

def print_test_info():
    """
    Print information about the available test modules.
    """
    test_modules = []
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List all test files
    print("\nAvailable Test Modules:")
    for file in sorted(os.listdir(tests_dir)):
        if file.startswith('test_') and file.endswith('.py'):
            module_name = file[:-3]
            print(f"  - {module_name}")
            test_modules.append(module_name)
    
    print("\nTo run a specific test module:")
    print(f"  python3 -m tests.{test_modules[0]}")
    print("\nTo run all tests:")
    print("  python3 -m tests.run_all_tests")

if __name__ == "__main__":
    # Get verbosity from command line argument if provided
    verbosity = 2  # Default verbosity
    show_info = False
    
    for arg in sys.argv[1:]:
        if arg == '--info' or arg == '-i':
            show_info = True
        elif arg.isdigit():
            verbosity = int(arg)
        elif arg == '--help' or arg == '-h':
            print("Usage: python -m tests.run_all_tests [verbosity] [--info/-i] [--help/-h]")
            print("  verbosity: Set test verbosity (1-3, default is 2)")
            print("  --info, -i: Show information about available test modules")
            print("  --help, -h: Show this help message")
            sys.exit(0)
    
    if show_info:
        print_test_info()
    
    # Run tests
    print("Running all tests in the OOP Dungeon Game...")
    print("=" * 70)
    result = run_tests(verbosity)
    
    # Set exit code based on test result (for CI pipelines)
    sys.exit(not result.wasSuccessful())