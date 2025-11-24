#Generated Assertions:
# 1. A TypeError must be raised if 'strings' is not a list of strings.
assert isinstance(strings, list) and all(isinstance(s, str) for s in strings)

# 2. A TypeError must be raised if 'substring' is not a string.
assert isinstance(substring, str)

# 3. The result list must contain only elements from the input list.
assert all(s in strings for s in res)

# 4. Each element in the result must contain the substring.
assert all(substring in s for s in res)

# 5. Any element in the input list that contains the substring must appear in the result.
assert all(
    (substring not in s) or (s in res)
    for s in strings
)




#Revised Assertions:
# 1. A TypeError must be raised if 'strings' is not a list of strings.
assert isinstance(strings, list) and all(isinstance(s, str) for s in strings)
# 2. A TypeError must be raised if 'substring' is not a string.
assert isinstance(substring, str)
# 3. The result list must contain only elements from the input list.
assert all(s in strings for s in res)
# 4. Each element in the result must contain the substring.
assert all(substring in s for s in res)
# 5.
# Explicitly checking counts for completeness (handling duplicates)
from collections import Counter
expected_counts = Counter(s for s in strings if substring in s)
assert Counter(res) == expected_counts
