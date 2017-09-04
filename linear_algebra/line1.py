#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:11:58 2017

@author: arjanhada
"""

from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30

class NoNonZeroElements(Exception):
    """Custom Error for No Non Zero Elements in a Plane"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class InaccurateDecimal(Decimal):
    """Utility wrapper class to detect values close to 0"""
    def is_near_zero(self, eps=1e-10):
        """Checks if value is virtually 0"""
        return abs(self) < eps

class Line(object):
    """Line class in the form Ax + By = C"""

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    """Initialise a new Line with a normal Vector and a Constant Term"""
    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()

    def is_parallel(self, line):
        """Determine if two Lines are parallel"""
        return self.normal_vector.is_parallel_to(line.normal_vector)


    def set_basepoint(self):
        """Calculates the basepoint where the line intersects x or y"""
        try:
            normal_vector = self.normal_vector
            constant = self.constant_term
            basepoint_coords = ['0'] * self.dimension

            initial_index = Line.first_nonzero_index(normal_vector)
            initial_coefficient = normal_vector[initial_index]

            basepoint_coords[initial_index] = constant / initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except NoNonZeroElements as error:
            if str(error) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise error

    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            """Print the coefficient as a readable string in Ax + By = C"""
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

        normal_vector = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(normal_vector)
            terms = ([
                (write_coefficient(
                    normal_vector[i],
                    is_initial_term=(i == initial_index)) + 'x_{}'.format(i+1))
                for i in range(self.dimension)
                if round(normal_vector[i], num_decimal_places) != 0
            ])
            output = ' '.join(terms)

        except NoNonZeroElements as error:
            if str(error) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise error

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    @staticmethod
    def first_nonzero_index(iterable):
        """Find the first non zero value"""
        for k, item in enumerate(iterable):
            if not InaccurateDecimal(item).is_near_zero():
                return k
        raise NoNonZeroElements(Line.NO_NONZERO_ELTS_FOUND_MSG)
        
line1 = Line(Vector(['4.046', '2.836']), '1.21')
line2 = Line(Vector(['10.115', '7.09']), '3.025')
print(line1.is_parallel_with(line2))