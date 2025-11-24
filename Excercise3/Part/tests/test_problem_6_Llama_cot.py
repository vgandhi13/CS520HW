"""
Test file for HumanEval_6 (parse_nested_parens) - Llama_cot variant
Part 2: LLM-generated tests to improve coverage

Add your LLM-generated unit tests below.
These tests should aim to improve code coverage beyond the baseline.
"""

from solutions.problem_6_Llama_cot import parse_nested_parens


# TODO: Add your LLM-generated test cases here
# Example structure:
# def test_parse_nested_parens_edge_case_1():
#     """Test description"""
#     result = parse_nested_parens("your test input")
#     assert result == expected_output

# --- Old Tests From Excercise 2---
def test_multiple_groups(): #Iteration 1
    """Test multiple groups of nested parentheses with varying depths."""
    result = parse_nested_parens("(()()) ((())) () ((())()())")
    assert result == [2, 3, 1, 3]

def test_parse_nested_parens_with_other_chars():
    """Test that characters other than parentheses are ignored and do not affect depth."""
    result = parse_nested_parens("() (a) (b(c))")
    assert result == [1, 1, 2]




# --- Individual Specification Tests for Excercise 3 ---

def test_spec_1_result_length():
    """
    Spec 1: The number of results must equal the number of parenthesis groups.
    """
    paren_string = "((())) (()) ()"
    res = parse_nested_parens(paren_string)
    
    # Assertion from instructions
    assert len(res) == len(paren_string.split())


def test_spec_2_non_negative():
    """
    Spec 2: Each result value must be >= 0.
    """
    paren_string = "((())) (())"
    res = parse_nested_parens(paren_string)
    
    # Assertion from instructions
    assert all(depth >= 0 for depth in res)


def test_spec_3_lower_bound_depth():
    """
    Spec 3: Recorded depth must be at least as large as the maximum prefix balance.
    """
    paren_string = "(((()))) ((()))"
    res = parse_nested_parens(paren_string)
    
    # Assertion from instructions
    assert all(
        depth >= max(
            sum(1 if ch == '(' else -1 for ch in group[:i])
            for i in range(len(group) + 1)
        )
        for depth, group in zip(res, paren_string.split())
    )


def test_spec_4_exact_depth_equality():
    """
    Spec 4: Recorded depth must explicitly equal the maximum prefix balance.
    (This asserts correctness of the calculation logic)
    """
    paren_string = "(()(())) ((()()))"
    res = parse_nested_parens(paren_string)
    
    # Assertion from instructions
    assert all(
        depth == max(
            sum(1 if ch == '(' else -1 for ch in group[:i])
            for i in range(len(group) + 1)
        )
        for depth, group in zip(res, paren_string.split())
    )


def test_spec_5_upper_bound_sanity():
    """
    Spec 5: Each group's depth cannot exceed the length of the group itself.
    (Physical boundary condition)
    """
    paren_string = "((())) (())"
    res = parse_nested_parens(paren_string)
    
    # Assertion from instructions
    assert all(depth <= len(group) for depth, group in zip(res, paren_string.split()))