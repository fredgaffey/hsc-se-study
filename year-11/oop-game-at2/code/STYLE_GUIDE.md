# Code Style Guide

This document outlines the code style standards for the 11AT2-OOP project.

## General Guidelines

- Follow PEP 8 style guide for Python code.
- Use 4 spaces for indentation (no tabs).
- Maximum line length: 100 characters.
- Use blank lines to separate logical sections of code.
- End files with a single newline.
- No trailing whitespace.

## Naming Conventions

- Classes: Use `CapWords` convention (e.g., `GameObject`, `Player`).
- Methods and variables: Use `lowercase_with_underscores`.
- Constants: Use `UPPERCASE_WITH_UNDERSCORES`.
- Private methods/attributes: Prefix with a single underscore (e.g., `_private_method`).
- Be descriptive with naming - avoid single-letter variables except for well-understood cases like:
  - `x`, `y` for coordinates
  - `i`, `j` for loop indices
  - `dx`, `dy` for direction/delta values

## Imports

Order imports as follows, with a blank line between each group:
1. Standard library imports
2. Third-party imports
3. Local/application imports

```python
# Standard library
import os
import sys
import math

# Third-party
import pygame

# Local
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from core.game_object import GameObject
```

- Do not use wildcard imports (e.g., `from utils.constants import *`).
- Group related imports on a single line when appropriate.

## Docstrings

Use Google-style docstrings:

```python
def function_name(param1, param2):
    """Short description of function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When/why this exception is raised
    """
```

- All modules should have a module-level docstring.
- All classes should have a class-level docstring.
- All public methods should have docstrings with parameters and return values documented.
- Private methods should have docstrings when their purpose isn't immediately clear.

## Comments

- Use comments to explain complex logic or non-obvious code.
- Use section comments to divide large code blocks:

```python
# --- Game initialisation ---
```

- Avoid comments that simply restate what the code does.
- Comments should explain why, not what.

## Error Handling

- Use try/except blocks to handle specific exceptions, not to catch all exceptions.
- Provide meaningful error messages.
- Use the logging module for error reporting instead of print statements.

```python
try:
    file = open(filename)
except FileNotFoundError:
    logger.error(f"Could not find file: {filename}")
```

## Logging

- Use the utils.logger module for all logging.
- Prefer structured logging messages over string concatenation.
- Use appropriate log levels:
  - DEBUG: Detailed information, typically useful only for diagnosing problems
  - INFO: Confirmation that things are working as expected
  - WARNING: Indication that something unexpected happened, but the program still works
  - ERROR: Due to a more serious problem, the program has not been able to perform a function
  - CRITICAL: A serious error, indicating that the program itself may be unable to continue running

## Type Hints

While not required, type hints are encouraged for function signatures:

```python
def calculate_distance(point1: tuple[int, int], point2: tuple[int, int]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
```

## Tools

Consider using these tools to help maintain code style:
- `black` for code formatting
- `isort` for import sorting
- `flake8` for style guide enforcement
- `pylint` for code analysis

