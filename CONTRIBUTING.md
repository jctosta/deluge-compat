# Contributing to Deluge Compatibility Layer

Thank you for your interest in contributing to the Deluge Compatibility Layer! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Development Workflow](#development-workflow)
- [Testing Guidelines](#testing-guidelines)
- [Code Style](#code-style)
- [Documentation](#documentation)

## Important Notice

**Deluge Language**: Deluge is a proprietary scripting language owned by Zoho Corporation. This project is an independent compatibility layer and is not affiliated with Zoho Corporation. Contributors should respect all intellectual property rights.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Be collaborative and professional
- Respect different viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone git@github.com:YOUR_USERNAME/deluge-compat.git
   cd deluge-compat
   ```

3. **Set up the development environment**:
   ```bash
   # Install dependencies using uv
   uv install
   
   # Install in editable mode for development
   uv pip install -e .
   ```

4. **Set up the upstream remote**:
   ```bash
   git remote add upstream git@github.com:jctosta/deluge-compat.git
   ```

5. **Verify the setup**:
   ```bash
   # Run the test suite
   uv run pytest
   
   # Should show 115/115 tests passing
   ```

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes** - Fix issues in existing functionality
- **Feature additions** - Add new Deluge functions or data type methods
- **Documentation improvements** - Enhance README, docstrings, or examples
- **Test improvements** - Add test coverage or improve existing tests
- **Performance optimizations** - Improve execution speed or memory usage
- **Translation improvements** - Enhance the Deluge-to-Python translator

### Before You Start

1. **Check existing issues** to see if your contribution is already being worked on
2. **Create an issue** for new features or significant changes to discuss the approach
3. **Start small** - consider beginning with documentation or small bug fixes
4. **Review the codebase** to understand the project structure and patterns

## Pull Request Process

### 1. Create a Feature Branch

```bash
# Make sure you're on main and up to date
git checkout main
git pull upstream main

# Create a new branch for your feature/fix
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Your Changes

- Follow the existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Test Your Changes

```bash
# Run the full test suite
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test categories
uv run pytest tests/test_types.py
uv run pytest tests/test_functions.py
uv run pytest tests/test_translator.py
```

### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add support for new Deluge string method"
```

**Commit Message Guidelines:**
- Use the imperative mood ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Include a detailed description if needed
- Reference issue numbers when applicable

### 5. Push and Create Pull Request

```bash
# Push your branch to your fork
git push origin feature/your-feature-name
```

1. Go to GitHub and create a pull request
2. Fill out the pull request template
3. Link to any related issues
4. Wait for review and address feedback

### Pull Request Checklist

- [ ] Tests pass (`uv run pytest`)
- [ ] Code follows existing style patterns
- [ ] Documentation updated if needed
- [ ] Changelog updated for significant changes
- [ ] Pull request has a clear title and description
- [ ] Related issues are linked

## Issue Guidelines

### Bug Reports

When reporting bugs, please include:

- **Python version** and operating system
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Error messages** or stack traces
- **Minimal code example** that demonstrates the issue

### Feature Requests

When requesting features, please include:

- **Description** of the proposed feature
- **Use case** - why is this feature needed?
- **Example** of how it would be used
- **Deluge compatibility** - reference to official Deluge documentation if applicable

### Questions

For questions about usage:
- Check the README and examples first
- Search existing issues
- Create a new issue with the "question" label

## Development Workflow

### Project Structure

```
deluge-compat/
├── src/deluge_compat/
│   ├── __init__.py          # Main API exports
│   ├── types.py             # Deluge data types (Map, List, DelugeString)
│   ├── functions.py         # Built-in functions (HTTP, encoding, math)
│   ├── translator.py        # Deluge → Python syntax translator
│   └── runtime.py           # Script execution environment
├── tests/                   # Test suite (115 tests)
│   ├── test_types.py        # Data type tests
│   ├── test_functions.py    # Built-in function tests
│   ├── test_translator.py   # Translation tests
│   ├── test_runtime.py      # Runtime execution tests
│   ├── test_integration.py  # Integration scenarios
│   └── test_showcase.py     # Feature demonstrations
├── examples/                # Usage examples
├── LICENSE                  # MIT License
├── README.md               # Project documentation
├── CONTRIBUTING.md         # This file
└── pyproject.toml          # Project configuration
```

### Key Components

1. **Types Module** (`src/deluge_compat/types.py`)
   - Implements `Map`, `List`, and `DelugeString` classes
   - Each class provides Deluge-specific methods
   - Handles type conversion and compatibility

2. **Functions Module** (`src/deluge_compat/functions.py`)
   - HTTP functions: `getUrl()`, `postUrl()`
   - Encoding functions: `base64Encode()`, `aesEncode()`, etc.
   - Math functions: `abs()`, `sqrt()`, `power()`, etc.
   - Utility functions: `info()`, `ifnull()`, etc.

3. **Translator** (`src/deluge_compat/translator.py`)
   - Converts Deluge syntax to Python syntax
   - Handles control structures, method calls, assignments
   - Manages indentation and code structure

4. **Runtime** (`src/deluge_compat/runtime.py`)
   - Executes translated Python code
   - Manages execution context and variables
   - Provides error handling and debugging

## Testing Guidelines

### Test Structure

- **Unit tests** - Test individual components in isolation
- **Integration tests** - Test complete scenarios and workflows
- **Showcase tests** - Demonstrate working features and serve as examples

### Writing Tests

```python
def test_new_feature():
    """Test description explaining what this test validates."""
    # Arrange - set up test data
    script = '''
    // Deluge code to test
    result = someFunction();
    return result;
    '''
    
    # Act - execute the test
    result = run_deluge_script(script)
    
    # Assert - verify the results
    assert result is not None
    assert isinstance(result, expected_type)
```

### Test Categories

1. **types.py tests** - Verify data type methods work correctly
2. **functions.py tests** - Verify built-in functions work correctly
3. **translator.py tests** - Verify syntax translation is accurate
4. **runtime.py tests** - Verify script execution works correctly
5. **integration tests** - Verify complete workflows work end-to-end

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=deluge_compat

# Run specific test file
uv run pytest tests/test_types.py -v

# Run tests matching a pattern
uv run pytest -k "test_string"
```

## Code Style

### Python Style Guidelines

- Follow **PEP 8** style guidelines
- Use **type hints** for function parameters and return values
- Write **descriptive docstrings** for all public methods
- Use **meaningful variable names**
- Keep functions focused and single-purpose

### Example Code Style

```python
def translate_condition(self, condition: str) -> str:
    """Translate condition expressions from Deluge to Python.
    
    Args:
        condition: The Deluge condition expression to translate
        
    Returns:
        The translated Python condition expression
    """
    # Handle method calls
    condition = self._translate_string_methods(condition)
    
    # Handle logical operators
    condition = condition.replace('&&', ' and ')
    condition = condition.replace('||', ' or ')
    
    return condition
```

### Documentation Style

- Use **clear, concise docstrings**
- Include **parameter descriptions** and **return value descriptions**
- Provide **usage examples** for complex functions
- Keep **line length under 88 characters**

## Documentation

### Types of Documentation

1. **Code documentation** - Docstrings in the code
2. **README.md** - Project overview and usage guide
3. **Examples** - Working code examples in the `examples/` directory
4. **Test documentation** - Tests that serve as usage examples

### Documentation Guidelines

- **Be clear and concise** - avoid jargon when possible
- **Provide examples** - show how to use features
- **Keep it up to date** - update docs when code changes
- **Use proper formatting** - follow Markdown best practices

### Updating Documentation

When adding new features:

1. **Add docstrings** to new functions and classes
2. **Update README.md** if the feature affects the public API
3. **Add examples** demonstrating the new functionality
4. **Update test documentation** to cover new test cases

## Getting Help

If you need help with contributing:

1. **Check the documentation** - README.md and code comments
2. **Look at existing code** - see how similar features are implemented
3. **Run the tests** - understand how components work together
4. **Create an issue** - ask questions if you're stuck
5. **Start small** - begin with simple contributions to learn the codebase

## Recognition

Contributors will be recognized in:
- The project's contributor list
- Release notes for significant contributions
- Special recognition for major features or improvements

Thank you for contributing to the Deluge Compatibility Layer! Your contributions help make Deluge scripts more accessible and testable in Python environments.