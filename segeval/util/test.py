'''
Test utilities, and tests for said utilities.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal

class TestCase(unittest.TestCase):
    '''
    Test WindowDiff.
    '''
    # pylint: disable=R0904,C0324
    DECIMAL_PLACES = 4

    def assertAlmostEquals(self, first, second, places=DECIMAL_PLACES,
                           msg=None, delta=None):
        '''
        Automatically converts values to floats.
        '''
        # pylint: disable=C0103,R0913
        if isinstance(first, dict) and isinstance(second, dict):
            for item in set(first.keys() + second.keys()):
                if not msg:
                    msg = '{0} != {1}'.format(first, second)
                if item not in first:
                    raise Exception(
                            '{0} not in {1}; expected {2}'.format(item, first,
                                                                  second))
                if item not in second:
                    raise Exception(
                            '{0} not in {1}; expected {2}'.format(item, second,
                                                                  first))
                self.assertAlmostEquals(first[item], second[item], places, msg,
                                        delta)
        elif (isinstance(first, list) or isinstance(first, tuple)) and \
            (isinstance(second, list) or isinstance(second, tuple)):
            if len(first) != len(second):
                raise Exception(
                        'Size mismatch; {0} != {1}'.format(first, second))
            for item in zip(first, second):
                if not msg:
                    msg = '{0} != {1}'.format(first, second)
                self.assertAlmostEquals(item[0], item[1], places, msg, delta)
        elif type(first) != type(second):
            if type(first) != float and type(first) != Decimal and \
            type(second) != float and type(second) != Decimal:
                raise Exception('Type mismatch; {0} != {1}'.format(
                                    type(first), type(second)))
        else:
            return unittest.TestCase.assertAlmostEquals(self,
                                                        float(first),
                                                        float(second),
                                                        places=places,
                                                        msg=msg,
                                                        delta=delta)


class TestTestCase(TestCase):
    '''
    Test utility tests.
    '''
    # pylint: disable=R0904
    
    def test_almost_equal_values(self):
        '''
        Test a type mistmatch.
        '''
        self.assertRaises(AssertionError, self.assertAlmostEquals,
                          {'a' : 1},
                          {'a' : 2})
    
    def test_mismatch(self):
        '''
        Test a type mistmatch.
        '''
        self.assertRaises(Exception, self.assertAlmostEquals, (), {})
    
    def test_equal_types(self):
        '''
        Test a type mistmatch.
        '''
        self.assertAlmostEquals({}, {})
        self.assertAlmostEquals([], [])
        self.assertAlmostEquals((), ())
        self.assertAlmostEquals((), [])
        self.assertAlmostEquals([], ())
        self.assertAlmostEquals(0.0, 0.0)
        self.assertAlmostEquals(0, 0)
        self.assertAlmostEquals(Decimal('0'), Decimal('0'))
        self.assertAlmostEquals(0.0, 0)
        self.assertAlmostEquals(0, 0.0)
        self.assertAlmostEquals(0, Decimal('0'))
        self.assertAlmostEquals(Decimal('0'), 0)
        self.assertAlmostEquals(0.0, Decimal('0'))
        self.assertAlmostEquals(Decimal('0'), 0.0)
    
    def test_tuple_first(self):
        self.assertRaises(Exception, self.assertAlmostEquals, (), (1))
    
    def test_tuple_second(self):
        self.assertRaises(Exception, self.assertAlmostEquals, (1), ())
    
    def test_list_first(self):
        self.assertRaises(Exception, self.assertAlmostEquals, [], [1])
    
    def test_list_second(self):
        self.assertRaises(Exception, self.assertAlmostEquals, [1], [])
    
    def test_dict_first(self):
        self.assertRaises(Exception, self.assertAlmostEquals, {}, {'a' : 1})
    
    def test_dict_second(self):
        self.assertRaises(Exception, self.assertAlmostEquals, {'a' : 1}, {})
    
        
        
        
        
        