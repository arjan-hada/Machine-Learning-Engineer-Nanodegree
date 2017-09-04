#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 10:25:36 2017

@author: arjanhada
"""

from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30

class MyDecimal(Decimal):
    """Check whether a decimal object is in given tolerance to zero"""
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        """Initialize a new linear system object by providing a list of plane objects"""
        try:
            d = planes[0].dimension
            for p in planes:
                # Make sure all our planes live in teh same dimension
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        """Swapping two equations"""
        temp = self[row1]
        self[row1] = self[row2]
        self[row2] = temp


    def multiply_coefficient_and_row(self, coefficient, row):
        """Multiplying an equation by a non-zero number"""
        n = self[row].normal_vector
        k = self[row].constant_term
        new_normal_vector = n.times_scalar(coefficient)
        new_constant_term = k * coefficient
        self[row] = Plane(normal_vector = new_normal_vector,
                          constant_term = new_constant_term)


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        """Adding a multiple of one equation to another"""
        n1 = self[row_to_add].normal_vector
        n2 = self[row_to_be_added_to].normal_vector
        k1 = self[row_to_add].constant_term
        k2 = self[row_to_be_added_to].constant_term
        
        new_normal_vector = n1.times_scalar(coefficient).plus(n2)
        new_constant_term = (k1 * coefficient) + k2
        self[row_to_be_added_to] = Plane(normal_vector = new_normal_vector,
                          constant_term = new_constant_term)
        
    def compute_triangular_form(self):
        """Return a new system in triangular form that has the same solution 
        set as the original system"""
        system = deepcopy(self) # To not modify the original system directly
        
        num_equations = len(system)
        num_variables = system.dimension
        j = 0
        
        for i in range(0, num_equations):
            while j < num_variables:
                c = MyDecimal(system[i].normal_vector[j])
                if c.is_near_zero():
                    swap_succeeded = system.swap_with_row_below_for_nonzero_coefficient(i, j)
                    
                    if not swap_succeeded:
                        j += 1
                        continue # continue to the next iteration of the while loop
                
                system.clear_coefficients_below(i,j)
                j += 1
                break # Break out of the while loop
        return system
    
    def swap_with_row_below_for_nonzero_coefficient(self, row, col):
        """If there is a row under row i with nonzero coefficient for var j
        swap that row with row i"""
        num_equations = len(self)
        
        for k in range(row+1, num_equations):
            coefficient = MyDecimal(self[k].normal_vector[col])
            if not coefficient.is_near_zero():
                self.swap_rows(row, k)
                return True
            
        return False
    
    def clear_coefficients_below(self, row, col):
        """Clear all the terms with var j below row i"""
        num_equations = len(self)
        beta = MyDecimal(self[row].normal_vector[col])
        
        for k in range(row+1, num_equations):
            gamma = MyDecimal(self[k].normal_vector[col])
            alpha = -gamma/beta
            self.add_multiple_times_row_to_row(alpha, row, k)
            

    def indices_of_first_nonzero_terms_in_each_row(self):
        """Find pivot variable in each equation"""
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        """Utility function that returns the number of planes in the system"""
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        """Utility function that prints the pretty version of the system of equations"""
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2):
    print('test case 1 failed')
    
p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == Plane(constant_term='1')):
    print('test case 2 failed')
    
p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','-1','1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','2','-5']), constant_term='3')
s = LinearSystem([p1,p2,p3])
t = s.compute_triangular_form()
if not (t[0] == Plane(normal_vector=Vector(['1','-1','1']), constant_term='2') and
        t[1] == Plane(normal_vector=Vector(['0','1','1']), constant_term='1') and
        t[2] == Plane(normal_vector=Vector(['0','0','-9']), constant_term='-2')):
    print('test case 4 failed')


