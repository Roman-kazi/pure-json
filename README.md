# pure-json

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`pure-json` is a lightweight, zero-dependency Python library designed to extract, clean, and parse JSON from messy Large Language Model (LLM) string outputs. 

LLMs frequently return JSON surrounded by conversational fluff (e.g., "Here is your JSON:") or Markdown formatting (` ```json ... ``` `). Furthermore, they often make syntax errors like trailing commas, unquoted keys, or use single quotes (outputting Python dicts instead of valid JSON). `pure-json` acts as a middleware to automatically heal these issues so your pipelines don't break.

## Features

- **Fluff Stripping**: Automatically detects the outermost JSON bounds and ignores conversational text and Markdown blocks.
- **Auto-Healing**:
  - Removes trailing commas.
  - Converts unquoted Python types (`True`, `False`, `None`) to JSON literals (`true`, `false`, `null`).
  - Swaps single quotes (`'`) for double quotes (`"`).
  - Quotes unquoted keys (e.g., `{key: "value"}` -> `{"key": "value"}`).
- **Zero Dependencies**: Uses only the Python standard library.
- **Strict Mode**: Optional mode to fail fast on invalid JSON if you prefer to trigger an LLM retry instead of auto-healing.

## Installation

*(Note: Currently in development. Will be available on PyPI soon.)*

```bash
pip install pure-json
```

## Quick Start

```python
from pure_json import extract

messy_output = """
Sure! Here is the output you requested:
```json
{
  'status': "success",
  error_code: None,
  "data": [1, 2, 3,]
}
```
Let me know if you need anything else!
"""

# Extract and auto-heal the JSON
parsed_data = extract(messy_output)
print(parsed_data)
# Output: {'status': 'success', 'error_code': None, 'data': [1, 2, 3]}
```

## API Reference

### `extract(text: str, strict: bool = False) -> Any`

**Arguments:**
- `text`: The raw string containing the JSON you want to extract.
- `strict`: If `True`, disables the auto-healer. The library will still strip conversational fluff and Markdown, but if the extracted string is not valid JSON, it will immediately raise a `JSONHealingError`.

**Returns:**
- The parsed JSON object (dict, list, etc.).

### Exceptions

- `JSONExtractionError`: Raised when the library cannot locate valid JSON boundaries (no `{...}` or `[...]` found).
- `JSONHealingError`: Raised when the library cannot parse the extracted text into valid JSON (either because strict mode is on, or because the auto-healer failed to fix the syntax errors).

## Handling Errors

It's recommended to catch these custom exceptions in your pipeline and use them to trigger a retry to the LLM.

```python
from pure_json import extract, JSONExtractionError, JSONHealingError

def process_llm_output(output):
    try:
        data = extract(output)
        return data
    except JSONExtractionError:
        print("LLM didn't return any JSON object.")
        # Trigger LLM retry...
    except JSONHealingError as e:
        print(f"LLM returned hopelessly invalid JSON: {e}")
        # Trigger LLM retry...
```
