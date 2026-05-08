from typing import Any, Dict
import re
import uuid

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_uuid(value: str) -> bool:
    """Validate UUID format"""
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove special characters that could be harmful
    dangerous_chars = ['<', '>', '"', "'", ';', '--', '/*', '*/']
    for char in dangerous_chars:
        text = text.replace(char, '')
    return text.strip()

def validate_pagination(skip: int, limit: int, max_limit: int = 100) -> tuple:
    """Validate pagination parameters"""
    skip = max(0, skip)
    limit = min(max(1, limit), max_limit)
    return skip, limit
