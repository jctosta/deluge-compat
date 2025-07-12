"""Deluge Compatibility Layer for Python.

This module provides compatibility for running Deluge scripts in Python.
"""

from .runtime import DelugeRuntime
from .translator import DelugeTranslator
from .types import Map, List, DelugeString

__all__ = ["DelugeRuntime", "DelugeTranslator", "Map", "List", "DelugeString"]

def run_deluge_script(script: str, **context) -> any:
    """Execute a Deluge script string in Python.
    
    Args:
        script: The Deluge script code as a string
        **context: Additional variables to make available in the script context
        
    Returns:
        The result of executing the script
    """
    runtime = DelugeRuntime()
    runtime.update_context(context)
    return runtime.execute(script)
