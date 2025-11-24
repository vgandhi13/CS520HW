"""
Test file for HumanEval_7 (filter_by_substring) - Llama_cot variant
Part 2: LLM-generated tests to improve coverage

Add your LLM-generated unit tests below.
These tests should aim to improve code coverage beyond the baseline.
"""

from solutions.problem_7_Llama_cot import filter_by_substring
from collections import Counter


# TODO: Add your LLM-generated test cases here
# Example structure:
# def test_filter_by_substring_edge_case_1():
#     """Test description"""
#     result = filter_by_substring(["test", "strings"], "substring")
#     assert result == expected_output

# --- Old Tests From Excercise 2---
def test_filter_by_substring_standard(): #Iteration 1
    """Test standard filtering with multiple matches and non-matches."""
    result = filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    assert result == ['abc', 'bacd', 'array']

import pytest

def test_filter_by_substring_invalid_strings_type(): #Iteration 2
    """Test that a TypeError is raised when strings is not a list."""
    with pytest.raises(TypeError):
        filter_by_substring(strings=123, substring='a')








# --- Individual Specification Tests for Excercise 3---

def test_spec_1_strings_type_error():
    """
    Spec 1: A TypeError must be raised if 'strings' is not a list of strings.
    """
    # Case A: Input is not a list
    with pytest.raises(TypeError):
        filter_by_substring(strings=123, substring="abc")
    
    # Case B: Input is a list, but contains non-strings
    with pytest.raises(TypeError):
        filter_by_substring(strings=["valid", 123], substring="abc")

def test_spec_2_substring_type_error():
    """
    Spec 2: A TypeError must be raised if 'substring' is not a string.
    """
    with pytest.raises(TypeError):
        filter_by_substring(strings=["a", "b"], substring=None)

def test_spec_3_result_in_input():
    """
    Spec 3: The result list must contain only elements from the input list.
    (Safety / Subset Property)
    """
    strings = ["apple", "banana", "apricot", "grape"]
    substring = "ap"
    res = filter_by_substring(strings, substring)
    
    # Assert logical property
    assert all(s in strings for s in res)

def test_spec_4_result_contains_substring():
    """
    Spec 4: Each element in the result must contain the substring.
    (Filtering Property)
    """
    strings = ["apple", "banana", "apricot", "grape"]
    substring = "ap"
    res = filter_by_substring(strings, substring)
    
    # Assert logical property
    assert all(substring in s for s in res)

def test_spec_5_completeness():
    """
    Spec 5: Explicitly checking counts for completeness (handling duplicates).
    (Correctness / Multiplicity Property)
    """
    strings = ["apple", "banana", "apricot", "grape", "apple"] # 'apple' appears twice
    substring = "ap"
    res = filter_by_substring(strings, substring)
    
    # Calculate expected counts based on specification
    expected_counts = Counter(s for s in strings if substring in s)
    
    # Assert logical property
    assert Counter(res) == expected_counts



