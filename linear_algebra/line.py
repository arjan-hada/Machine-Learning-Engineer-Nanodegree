#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 12:23:53 2017

@author: arjanhada
"""

from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

class Line(object):
    """Line ckass in the form of Ax + By = c"""

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        """Initialise a new Line with a normal Vector and a Constant Term"""
        
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        """Finds the basepoint where the line intersects x or y"""
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            """Print the line in the form of a equation Ax + By = c"""
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    @staticmethod
    def first_nonzero_index(iterable):
        """Return the index of first non-zero value"""
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)
        
    def is_parallel_with(self, line2):
        """Find if a given line is parallel with our line"""
        n1 = self.normal_vector
        n2 = line2.normal_vector
        return n1.is_parallel_to(n2)
    
    def __eq__(self, line2):
        """Check if two lines being compared are equal"""
        
        # Check if the normal vector of the line is zero
        if self.normal_vector.is_zero():
            if not line2.normal_vector.is_zero():
                return False
            else:
                diff = self.constant_term - line2.constant_term
                # Check if the constant terms of the two lines are the same
                return MyDecimal(diff).is_near_zero() 
        
        # Check if the lines being compared are parallel,
        # if not parallel they cannot be equal.
        if not self.is_parallel_with(line2):
            return False
        basepoint1 = self.basepoint
        basepoint2 = line2.basepoint
        basepoint_diff = basepoint1.minus(basepoint2)
        
        n = self.normal_vector
        
        return basepoint_diff.is_orthogonal_to(n)
    
    def intersection_with(self, line2):
        try:
            A, B = self.normal_vector.coordinates
            C, D = line2.normal_vector.coordinates
            k1 = self.constant_term
            k2 = line2.constant_term
            
            x_num = D*k1 - B*k2
            y_num = A*k2 - C*k1
            one_over_denom = Decimal('1')/(A*D - B*C)
            return Vector([x_num, y_num]).times_scalar(one_over_denom)
        
        except ZeroDivisionError:
            if self == line2:
                return self
            else:
                None

# Test case   
line1 = Line(Vector(['4.046', '2.836']), '1.21')
line2 = Line(Vector(['10.115', '7.09']), '3.025')
print('intersection of line1 with line2 is', line1.intersection_with(line2))

line1 = Line(Vector(['7.204', '3.182']), '8.68')
line2 = Line(Vector(['8.172', '4.114']), '9.883')
print('intersection of line1 with line2 is', line1.intersection_with(line2))

line1 = Line(Vector(['1.182', '5.562']), '6.744')
line2 = Line(Vector(['1.773', '8.343']), '9.525')
print('intersection of line1 with line2 is', line1.intersection_with(line2))

#print('intersection 1:', line1.intersection_with(line2))