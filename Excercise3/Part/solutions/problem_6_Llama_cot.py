from typing import List

def parse_nested_parens(paren_string: str) -> List[int]:
    """
    Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    
    Args:
        paren_string (str): Input string containing multiple balanced parenthesis groups separated by spaces.
    
    Returns:
        List[int]: A list of maximum nesting depths for each group of parentheses.
    """
    # Split the input string into individual groups by spaces
    groups = paren_string.split()
    
    # Initialize an empty list to store the maximum nesting depths for each group
    max_depths = []
    
    # Iterate over each group
    for group in groups:
        # Initialize the current nesting depth to 0
        current_depth = 0
        
        # Initialize the maximum depth seen so far to 0
        max_depth = 0
        
        # Iterate over each character in the group
        for char in group:
            # If the character is an opening parenthesis, increment the current depth
            if char == '(':
                current_depth += 1
                # Update the maximum depth if the current depth is greater
                max_depth = max(max_depth, current_depth)
            # If the character is a closing parenthesis, decrement the current depth
            elif char == ')':
                current_depth -= 1
        
        # Ensure the maximum depth is not negative (in case of unbalanced parentheses)
        max_depth = max(0, max_depth)
        
        # Append the maximum depth for the current group to the result list
        max_depths.append(max_depth)
    
    # Return the list of maximum nesting depths for each group
    return max_depths
