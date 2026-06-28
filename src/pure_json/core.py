import json
from typing import Any
from .extractor import extract_json_bounds
from .healer import heal_json
from .exceptions import JSONExtractionError, JSONHealingError

def extract(text: str, strict: bool = False) -> Any:
    """
    Extracts and parses JSON from a potentially messy string.
    
    Args:
        text (str): The raw string containing JSON.
        strict (bool): If True, disables auto-healing and fails fast on invalid JSON.
        
    Returns:
        Any: The parsed JSON object (dict, list, etc.).
        
    Raises:
        JSONExtractionError: If no valid JSON boundaries are found.
        JSONHealingError: If the extracted string cannot be parsed as JSON.
    """
    extracted_text = extract_json_bounds(text)
    
    if strict:
        try:
            return json.loads(extracted_text)
        except json.JSONDecodeError as e:
            raise JSONHealingError(f"Strict mode enabled. Failed to parse JSON: {e}") from e
    else:
        healed_text = heal_json(extracted_text)
        try:
            return json.loads(healed_text)
        except json.JSONDecodeError as e:
            raise JSONHealingError(f"Failed to parse JSON even after healing: {e}\nHealed text: {healed_text}") from e
