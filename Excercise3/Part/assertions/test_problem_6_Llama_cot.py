#Generated Assertions:
# 1. The number of results must equal the number of parenthesis groups 
#    (groups are substrings separated by spaces).
assert len(res) == paren_string.count(" ") + 1

# 2. Each result value must be >= 0, since nesting depth cannot be negative.
assert all(depth >= 0 for depth in res)

# 3. For each group, the recorded depth must be at least as large as the 
#    maximum number of '(' minus ')' imbalance seen at any prefix within that group.
assert all(
    depth >= max(
        sum(1 if ch == '(' else -1 for ch in group[:i])
        for i in range(len(group) + 1)
    )
    for depth, group in zip(res, paren_string.split())
)

# 4. No group may ever show negative imbalance at any prefix (i.e., 
#    parentheses should not close before they open).
assert all(
    all(
        sum(1 if ch == '(' else -1 for ch in group[:i]) >= 0
        for i in range(len(group) + 1)
    )
    for group in paren_string.split()
)

# 5. Each group's final balance must return to zero 
#    (every '(' must have a matching ')').
assert all(
    sum(1 if ch == '(' else -1 for ch in group) == 0
    for group in paren_string.split()
)





# Revised Assertions:
# 1. The number of results must equal the number of parenthesis groups 
#    (groups are substrings separated by spaces).
assert len(res) == len(paren_string.split())

# 2. Each result value must be >= 0, since nesting depth cannot be negative.
assert all(depth >= 0 for depth in res)

# 3. For each group, the recorded depth must be at least as large as the 
#    maximum number of '(' minus ')' imbalance seen at any prefix within that group.
assert all(
    depth >= max(
        sum(1 if ch == '(' else -1 for ch in group[:i])
        for i in range(len(group) + 1)
    )
    for depth, group in zip(res, paren_string.split())
)

# 4. No group may ever show negative imbalance at any prefix (i.e., 
#    parentheses should not close before they open).
assert all(
    depth == max(
        sum(1 if ch == '(' else -1 for ch in group[:i])
        for i in range(len(group) + 1)
    )
    for depth, group in zip(res, paren_string.split())
)

# 5. Each group's final balance must return to zero 
#    (every '(' must have a matching ')').
assert all(depth <= len(group) for depth, group in zip(res, paren_string.split()))
