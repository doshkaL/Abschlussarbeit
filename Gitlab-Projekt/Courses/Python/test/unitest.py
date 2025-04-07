from scr.fibonacci import fibonacci  # Pfad anpassen, falls nötig
import pytest

def test_fibonacci_0():
    """Punkt: 10"""
    assert fibonacci(0) == 0

def test_fibonacci_1():
    """Punkt: 10"""
    assert fibonacci(1) == 1

def test_fibonacci_10():
    """Punkt: 10"""
    assert fibonacci(10) == 55


if __name__ == "__main__":
    unittest.main()
