# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python compatibility layer for executing Deluge scripts within Python, primarily for testing purposes. The project translates Deluge language syntax to Python and provides a runtime environment with Deluge-compatible data types and functions.

## Development Commands

All commands should be run using `uv` as the package manager:

- **Install dependencies**: `uv add <dependency>`
- **Run scripts**: `uv run <script or command>`
- **Run tests**: `uv run pytest`
- **Run specific tests**: `uv run pytest tests/test_showcase.py -v`
- **Build package**: `uv build`
- **Install in development mode**: `uv pip install -e .`

## Project Structure

- `src/deluge_compat/`: Main package source code
  - `__init__.py`: Package entry point and main API
  - `types.py`: Deluge data types (Map, List, DelugeString) with their methods
  - `functions.py`: Built-in Deluge functions (HTTP, encoding, math, etc.)
  - `translator.py`: Deluge to Python syntax translator
  - `runtime.py`: Script execution environment
  - `py.typed`: Type hint support indicator
- `tests/`: Comprehensive test suite with 102+ tests
  - `test_types.py`: Data type testing
  - `test_functions.py`: Built-in function testing
  - `test_runtime.py`: Script execution testing
  - `test_translator.py`: Syntax translation testing
  - `test_integration.py`: End-to-end scenarios
  - `test_showcase.py`: Working feature demonstrations
- `examples/`: Usage examples and legacy test scripts
- `pyproject.toml`: Project configuration using hatchling build backend
- `pytest.ini`: Test configuration
- `README.md`: Comprehensive project documentation

## Architecture Notes

The compatibility layer consists of four main components:

1. **Types Module**: Implements Deluge's Map, List, and String types with all their specific methods
2. **Functions Module**: Provides built-in functions like getUrl, postUrl, base64Encode, etc.
3. **Translator**: Converts Deluge syntax (braces, semicolons) to Python syntax (colons, indentation)
4. **Runtime**: Manages script execution context and handles return values

Key design decisions:
- Uses Python 3.12+ for modern type hints and features
- Translates Deluge scripts to Python rather than interpreting directly
- Maintains compatibility with Deluge's method names and behavior
- Wraps execution in functions to handle return statements properly
- Comprehensive test coverage validates functionality

## Common Development Tasks

- **Adding new Deluge functions**: Add to `functions.py` and update `BUILTIN_FUNCTIONS` dict
- **Extending data types**: Add methods to respective classes in `types.py`
- **Improving translation**: Modify `translator.py` for better syntax handling
- **Testing**: Create tests in `tests/` directory and run with `uv run pytest`
- **Examples**: Add usage examples to `examples/` directory

## Test Coverage

The project includes 102+ tests covering:
- All data types and their methods
- All built-in functions
- Script execution scenarios
- Error handling
- Performance with large datasets
- Integration scenarios

Run tests with:
```bash
uv run pytest                    # All tests
uv run pytest tests/test_types.py -v    # Specific module
uv run pytest tests/test_showcase.py    # Working features
```

## Known Limitations

- Complex nested conditionals may not translate correctly due to brace handling
- Some advanced invokeurl features are simplified
- Error messages differ from native Deluge format
- Performance characteristics may vary from native Deluge execution

## Status

✅ **Fully Working**: Data types, built-in functions, simple scripts, string operations, mathematical operations, encoding/decoding

⚠️ **Limited Support**: Complex nested conditionals, advanced control flow (due to translator limitations)

The core functionality is solid and covers most common Deluge language features for testing purposes.