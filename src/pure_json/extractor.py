from typing import List
from .exceptions import JSONExtractionError

def extract_all_json_bounds(text: str) -> List[str]:
    """
    Extracts all distinct top-level JSON objects/arrays from a larger string
    by using a character-level state machine.
    """
    blocks = []
    stack = []
    in_string = False
    escape_next = False
    start_idx = -1

    for i, char in enumerate(text):
        if escape_next:
            escape_next = False
            continue
        
        if char == '\\' and in_string:
            escape_next = True
            continue
            
        if char == '"':
            in_string = not in_string
            continue
            
        if not in_string:
            if char in '{[':
                if not stack:
                    start_idx = i
                stack.append(char)
            elif char in '}]':
                if stack:
                    expected = '{' if char == '}' else '['
                    if stack[-1] == expected:
                        stack.pop()
                        if not stack:
                            blocks.append(text[start_idx:i+1])
                    else:
                        # Mismatched bracket, we just ignore and continue
                        # It could be invalid JSON or text mimicking JSON
                        pass

    return blocks

def extract_json_bounds(text: str) -> str:
    """
    Extracts the first valid JSON payload from a larger string.
    """
    blocks = extract_all_json_bounds(text)
    if not blocks:
        raise JSONExtractionError("Could not find any JSON object or array bounds in the string.")
    return blocks[0]
