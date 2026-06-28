import re
import logging

logger = logging.getLogger("pure_json.healer")

def heal_json(text: str) -> str:
    """
    Applies heuristics to auto-heal common JSON syntax errors in LLM outputs.
    """
    original_text = text
    
    # 1. Fix trailing commas before closing braces/brackets
    pattern_comma = r',\s*(?=[\]}])'
    if re.search(pattern_comma, text):
        text = re.sub(pattern_comma, '', text)
        logger.debug("Healed trailing comma(s).")
        
    # 2. Fix unquoted Python booleans and None
    replacements = [
        (r'(:\s*|,\s*|\[\s*)True\b', r'\g<1>true', 'True -> true'),
        (r'(:\s*|,\s*|\[\s*)False\b', r'\g<1>false', 'False -> false'),
        (r'(:\s*|,\s*|\[\s*)None\b', r'\g<1>null', 'None -> null'),
    ]
    
    for pattern, repl, desc in replacements:
        if re.search(pattern, text):
            text = re.sub(pattern, repl, text)
            logger.debug(f"Healed: {desc}")
            
    if text != original_text:
        logger.info("JSON auto-healing applied.")
        
    return text
