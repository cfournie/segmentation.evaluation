

import unittest


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
        if isinstance(first, dict):
            for item in first.keys():
                try:
                    self.assertAlmostEquals(first[item], second[item], places,
                                            msg, delta)
                except:
                    print(first)
                    print(second)
                    raise
        elif isinstance(first, list) or isinstance(first, tuple):
            for item in zip(first, second):
                try:
                    self.assertAlmostEquals(item[0], item[1], places, msg,
                                            delta)
                except:
                    print(first)
                    print(second)
                    raise
        else:
            return unittest.TestCase.assertAlmostEquals(self,
                                                        float(first),
                                                        float(second),
                                                        places=places,
                                                        msg=msg,
                                                        delta=delta)
