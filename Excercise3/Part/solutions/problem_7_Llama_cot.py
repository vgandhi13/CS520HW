from typing import List

def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """
    Filter a list of strings to keep only those that contain a given substring.

    Args:
    strings (List[str]): Input list of strings to filter.
    substring (str): Substring to filter by.

    Returns:
    List[str]: List of strings that contain the given substring.

    Raises:
    TypeError: If the input list or substring is not a string.
    """

    # Check if input list and substring are strings
    if not isinstance(strings, list) or not all(isinstance(s, str) for s in strings) or not isinstance(substring, str):
        raise TypeError("Input list and substring must be strings")

    # Use list comprehension to iterate through the list efficiently
    # The 'if substring in s' condition checks if the substring is present in each string
    # This is case-sensitive, meaning it treats uppercase and lowercase letters as distinct
    # If you want a case-insensitive match, consider converting both the substring and the strings to lowercase or uppercase
    return [s for s in strings if substring in s]
