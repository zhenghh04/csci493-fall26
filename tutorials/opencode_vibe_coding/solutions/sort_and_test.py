"""Reference solution — sort integers ascending, with tests.

The lab's point is to have opencode WRITE this from a prompt; this is the
answer key / projector fallback.

    pytest solutions/sort_and_test.py     # run the tests (needs: pip install pytest)
    python solutions/sort_and_test.py     # quick self-check without pytest
"""


def sort_ints(nums):
    """Return a NEW list with the integers sorted in ascending order."""
    return sorted(nums)


# ---- tests (pytest discovers any function named test_*) -------------------
def test_empty():
    assert sort_ints([]) == []


def test_single():
    assert sort_ints([42]) == [42]


def test_already_sorted():
    assert sort_ints([1, 2, 3]) == [1, 2, 3]


def test_reverse_sorted():
    assert sort_ints([3, 2, 1]) == [1, 2, 3]


def test_duplicates():
    assert sort_ints([2, 3, 2, 1, 3]) == [1, 2, 2, 3, 3]


def test_negatives():
    assert sort_ints([0, -5, 3, -1]) == [-5, -1, 0, 3]


def test_does_not_mutate_input():
    original = [3, 1, 2]
    sort_ints(original)
    assert original == [3, 1, 2]


# ---- quick self-check when run directly -----------------------------------
if __name__ == "__main__":
    cases = [
        ([], []),
        ([42], [42]),
        ([3, 1, 2], [1, 2, 3]),
        ([2, 3, 2, 1], [1, 2, 2, 3]),
        ([0, -5, 3, -1], [-5, -1, 0, 3]),
        ([10, 2, 33, 4], [2, 4, 10, 33]),
    ]
    all_ok = True
    for inp, want in cases:
        got = sort_ints(list(inp))
        ok = got == want
        all_ok &= ok
        print(f"[{'ok' if ok else 'FAIL'}] sort_ints({inp}) -> {got}")
    print("all passed" if all_ok else "SOME FAILED")
