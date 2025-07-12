# Deluge Compatibility Layer

A Python compatibility layer that allows you to execute Deluge scripts within Python environments. This project provides a runtime environment and translator that converts Deluge language syntax to Python, enabling testing and execution of Deluge scripts outside of their native environment.

## Features

- **Complete Data Type Support**: Implements Deluge's Map, List, and String types with all their methods
- **Built-in Functions**: HTTP requests, encoding/decoding, mathematical operations, and utility functions
- **Script Translation**: Converts Deluge syntax to executable Python code
- **Runtime Environment**: Provides a sandboxed execution context for Deluge scripts
- **Easy Integration**: Simple API for running Deluge scripts from Python

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd deluge-compat

# Install dependencies using uv
uv install

# Or install in development mode
uv pip install -e .
```

## Quick Start

### Basic Usage

```python
from deluge_compat import run_deluge_script

# Simple Deluge script
script = '''
response = Map();
response.put("greeting", "Hello World!");
response.put("timestamp", "2024-01-01");
return response;
'''

result = run_deluge_script(script)
print(result)  # {'greeting': 'Hello World!', 'timestamp': '2024-01-01'}
```

### String Operations

```python
script = '''
text = "Hello World";
result = Map();

result.put("original", text);
result.put("upper", text.toUpperCase());
result.put("length", text.length());
result.put("contains_world", text.contains("World"));

return result;
'''

result = run_deluge_script(script)
print(result['upper'])  # "HELLO WORLD"
```

### Working with Lists

```python
script = '''
numbers = List();
numbers.add(1);
numbers.add(2);
numbers.add(3);

sum = 0;
for each num in numbers {
    sum = sum + num;
}

result = Map();
result.put("numbers", numbers);
result.put("sum", sum);
return result;
'''

result = run_deluge_script(script)
print(result['sum'])  # 6
```

### HTTP Operations

```python
script = '''
url = "https://api.github.com/users/octocat";
response = getUrl(url);

result = Map();
result.put("url", url);
result.put("response_length", response.length());
result.put("success", response.length() > 0);

return result;
'''

result = run_deluge_script(script)
```

### Using Context Variables

```python
script = '''
greeting = "Hello " + username + "!";
result = Map();
result.put("message", greeting);
result.put("age_group", age >= 18 ? "adult" : "minor");
return result;
'''

result = run_deluge_script(script, username="Alice", age=25)
print(result['message'])  # "Hello Alice!"
```

## Supported Deluge Features

### Data Types

- **Map**: Key-value pairs with methods like `put()`, `get()`, `containKey()`, `keys()`
- **List**: Ordered collections with methods like `add()`, `size()`, `get()`, `sort()`
- **String**: Enhanced strings with Deluge-specific methods like `contains()`, `substring()`, `toUpperCase()`

### Built-in Functions

#### HTTP Functions
- `getUrl(url, simple)` - HTTP GET requests
- `postUrl(url, body, headers, simple)` - HTTP POST requests

#### Encoding Functions
- `base64Encode(text)` / `base64Decode(text)`
- `encodeUrl(url)` / `urlDecode(url)`
- `aesEncode(key, text)` / `aesDecode(key, encrypted)`

#### Mathematical Functions
- `abs(number)`, `cos(number)`, `sin(number)`, `tan(number)`
- `log(number)`, `exp(number)`, `sqrt(number)`
- `min(a, b)`, `max(a, b)`, `power(base, exp)`
- `randomNumber(max, min)`

#### Utility Functions
- `info(message)` - Logging
- `ifnull(value, default)` - Null checking
- Collection constructors: `Map()`, `List()`, `Collection()`

### Control Structures

- **Conditional statements**: `if`, `else if`, `else`
- **Loops**: `for each` loops
- **Function calls** and **return statements**

### String Methods

All Deluge string methods are supported:
- `contains()`, `startsWith()`, `endsWith()`
- `toUpperCase()`, `toLowerCase()`, `trim()`
- `substring()`, `indexOf()`, `lastIndexOf()`
- `replaceAll()`, `replaceFirst()`
- `toList()`, `toMap()`, `length()`
- And many more...

## Examples

### File Processing Example

```python
# examples/file_example.py
from deluge_compat import run_deluge_script

script = '''
// Process a list of files
files = List();
files.add("document.pdf");
files.add("image.jpg");
files.add("script.dg");

result = Map();
documents = List();
images = List();

for each file in files {
    if(file.contains(".pdf") || file.contains(".doc")) {
        documents.add(file);
    } else if(file.contains(".jpg") || file.contains(".png")) {
        images.add(file);
    }
}

result.put("documents", documents);
result.put("images", images);
result.put("total_files", files.size());

return result;
'''

result = run_deluge_script(script)
print(f"Found {len(result['documents'])} documents")
print(f"Found {len(result['images'])} images")
```

### API Integration Example

```python
script = '''
// Simulate API data processing
data = Map();
data.put("user_id", "12345");
data.put("email", "user@example.com");
data.put("status", "active");

// Process the data
processed = Map();
processed.put("id", data.get("user_id"));
processed.put("email_domain", data.get("email").getSuffix("@"));
processed.put("is_active", data.get("status").equals("active"));

// Create response
response = Map();
response.put("success", true);
response.put("data", processed);

return response;
'''

result = run_deluge_script(script)
```

## Testing

The project includes a comprehensive test suite with 100+ tests covering all major functionality.

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test categories
uv run pytest tests/test_types.py          # Test data types
uv run pytest tests/test_functions.py      # Test built-in functions  
uv run pytest tests/test_runtime.py        # Test script execution
uv run pytest tests/test_showcase.py       # Test working features

# Run legacy examples
uv run python examples/test_example.py
uv run python examples/http_example.py
```

### Test Coverage

- **102 passing tests** covering core functionality
- **Data Types**: Complete test coverage for Map, List, and DelugeString
- **Functions**: All built-in functions (HTTP, encoding, math, utilities)
- **Runtime**: Script execution, context variables, error handling
- **Integration**: End-to-end scenarios and performance tests
- **Showcase**: Demonstrations of working features

### Test Status

✅ **Fully Working**: Data types, built-in functions, simple scripts, string operations, mathematical operations, encoding/decoding

⚠️ **Limited Support**: Complex nested conditionals, advanced control flow (due to translator limitations)

❌ **Known Issues**: Some complex Deluge syntax patterns need translator improvements

## Project Structure

```
deluge-compat/
├── src/deluge_compat/
│   ├── __init__.py          # Main API
│   ├── types.py             # Deluge data types (Map, List, String)
│   ├── functions.py         # Built-in functions
│   ├── translator.py        # Deluge → Python translator
│   └── runtime.py           # Execution environment
├── examples/                # Usage examples
├── CLAUDE.md               # Development guidance
└── README.md               # This file
```

## Architecture

The compatibility layer consists of four main components:

1. **Types Module** (`types.py`): Implements Deluge's data types with their specific methods
2. **Functions Module** (`functions.py`): Provides all built-in Deluge functions
3. **Translator** (`translator.py`): Converts Deluge syntax to Python syntax
4. **Runtime** (`runtime.py`): Manages script execution and context

## Limitations

- Complex nested conditional statements may require manual adjustment
- Some advanced `invokeurl` block features are simplified
- Error messages may not match Deluge's native error format
- Performance may differ from native Deluge execution

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Development

### Setup

```bash
# Clone and setup
git clone <repository-url>
cd deluge-compat

# Install dependencies (pytest already included)
uv install

# Install in editable mode for development
uv pip install -e .
```

### Testing

```bash
# Run full test suite
uv run pytest

# Run with coverage
uv run pytest --cov=deluge_compat

# Run specific test files
uv run pytest tests/test_types.py -v

# Test working features showcase
uv run pytest tests/test_showcase.py -v
```

### Code Structure

- `src/deluge_compat/types.py` - Add new data type methods
- `src/deluge_compat/functions.py` - Add new built-in functions  
- `src/deluge_compat/translator.py` - Improve syntax translation
- `tests/` - Add tests for new functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the Deluge language specification and documentation
- Inspired by the [Deluge Language Parser](https://github.com/GuruDhanush/Deluge-Language-Parser) project
- Built with Python 3.12+ and modern tooling

---

**Note**: This is a compatibility layer for testing and development purposes. For production Deluge script execution, use the official Deluge runtime environment.