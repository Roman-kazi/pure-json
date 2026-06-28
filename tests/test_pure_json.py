import pytest
from pure_json import extract, extract_all, JSONExtractionError, JSONHealingError, JSONValidationError

def test_clean_json():
    text = '{"key": "value"}'
    assert extract(text) == {"key": "value"}

def test_markdown_wrapped_json():
    text = '''```json
{
    "key": "value"
}
```'''
    assert extract(text) == {"key": "value"}

def test_conversational_fluff():
    text = 'Sure! Here is the output:\n{"status": "ok"}\nLet me know if you need anything else!'
    assert extract(text) == {"status": "ok"}

def test_string_with_braces_inside():
    # Boundary detection shouldn't break if a string value contains a curly brace
    text = 'Fluff {"expr": "a { b } c"} Fluff'
    assert extract(text) == {"expr": "a { b } c"}

def test_trailing_comma():
    text = '{"a": 1, "b": 2,}'
    assert extract(text) == {"a": 1, "b": 2}
    
def test_trailing_comma_array():
    text = '[1, 2, 3,]'
    assert extract(text) == [1, 2, 3]

def test_boolean_and_null_healing():
    text = '{"is_active": True, "value": None, "deleted": False}'
    assert extract(text) == {"is_active": True, "value": None, "deleted": False}
    
def test_strict_mode():
    text = '{"a": 1,}'
    with pytest.raises(JSONHealingError, match="Strict mode enabled"):
        extract(text, strict=True)

def test_invalid_bounds():
    text = 'This is just a string with no JSON'
    with pytest.raises(JSONExtractionError):
        extract(text)

def test_healing_failure():
    text = '{"a": 1, "b": UnquotedString}'
    with pytest.raises(JSONHealingError, match="Failed to parse JSON even after healing"):
        extract(text)

def test_single_quotes():
    text = "{'key': 'value', 'escaped': 'it\\'s fine'}"
    assert extract(text) == {"key": "value", "escaped": "it's fine"}

def test_unquoted_keys():
    text = '{key: "value", _id123: 1}'
    assert extract(text) == {"key": "value", "_id123": 1}

def test_single_quotes_and_unquoted_keys():
    text = "{status: 'ok', msg: 'all good'}"
    assert extract(text) == {"status": "ok", "msg": "all good"}

def test_extract_all_multiple_blocks():
    text = 'Here is block 1: {"id": 1} And block 2: [1, 2, 3] and finally {"a": "b"}'
    results = extract_all(text)
    assert len(results) == 3
    assert results[0] == {"id": 1}
    assert results[1] == [1, 2, 3]
    assert results[2] == {"a": "b"}

def test_schema_validation_success():
    text = '{"name": "Alice", "age": 30}'
    assert extract(text, required_keys=["name"]) == {"name": "Alice", "age": 30}

def test_schema_validation_missing_keys():
    text = '{"name": "Alice"}'
    with pytest.raises(JSONValidationError, match="Missing required keys: \\['age'\\]"):
        extract(text, required_keys=["name", "age"])

def test_state_machine_safety():
    # Ensuring { inside strings don't break the extractor
    text = 'Fluff {"key": "{ fake start"} Fluff'
    assert extract(text) == {"key": "{ fake start"}
