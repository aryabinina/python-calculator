import unittest
import pycalc

two = 2


def get10():
    return 10


def sin(number):
    return two


class PycalcTest(unittest.TestCase):
    def test_evaluate_sum(self):
        result = pycalc.evaluate([], "1034 + 13.678")
        self.assertEqual(result, 1047.678)

    def test_evaluate_subtract(self):
        result = pycalc.evaluate([], "1034 - 13.678")
        self.assertEqual(result, 1020.322)

    def test_evaluate_multiplication(self):
        result = pycalc.evaluate([], "34*90.05")
        self.assertEqual(result, 3061.7)

    def test_evaluate_division(self):
        result = pycalc.evaluate([], "1034/12")
        self.assertEqual(result, 86.16666666666667)

    def test_evaluate_division_integer_part(self):
        result = pycalc.evaluate([], "1034//12")
        self.assertEqual(result, 86)

    def test_evaluate_division_mod(self):
        result = pycalc.evaluate([], "1034%12")
        self.assertEqual(result, 2)

    def test_evaluate_power(self):
        result = pycalc.evaluate([], "2^6")
        self.assertEqual(result, 64)

    def test_evaluate_less_true(self):
        result = pycalc.evaluate([], "2 < 5")
        self.assertEqual(result, True)

    def test_evaluate_less_false(self):
        result = pycalc.evaluate([], "12 < 5")
        self.assertEqual(result, False)

    def test_evaluate_less_or_eq_true(self):
        result = pycalc.evaluate([], "5 <= 5")
        self.assertEqual(result, True)

    def test_evaluate_less_or_eq_false(self):
        result = pycalc.evaluate([], "12 <= 5")
        self.assertEqual(result, False)

    def test_evaluate_eq_true(self):
        result = pycalc.evaluate([], "12 == 12")
        self.assertEqual(result, True)

    def test_evaluate_eq_false(self):
        result = pycalc.evaluate([], "12 == 5")
        self.assertEqual(result, False)

    def test_evaluate_not_eq_true(self):
        result = pycalc.evaluate([], "2 != 5")
        self.assertEqual(result, True)

    def test_evaluate_not_eq_false(self):
        result = pycalc.evaluate([], "12 != 12")
        self.assertEqual(result, False)

    def test_evaluate_greater_or_eq_true(self):
        result = pycalc.evaluate([], "12 >= 5")
        self.assertEqual(result, True)

    def test_evaluate_greater_or_eq_false(self):
        result = pycalc.evaluate([], "2 >= 5")
        self.assertEqual(result, False)

    def test_evaluate_greater_true(self):
        result = pycalc.evaluate([], "12 > 5")
        self.assertEqual(result, True)

    def test_evaluate_greater_false(self):
        result = pycalc.evaluate([], "2 > 5")
        self.assertEqual(result, False)

    def test_evaluate_abs(self):
        result = pycalc.evaluate([], "abs(100-156)")
        self.assertEqual(result, 56)

    def test_evaluate_round(self):
        result = pycalc.evaluate([], "round(4.67)")
        self.assertEqual(result, 5)

    def test_evaluate_math_const_and_function(self):
        result = pycalc.evaluate([], "e*sin(8)")
        self.assertEqual(result, 2.689354543632441)

    def test_evaluate_priority(self):
        result = pycalc.evaluate([], "2+2*2^2")
        self.assertEqual(result, 10)

    def test_evaluate_bracers(self):
        result = pycalc.evaluate([], "2*(3+7)")
        self.assertEqual(result, 20)

    def test_evaluate_custom_const_and_functions(self):
        result = pycalc.evaluate(["pycalc_test"], "two*get10()")
        self.assertEqual(result, 20)

    def test_evaluate_custom_const_and_functions_overwrite(self):
        result = pycalc.evaluate(["pycalc_test"], "sin(1) + sin(2)")
        self.assertEqual(result, 4)

    def test_evaluate_implicit_multiplication(self):
        self.assertEqual(14, pycalc.evaluate([], "2(5+2)"))
        self.assertEqual(21, pycalc.evaluate([], "(1 + 2)(3 + 4)"))
        self.assertEqual(5, pycalc.evaluate([], "log10(10)5"))

    def test_evaluate_complex_case(self):
        expression = "1*4+3.3/(3+0.3)*3(sqrt(4))/(sin(0)+1)"
        self.assertEqual(10.0, pycalc.evaluate([], expression))


if __name__ == '__main__':
    unittest.main()
