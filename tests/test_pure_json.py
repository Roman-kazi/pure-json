import pytest
from pure_json import extract, JSONExtractionError, JSONHealingError

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
