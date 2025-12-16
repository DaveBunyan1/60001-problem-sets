# Problem Set 4A
# Name: Dave Bunyan
# Collaborators:
# Time Spent: x:xx

from typing import List


def get_permutations(sequence: str) -> List[str]:
    """
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    """
    # Base case
    if len(sequence) == 1:
        return [sequence]

    permutations: List[str] = []

    # Else, perms = get perms(sequence[1:])
    for i in range(len(sequence)):
        pass
        # Get all perms for sequence minus ith letter
        letter: str = sequence[i]
        perms = get_permutations(sequence[:i] + sequence[i + 1 :])
        # Insert letter into all perms
        for perm in perms:
            for j in range(len(perm) + 1):
                new_perm = perm[:j] + letter + perm[j:]
                if new_perm not in permutations:
                    permutations.append(new_perm)

    return permutations


# my_sliced_str = "abcde"
# for i in range(len(my_sliced_str)):
#     my_printed_sliced_str = my_sliced_str[:i] + my_sliced_str[i + 1 :]
#     print("My sliced letter:", my_sliced_str[i])
#     print("My slice test:", my_printed_sliced_str)

# my_str = "bcd"
# for i in range(len(my_str) + 1):
#     my_printed_str = my_str[:i] + "a" + my_str[i:]
#     print("My str test:", my_printed_str)


if __name__ == "__main__":
    #    #EXAMPLE
    #    example_input = 'abc'
    #    print('Input:', example_input)
    #    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    #    print('Actual Output:', get_permutations(example_input))

    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)
    example_input = "abc"
    print("Input:", example_input)
    print("Expected Output:", ["abc", "acb", "bac", "bca", "cab", "cba"])
    print("Actual Output:", get_permutations(example_input))

    example_input = "xyz"
    print("Input:", example_input)
    print("Expected Output:", ["xyz", "yxz", "yzx", "zxy", "xzy", "zyx"])
    print("Actual Output:", get_permutations(example_input))

    example_input = "aab"
    print("Input:", example_input)
    print("Expected Output:", ["aab", "aba", "baa"])
    print("Actual Output:", get_permutations(example_input))
