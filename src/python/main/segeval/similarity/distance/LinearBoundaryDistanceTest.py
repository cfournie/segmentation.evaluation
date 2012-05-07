'''
Created on Apr 2, 2012

@author: cfournie
'''
import unittest
from .SingleBoundaryDistance import linear_edit_distance


class TestLinearBoundaryDistance(unittest.TestCase):
    # pylint: disable=R0904,C0324,C0103
    
    SKIP = False

    def test_nested_transp_case_linear(self):
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [1,1,7]
        mass_b = [5,1,3]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     7)[0:3]
        self.assertEqual((d,t,s), (1,1,0))
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     5)[0:3]
        
        self.assertEqual((d,t,s), (3,1,2))


    def test_suboptimal_transp(self):
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [1,3,2]
        mass_b = [2,3,1]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     4)[0:3]
        self.assertEqual((d,t,s), (2,2,0))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     2)[0:3]
        self.assertEqual((d,t,s), (2,2,0))


    def test_n2_transp(self):
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [5,5]
        mass_b = [6,4]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     1)[0:3]
        self.assertEqual((d,t,s), (2,0,2))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     2)[0:3]
        self.assertEqual((d,t,s), (1,1,0))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     3)[0:3]
        self.assertEqual((d,t,s), (1,1,0))


    def test_n3_transp(self):
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [5,5]
        mass_b = [7,3]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     1)[0:3]
        self.assertEqual((d,t,s), (2,0,2))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     2)[0:3]
        self.assertEqual((d,t,s), (2,0,2))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     3)[0:3]
        self.assertEqual((d,t,s), (1,1,0))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     4)[0:3]
        self.assertEqual((d,t,s), (1,1,0))

    
    def test_complex_case(self):
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [1,2,2,4]
        mass_b = [2,2,5]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     4)[0:3]
        self.assertEqual((d,t,s), (3,2,1))
        
    def test_sim_1(self):
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [1,4,4]
        mass_b = [1,2,6]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     5)[0:3]
                                     
        self.assertEqual((d,t,s), (1,1,0))
        
        
        
        
        
        