import pytest

# example.py
def add(a, b):
    return a + b

def test_addition():
    result = add(1, 2)
    assert result == 3, f"Expected 3 but got {result}"

def test_subtraction():
    result = add(5, -3)
    assert result == 2, f"Expected 2 but got {result}"
