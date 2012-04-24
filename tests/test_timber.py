from timber.timber import Timber
from twisted.trial import unittest

"""
Test cases
"""
class TimberTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def _test(self, operation, a, b, expected):
        pass
        #result = operation(a, b)
        #self.assertEqual(result, expected)


    def _test_error(self, operation):
        pass
	"""        self.assertRaises(TypeError, operation, "foo", 2)
        self.assertRaises(TypeError, operation, "bar", "egg")
        self.assertRaises(TypeError, operation, [3], [8, 2])
        self.assertRaises(TypeError, operation, {"e": 3}, {"r": "t"})"""

    def test_add(self):
        pass
        #self.assertEqual(result, 11)

    def test_subtract(self):
        pass

    def test_multiply(self):
        pass

    def test_divide(self):
        pass
