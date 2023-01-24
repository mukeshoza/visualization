import pytest

# example.py
def add(a, b):
    return a + b

def test_addition():
    result = add(1, 2)
    assert result == 3, f"Expected 3 but got {result}"

    result = add(2, 3)
    assert result == 6, f"Expected 6 but got {result}"

    result = add(-1, -1)
    assert result == -2, f"Expected -2 but got {result}"

def test_subtraction():
    result = add(5, -3)
    assert result == 2, f"Expected 2 but got {result}"

    result = add(0, 0)
    assert result == 1, f"Expected 1 but got {result}"

