import unittest
from source.MathUtils.MathUtils import *

test1 = Fractional(5, 2)
test2 = Decimal(3.5)
test3 = MoneyLine(120)
test4 = MoneyLine(-120)


class TestProgram(unittest.TestCase):

    def test_case_1(self):
        self.assertEqual(test1.get_odds().probability, 28.57142857142857)

    def test_case_2(self):
        self.assertEqual(test2.get_odds().probability, 28.57142857142857)

    def test_case_3(self):
        self.assertEqual(test1.get_odds().probability, test2.get_odds().probability)

    def test_case_4(self):
        self.assertEqual(test3.get_odds().probability, 45.45454545454545)

    def test_case_5(self):
        self.assertEqual(test4.get_odds().probability, 54.54545454545454)

    def test_case_6(self):
        self.assertEqual(test3.get_odds().probability + test4.get_odds().probability, 100.0)


if __name__ == "__main__":
    unittest.main()
