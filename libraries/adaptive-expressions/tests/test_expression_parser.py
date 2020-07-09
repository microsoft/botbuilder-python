import unittest
from adaptive.expressions import Expression

class ExpressionParserTests(unittest.TestCase):
    def test_add_valid(self):
        parsed = Expression.parse('1+1')
        self.assertTrue(parsed is not None)
        value, error = parsed.try_evaluate()
        self.assertEqual(value, 2)
        self.assertTrue(error is None)

        parsed = Expression.parse('add(2, 3)')
        self.assertTrue(parsed is not None)
        value, error = parsed.try_evaluate()
        self.assertEqual(value, 5)
        self.assertTrue(error is None)

if __name__ == '__main__':
    unittest.main()
