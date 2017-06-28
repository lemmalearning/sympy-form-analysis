from singleton_form import *
from monomial_form import *
from polynomial_form import *

import unittest
'''
    NOTE: Sympy doesn't honor expression flag evaluate=False
        for the identity property. This may be a crippling problem, that needs
        to be handled by whatever implements this library
'''
class TestSymp(unittest.TestCase):
    def setUp(self):
        self.x = Symbol('x')
        self.y = Symbol('y')
        self.a1 = Pow(self.x, 2, evaluate=False)
        self.a2 = Add(self.x, self.y, evaluate=False)
        self.a3 = Mul(self.x,self.y,2,3, evaluate = False)
        self.a4 = Mul(Pow(self.x,3),self.y,4,evaluate = False)
        self.a5 = Pow(3, 5, evaluate = False)
        self.a6 = Pow(3, pi, evaluate = False)
        self.a7 = Mul(Pow(self.x,4),Pow(self.x,9),evaluate=False)
        self.a8 = Mul(Pow(self.y,3),Pow(self.x,2),evaluate=False)
        self.a9 = Mul(Pow(self.y,pi),Pow(self.x,10),evaluate=False)
        self.a10 = Add(3,pi,pi,evaluate=False)
        self.a11 = Add(1,9,pi,evaluate=False)
        #self.a12 = Add(0,1,evaluate=False)
        self.a13 = Add(152, pi, evaluate=False)
    
    
    
    def test_singleton(self):
        self.assertTrue(is_singleton_form(self.x)[0])
        self.assertTrue(is_singleton_form(self.y)[0])
        self.assertFalse(is_singleton_form(self.a1)[0])
        self.assertFalse(is_singleton_form(self.a2)[0])
        self.assertFalse(is_singleton_form(self.a3)[0])
        self.assertFalse(is_singleton_form(self.a10)[0])
        self.assertFalse(is_singleton_form(self.a11)[0])
        #self.assertFalse(is_singleton_form(self.a12)[0])
        self.assertTrue(is_singleton_form(self.a13)[0])
    
    
    
    def test_monomial(self):
        self.assertTrue(is_monomial_form(self.x)[0])
        self.assertTrue(is_monomial_form(self.y)[0])
        self.assertTrue(is_monomial_form(self.a1)[0])
        self.assertFalse(is_monomial_form(self.a2)[0])
        self.assertFalse(is_monomial_form(self.a3)[0])
        self.assertTrue(is_monomial_form(self.a4)[0])
        self.assertFalse(is_monomial_form(self.a5)[0])
        self.assertTrue(is_monomial_form(self.a6)[0])
        self.assertFalse(is_monomial_form(self.a7)[0])
        self.assertTrue(is_monomial_form(self.a8)[0])
        self.assertTrue(is_monomial_form(self.a9)[0])
    
    
    
    def test_polynomial(self):
        self.assertFalse(is_polynomial_form(self.a10)[0])
        self.assertFalse(is_polynomial_form(self.a11)[0])
        #self.assertFalse(is_polynomial(self.a12)[0])
        self.assertTrue(is_polynomial_form(self.a13)[0])
if __name__ == '__main__':
    unittest.main()