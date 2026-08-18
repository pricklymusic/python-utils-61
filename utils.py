from typing import List, Optional
import random


def pick_random_element(elements: List[Optional[str]]) -> Optional[str]:
    """
    Picks a random element from a non-empty list of strings.

    Args:
        elements: A list that may contain strings or None values.

    Returns:
        A randomly selected string from the list, or None if the list is empty.
    """
    if not elements:
        return None
    return random.choice(elements)


def flatten_list(nested_list: List[List[Optional[int]]]) -> List[Optional[int]]:
    """
    Flattens a nested list of integers into a single list.

    Args:
        nested_list: A list of lists containing integers or None.

    Returns:
        A single flattened list containing the integers from the nested lists.
    """
    return [item for sublist in nested_list for item in sublist if item is not None]


def calculate_average(numbers: List[Optional[float]]) -> Optional[float]:
    """
    Calculates the average of a list of numbers, ignoring None values.

    Args:
        numbers: A list containing numbers or None.

    Returns:
        The average of the numbers, or None if there are no valid numbers.
    """
    valid_numbers = [num for num in numbers if num is not None]
    if not valid_numbers:
        return None
    return sum(valid_numbers) / len(valid_numbers)
