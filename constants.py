"""Constants module with type annotations and docstrings.
Uses unusual registry for creative centralized management.
"""

from __future__ import annotations

from typing import Final, Dict, Tuple, Any, List

import math

import datetime

# Registry of constants with values and docs
CONSTANT_REGISTRY: Final[Dict[str, Tuple[Any, str]]] = {
    "PI": (math.pi, "The mathematical constant pi"),
    "E": (math.e, "Base of the natural logarithm"),
    "GOLDEN_RATIO": ((1 + math.sqrt(5)) / 2, "Golden ratio phi"),
    "MAX_RETRIES": (5, "Maximum retry attempts for failed ops"),
    "DEFAULT_TIMEOUT": (30.0, "Default timeout seconds for tasks"),
    "EMPTY_LIST": ([], "Empty list for default values"),
    "NULL": (None, "Null constant representing absence"),
    "TRUE": (True, "True boolean constant"),
    "ZERO": (0, "Zero integer constant"),
    "CURRENT_YEAR": (datetime.datetime.now().year, "Year at module load time"),
}

PI: Final[float] = CONSTANT_REGISTRY["PI"][0]
E: Final[float] = CONSTANT_REGISTRY["E"][0]
GOLDEN_RATIO: Final[float] = CONSTANT_REGISTRY["GOLDEN_RATIO"][0]
MAX_RETRIES: Final[int] = CONSTANT_REGISTRY["MAX_RETRIES"][0]
DEFAULT_TIMEOUT: Final[float] = CONSTANT_REGISTRY["DEFAULT_TIMEOUT"][0]
EMPTY_LIST: Final[List[Any]] = CONSTANT_REGISTRY["EMPTY_LIST"][0]
NULL: Final[None] = CONSTANT_REGISTRY["NULL"][0]
TRUE: Final[bool] = CONSTANT_REGISTRY["TRUE"][0]
ZERO: Final[int] = CONSTANT_REGISTRY["ZERO"][0]
CURRENT_YEAR: Final[int] = CONSTANT_REGISTRY["CURRENT_YEAR"][0]

def get_constant(name: str) -> Any:
    """Retrieve a constant's value using its name.
    This allows dynamic access to the registry.

    Args:
        name: Name of the constant.

    Returns:
        The constant value.

    Raises:
        KeyError: If name is unknown.
    """
    if name not in CONSTANT_REGISTRY:
        raise KeyError(f"Constant '{name}' not found")
    return CONSTANT_REGISTRY[name][0]

def get_constant_doc(name: str) -> str:
    """Get documentation for a constant.
    Args:
        name: The constant name.

    Returns:
        Docstring for the constant.

    Raises:
        KeyError: If constant missing.
    """
    if name not in CONSTANT_REGISTRY:
        raise KeyError(f"Constant '{name}' not found")
    return CONSTANT_REGISTRY[name][1]
