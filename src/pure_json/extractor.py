def extract_json_bounds(text: str) -> str:
    """
    Extracts the JSON payload from a larger string, stripping away conversational
    fluff and Markdown formatting.
    """
    first_brace = text.find('{')
    first_bracket = text.find('[')
    
    if first_brace == -1 and first_bracket == -1:
        from .exceptions import JSONExtractionError
        raise JSONExtractionError("Could not find any JSON object or array bounds in the string.")
    
    # Determine which boundary comes first
    if first_brace != -1 and (first_bracket == -1 or first_brace < first_bracket):
        # Object is first
        last_brace = text.rfind('}')
        if last_brace == -1 or last_brace < first_brace:
            from .exceptions import JSONExtractionError
            raise JSONExtractionError("Found opening '{' but no closing '}'.")
        return text[first_brace:last_brace + 1]
    else:
        # Array is first
        last_bracket = text.rfind(']')
        if last_bracket == -1 or last_bracket < first_bracket:
            from .exceptions import JSONExtractionError
            raise JSONExtractionError("Found opening '[' but no closing ']'.")
        return text[first_bracket:last_bracket + 1]
