from __future__ import division
import sympy
from sympy import Add,Mul,rcollect,Number,NumberSymbol,sin,cos,Pow,Integer,Symbol,fraction,gcd,div
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction

from .form_output import *
from .form_utils import *

def is_singleton_form(expr):
    '''determines if the expression is a singleton.
        Note: internally, 0 + 6 will pass as a singleton, because SymPy will
            convert 0 + 6 to 6. This is Sympy's fault; if the issue is handled
            it won't be here.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    if isinstance(expr, (Number, NumberSymbol, Symbol)):
        return True, SingletonOutput.strout("VALID")

    if isinstance(expr, Add):
        result = singleton_combinable_terms(expr)
        return not result[0], result[1]

    if isinstance(expr, (Mul,Pow)):
        if is_numerically_reducible_monomial(expr)[0]:
            return False, UtilOutput.strout("REDUCIBLE")
        return is_singleton_factor_form(expr)

    if isinstance(expr, (TrigonometricFunction, InverseTrigonometricFunction)):
        return True, SingletonOutput.strout("VALID_TRIG")

    return False, SingletonOutput.strout("INVALID")

def is_singleton_factor_form(expr):
    '''Determines if a product in a singleton is appropriate.
        1. No symbols are allowed in the product.
        2. Product cannot contain two rational numbers.
        3. Product cannot contain any operations other than Mul.
        Args:
            expr: A Mul Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    if len(expr.free_symbols) > 0 and not isinstance(expr, Symbol):
        return False, SingletonOutput.strout("IMPROPER_TERM")

    if isinstance(expr,Pow) and isinstance(expr.args[0], Number):
        result = const_to_const(expr)
        return not result[0], result[1]

    for i in expr.args:
        #Make sure that anything inside is either a number,
        #numbersymbol, multiplication, or addition.
        if not isinstance(i, (Number, NumberSymbol,Pow,Mul)):
            return False, SingletonOutput.strout("IMPROPER_TERM")
        if isinstance(i,Pow):
            result = const_to_const(i)
            if result[0]:
                return False, result[1] 
        if isinstance(i,Mul):
            if is_numerically_reducible_monomial(i)[0]:
                return False, SingletonOutput.strout("IMPROPER_TERM")
    

    if sum(isinstance(j, Number) for j in expr.args) > 1:
        return False, SingletonOutput.strout("INVALID_PRODUCT")

    return True, SingletonOutput.strout("VALID_PRODUCT")

def singleton_combinable_terms(expr):
    '''determines if two terms in a singleton can be combined.
        1. Two rational numbers are combinable.
        2. Two identical rational numbers are combinable.
        3. Two irrational numbers with combinable terms (pi, sqrt(2),etc)
            are combinable
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    #Collect the bases for later comparison
    bases = []

    #We don't want symbols or subexpressions like Add
    for i in expr.args:
        if not isinstance(i, (Number, NumberSymbol, Mul)):
            return True, SingletonOutput.strout("INVALID_SUM")
        if isinstance(i, Mul):
            bases += i.args
            result = is_singleton_factor_form(i)
            if not result[0]:
                return True, result[1]
        else:
            bases.append(i)

    #Any two rational numbers can be simplified
    if sum(isinstance(i, Number) for i in expr.args) > 1:
        return True, SingletonOutput.strout("INVALID_SUM")

    if len(bases) != len(set(bases)):
        return True, SingletonOutput.strout("INVALID_SUM")
    
    return False, SingletonOutput.strout("VALID_SUM")

