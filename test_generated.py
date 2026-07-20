from uploads.calculator import add, subtract, multiply, divide
import pytest

def test_add_positive_integers():
    assert add(2, 3) == 5

def test_add_negative_integers():
    assert add(-5, -7) == -12

def test_add_positive_and_negative_integers():
    assert add(10, -3) == 7
    assert add(-10, 3) == -7

def test_add_with_zero():
    assert add(0, 8) == 8
    assert add(-8, 0) == -8
    assert add(0, 0) == 0

def test_add_float_numbers():
    assert add(0.1, 0.2) == pytest.approx(0.3)
    assert add(1.5, -0.7) == pytest.approx(0.8)

def test_add_large_numbers():
    assert add(1000000000, 2000000000) == 3000000000
    assert add(-123456789, 987654321) == 864200000 + 12

def test_subtract_positive_integers():
    assert subtract(10, 4) == 6

def test_subtract_negative_integers():
    assert subtract(-5, -2) == -3
    assert subtract(-2, -5) == 3

def test_subtract_positive_and_negative_integers():
    assert subtract(5, -3) == 8
    assert subtract(-5, 3) == -8

def test_subtract_with_zero():
    assert subtract(7, 0) == 7
    assert subtract(0, 7) == -7
    assert subtract(0, 0) == 0

def test_subtract_float_numbers():
    assert subtract(0.5, 0.2) == pytest.approx(0.3)
    assert subtract(1.0, 0.1) == pytest.approx(0.9)

def test_subtract_result_is_negative():
    assert subtract(3, 8) == -5

def test_subtract_large_numbers():
    assert subtract(987654321, 123456789) == 864197532
    assert subtract(1, 1000000000) == -999999999

def test_multiply_positive_integers():
    assert multiply(4, 5) == 20

def test_multiply_negative_integers():
    assert multiply(-3, -6) == 18

def test_multiply_positive_and_negative_integers():
    assert multiply(7, -2) == -14
    assert multiply(-7, 2) == -14

def test_multiply_with_zero():
    assert multiply(0, 9) == 0
    assert multiply(9, 0) == 0
    assert multiply(0, 0) == 0

def test_multiply_with_one():
    assert multiply(1, 15) == 15
    assert multiply(-1, 15) == -15
    assert multiply(15, 1) == 15

def test_multiply_float_numbers():
    assert multiply(0.5, 2.0) == pytest.approx(1.0)
    assert multiply(0.1, 0.2) == pytest.approx(0.02)
    assert multiply(-2.5, 4.0) == pytest.approx(-10.0)

def test_multiply_large_numbers():
    assert multiply(100000, 1000) == 100000000
    assert multiply(12345, 0) == 0

def test_divide_positive_integers_exact_division():
    assert divide(10, 2) == 5.0

def test_divide_positive_integers_float_result():
    assert divide(7, 2) == 3.5

def test_divide_negative_integers():
    assert divide(-10, -2) == 5.0
    assert divide(-10, 2) == -5.0
    assert divide(10, -2) == -5.0

def test_divide_by_one():
    assert divide(15, 1) == 15.0
    assert divide(-15, 1) == -15.0

def test_divide_zero_by_number():
    assert divide(0, 5) == 0.0
    assert divide(0, -5) == 0.0

def test_divide_float_results_precision():
    assert divide(1, 3) == pytest.approx(0.3333333333333333)
    assert divide(20.0, 3.0) == pytest.approx(6.666666666666667)

def test_divide_large_numbers():
    assert divide(1000000, 2) == 500000.0
    assert divide(123456789, 3) == pytest.approx(41152263.0)

def test_divide_by_zero_edge_case():
    assert divide(10, 0) == "Division by zero is not allowed"
    assert divide(-10, 0) == "Division by zero is not allowed"
    assert divide(0, 0) == "Division by zero is not allowed"