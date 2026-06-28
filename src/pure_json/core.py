import json
from typing import Any, List, Optional
from .extractor import extract_json_bounds, extract_all_json_bounds
from .healer import heal_json
from .exceptions import JSONExtractionError, JSONHealingError, JSONValidationError

def _validate_schema(parsed: Any, required_keys: Optional[List[str]]) -> None:
    if required_keys:
        if not isinstance(parsed, dict):
            raise JSONValidationError(f"Schema validation failed: Expected a JSON object (dict), got {type(parsed).__name__}")
        missing = [k for k in required_keys if k not in parsed]
        if missing:
            raise JSONValidationError(f"Schema validation failed: Missing required keys: {missing}")

def extract(text: str, strict: bool = False, required_keys: Optional[List[str]] = None) -> Any:
    """
    Extracts and parses the first JSON block from a potentially messy string.
    
    Args:
        text (str): The raw string containing JSON.
        strict (bool): If True, disables auto-healing and fails fast on invalid JSON.
        required_keys (list): If provided, validates that the parsed JSON is a dict containing these keys.
        
    Returns:
        Any: The parsed JSON object (dict, list, etc.).
        
    Raises:
        JSONExtractionError: If no valid JSON boundaries are found.
        JSONHealingError: If the extracted string cannot be parsed as JSON.
        JSONValidationError: If the parsed JSON is missing required keys.
    """
    extracted_text = extract_json_bounds(text)
    
    if strict:
        try:
            parsed = json.loads(extracted_text)
        except json.JSONDecodeError as e:
            raise JSONHealingError(f"Strict mode enabled. Failed to parse JSON: {e}") from e
    else:
        healed_text = heal_json(extracted_text)
        try:
            parsed = json.loads(healed_text)
        except json.JSONDecodeError as e:
            raise JSONHealingError(f"Failed to parse JSON even after healing: {e}\nHealed text: {healed_text}") from e
            
    _validate_schema(parsed, required_keys)
    return parsed

def extract_all(text: str, strict: bool = False) -> List[Any]:
    """
    Extracts and parses all JSON blocks from a potentially messy string.
    
    Args:
        text (str): The raw string containing JSON blocks.
        strict (bool): If True, disables auto-healing and fails fast on invalid JSON.
        
    Returns:
        List[Any]: A list of all parsed JSON objects found in the string.
    """
    blocks = extract_all_json_bounds(text)
    results = []
    
    for extracted_text in blocks:
        if strict:
            try:
                results.append(json.loads(extracted_text))
            except json.JSONDecodeError as e:
                raise JSONHealingError(f"Strict mode enabled. Failed to parse JSON block: {e}") from e
        else:
            healed_text = heal_json(extracted_text)
            try:
                results.append(json.loads(healed_text))
            except json.JSONDecodeError as e:
                raise JSONHealingError(f"Failed to parse JSON block even after healing: {e}\nHealed text: {healed_text}") from e
                
    return results
