from mathParser import MathParser
import unittest

def test(self, test, result):
  self.assertEqual(self.mathParser.eval(test),result)

class TestMessageParsing(unittest.TestCase):

  def setUp(self):
    # create parser instance
    self.mathParser = MathParser()
    self.mathParser.errorHandling=True

  def test_parentheses(self):
    # order of operations
    test(self, '1*(1+2)*3', '9')

  def test_exponents(self):
    test(self, '2^3', '8')
    test(self, '3^(2^3)', '6561')

  def test_multiplication(self):
    test(self, '3*4', '12')
    # Test negative numbers
    test(self, '-3*-4*-2', '-24')

  def test_division(self):
    # Test division direction
    test(self, '16/4/2','2') 
    # Test float responses
    test(self, '1/2', '0.5')
    # Test addition of fractions
    test(self, '3/4+1/8', '0.875')

  def test_addition(self):
    test(self, '2+2+4', '8')
    # Test adding a negative number
    test(self, '2+-3', '-1')

  def test_subtraction(self):
    # Test direction of subtraction
    test(self, '16-4-6', '6')
    # Test negative numbers
    test(self, '16-26', '-10')

  def test_variables(self):
    test(self, 'x=2', 'x is set to 2')
    test(self, 'x+3','5')
    # Test simple recall
    test(self, 'x', '2')

  def test_errors(self):
    # Attempt to raise errors
    test(self, 'hi', "Unknown Variable: 'hi'")
    test(self, '3)', 'Syntax Error: Unmatched Parentheses')
    test(self, '(1+3', 'Syntax Error: Unmatched Parentheses')
    test(self, '123456789^123456789', 'Overflow: Number too large')
    test(self, '^3', 'Syntax Error: At ^')
    test(self, '3^^3', 'Syntax Error: At ^')
    test(self, '5/0', 'Cannot divide by zero')

  def test_order_of_operations(self):
    # Some 'tricky' expressions to test order of operations
    test(self, '3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3', '3.000122')
    test(self, '2+3*3+2', '13')
    
if __name__ == '__main__':
  unittest.main()
  