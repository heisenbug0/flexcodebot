"""
Utility functions for FlexCode Bot.

This module contains helper functions for common operations like
text processing, validation, and data transformation.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import hashlib
import json

from .logger import get_logger

logger = get_logger(__name__)


def clean_text(text: str) -> str:
    """
    Clean and normalize text input.
    
    Args:
        text: Raw text input
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters that might interfere with processing
    text = re.sub(r'[^\w\s@#.-]', '', text)
    
    return text


def extract_mentions(text: str) -> List[str]:
    """
    Extract @mentions from text.
    
    Args:
        text: Text containing mentions
        
    Returns:
        List of mentioned usernames (without @)
    """
    mentions = re.findall(r'@(\w+)', text)
    return list(set(mentions))  # Remove duplicates


def extract_hashtags(text: str) -> List[str]:
    """
    Extract #hashtags from text.
    
    Args:
        text: Text containing hashtags
        
    Returns:
        List of hashtags (without #)
    """
    hashtags = re.findall(r'#(\w+)', text)
    return list(set(hashtags))  # Remove duplicates


def validate_betting_code(code: str) -> bool:
    """
    Validate betting code format.
    
    Args:
        code: Betting code to validate
        
    Returns:
        True if code format is valid, False otherwise
    """
    if not code:
        return False
    
    # Basic validation: alphanumeric, 4-15 characters
    pattern = r'^[A-Z0-9]{4,15}$'
    return bool(re.match(pattern, code.upper()))


def validate_platform_name(platform: str) -> bool:
    """
    Validate platform name.
    
    Args:
        platform: Platform name to validate
        
    Returns:
        True if platform name is valid, False otherwise
    """
    if not platform:
        return False
    
    # Platform names should be alphabetic with possible spaces/hyphens
    pattern = r'^[a-zA-Z][a-zA-Z0-9\s\-]{1,20}$'
    return bool(re.match(pattern, platform))


def format_conversion_result(
    original_code: str,
    original_platform: str,
    target_platform: str,
    converted_code: Optional[str],
    message: str = ""
) -> str:
    """
    Format conversion result for display.
    
    Args:
        original_code: Original betting code
        original_platform: Original platform name
        target_platform: Target platform name
        converted_code: Converted code (None if failed)
        message: Additional message
        
    Returns:
        Formatted result string
    """
    if converted_code:
        result = f"{original_platform} {original_code} → {target_platform}: {converted_code}"
        if message:
            result += f" ({message})"
    else:
        result = f"{original_platform} {original_code}: Conversion failed"
        if message:
            result += f" - {message}"
    
    return result


def truncate_message(message: str, max_length: int = 280) -> str:
    """
    Truncate message to fit within character limit.
    
    Args:
        message: Message to truncate
        max_length: Maximum allowed length
        
    Returns:
        Truncated message
    """
    if len(message) <= max_length:
        return message
    
    # Truncate and add ellipsis
    return message[:max_length - 3] + "..."


def generate_request_id() -> str:
    """
    Generate unique request ID for tracking.
    
    Returns:
        Unique request ID
    """
    timestamp = datetime.now().isoformat()
    hash_input = f"{timestamp}{id(object())}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:8]


def parse_conversion_pairs(text: str) -> List[Dict[str, Any]]:
    """
    Parse text to extract conversion pairs using regex patterns.
    
    Args:
        text: Input text to parse
        
    Returns:
        List of conversion pair dictionaries
    """
    pairs = []
    
    # Pattern: "convert [platform] code [code] to [platform]"
    pattern1 = r'convert\s+(\w+)\s+code\s+([A-Z0-9]+)\s+to\s+(\w+)'
    matches1 = re.finditer(pattern1, text, re.IGNORECASE)
    
    for match in matches1:
        pairs.append({
            'original_platform': match.group(1).title(),
            'code': match.group(2).upper(),
            'target_platform': match.group(3).title()
        })
    
    # Pattern: "[platform] [code] to [platform]"
    pattern2 = r'(\w+)\s+([A-Z0-9]+)\s+to\s+(\w+)'
    matches2 = re.finditer(pattern2, text, re.IGNORECASE)
    
    for match in matches2:
        # Skip if already found by pattern1
        code = match.group(2).upper()
        if not any(p['code'] == code for p in pairs):
            pairs.append({
                'original_platform': match.group(1).title(),
                'code': code,
                'target_platform': match.group(3).title()
            })
    
    return pairs


def sanitize_user_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: User input text
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\';\\]', '', text)
    
    # Limit length
    text = text[:1000]
    
    # Clean whitespace
    text = clean_text(text)
    
    return text


def format_error_message(error: Exception, user_friendly: bool = True) -> str:
    """
    Format error message for logging or user display.
    
    Args:
        error: Exception object
        user_friendly: Whether to return user-friendly message
        
    Returns:
        Formatted error message
    """
    if user_friendly:
        # Generic user-friendly messages
        error_type = type(error).__name__
        if error_type in ['ConnectionError', 'Timeout', 'RequestException']:
            return "Service temporarily unavailable. Please try again later."
        elif error_type in ['ValidationError', 'ValueError']:
            return "Invalid input format. Please check your request and try again."
        else:
            return "An error occurred while processing your request. Please try again."
    else:
        # Detailed error for logging
        return f"{type(error).__name__}: {str(error)}"


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two text strings.
    
    Args:
        text1: First text string
        text2: Second text string
        
    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0
    
    # Simple character-based similarity
    text1_clean = clean_text(text1.lower())
    text2_clean = clean_text(text2.lower())
    
    if text1_clean == text2_clean:
        return 1.0
    
    # Calculate Jaccard similarity using character n-grams
    def get_ngrams(text: str, n: int = 2) -> set:
        return set(text[i:i+n] for i in range(len(text) - n + 1))
    
    ngrams1 = get_ngrams(text1_clean)
    ngrams2 = get_ngrams(text2_clean)
    
    if not ngrams1 and not ngrams2:
        return 1.0
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = len(ngrams1.intersection(ngrams2))
    union = len(ngrams1.union(ngrams2))
    
    return intersection / union if union > 0 else 0.0


def batch_process(items: List[Any], batch_size: int = 10) -> List[List[Any]]:
    """
    Split items into batches for processing.
    
    Args:
        items: List of items to batch
        batch_size: Size of each batch
        
    Returns:
        List of batches
    """
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """
    Safely parse JSON string with fallback.
    
    Args:
        json_str: JSON string to parse
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        logger.warning(f"Failed to parse JSON: {json_str}")
        return default


def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    """
    Safely serialize object to JSON string.
    
    Args:
        obj: Object to serialize
        default: Default JSON string if serialization fails
        
    Returns:
        JSON string or default value
    """
    try:
        return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    except (TypeError, ValueError):
        logger.warning(f"Failed to serialize object to JSON: {type(obj)}")
        return default