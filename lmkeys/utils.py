"""Utility functions for LMDB key/value processing"""

from typing import Tuple, Optional


def format_key(key: bytes) -> str:
    """
    Format a key for display.
    Try to decode as UTF-8, otherwise display as hex.

    Args:
        key: Raw key bytes from LMDB

    Returns:
        Formatted string representation
    """
    try:
        return key.decode('utf-8')
    except UnicodeDecodeError:
        return f"0x{key.hex()}"


def get_value_type(value: bytes) -> str:
    """
    Determine the type of a value for display.

    Args:
        value: Raw value bytes from LMDB

    Returns:
        String describing the type (e.g., 'str', 'bytes', 'int')
    """
    if value is None:
        return "None"

    # Try to decode as UTF-8 string
    try:
        decoded = value.decode('utf-8')
        # Check if it's printable
        if decoded.isprintable() or all(c in '\n\r\t' for c in decoded if not c.isprintable()):
            return "str"
    except UnicodeDecodeError:
        pass

    # Try to interpret as integer
    if len(value) in (1, 2, 4, 8):
        try:
            # Check if it looks like a little-endian integer
            return "int/bytes"
        except Exception:
            pass

    # Default to bytes
    return "bytes"


def format_value_info(value: bytes) -> str:
    """
    Format value information for display.

    Args:
        value: Raw value bytes from LMDB

    Returns:
        Formatted string with type and size info
    """
    value_type = get_value_type(value)
    size = len(value)
    return f"{value_type} ({size} bytes)"
