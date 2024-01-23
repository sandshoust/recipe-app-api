"""
Sample tests 
"""

from django.test import SimpleTestCase

from app import calc

class CalcuTests(SimpleTestCase):
    """Test the calc module """

    def test_add_numberss(self):
        """Test adding numbers together"""

        res = calc.add(5,6)

        self.assertEqual(res, 11)

    def test_subtact_numbers(self):
        """ Test subtracting numbers """

        res = calc.subtract(15, 10) 

        self.assertEqual(res, 5)


