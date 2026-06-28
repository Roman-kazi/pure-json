class JSONExtractionError(Exception):
    """Raised when pure-json cannot locate valid JSON boundaries in the string."""
    pass

class JSONHealingError(Exception):
    """Raised when pure-json cannot auto-heal the JSON into a valid format."""
    pass

class JSONValidationError(Exception):
    """Raised when the parsed JSON does not contain the required schema keys."""
    pass

