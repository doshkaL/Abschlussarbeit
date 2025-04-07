import pytest
from scr.multiply import multiply

class TestMultiply:
    def test_positive_numbers(self):
        """Punkt: 10"""
        assert multiply(2, 3) == 6
        assert multiply(5, 10) == 50

    def test_negative_numbers(self):
        """Punkt: 10"""
        assert multiply(-2, 3) == -6
        assert multiply(-5, -10) == 50

    def test_zero(self):
        """Punkt: 10"""
        assert multiply(0, 5) == 0
        assert multiply(5, 0) == 0
