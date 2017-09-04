import math
from decimal import Decimal, getcontext

# Ensure that numbers coming from outside the vector objects are treated as decimals
getcontext().prec = 30 

class Vector(object):
    
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(i) for i in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
    def __getitem__(self, i):
        return self.coordinates[i]

    def __iter__(self):
        return self.coordinates.__iter__()

    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def times_scalar(self, s):
        new_coordinates = [Decimal(s)*i for i in self.coordinates]
        return Vector(new_coordinates)
    
    def magnitude(self):
        coordinates_squared = [i**2 for i in self.coordinates]
        return Decimal(math.sqrt(sum(coordinates_squared)))
    
    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/magnitude)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            
    def dot_product(self, v):
        product = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(product)
    
    def angle_with(self, v, in_degrees = False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = math.acos(round(u1.dot_product(u2), 3))
            
            if in_degrees:
                return math.degrees(angle_in_radians)
            else:
                return angle_in_radians
            
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
                
            else:
                raise e
                
    def is_zero(self, tolerance = 1e-10):
        return self.magnitude() < tolerance
    
    def is_orthogonal_to(self, v, tolerance = 1e-10):
        return abs(self.dot_product(v)) < tolerance
    
    def is_parallel_to(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or
                self.angle_with(v) == math.pi)
        
    def projection_on(self, basis):
        u = basis.normalized()
        weight = self.dot_product(u)
        return u.times_scalar(weight)
        
    def component_orthogonal_to(self, basis):
        projection = self.projection_on(basis)
        return self.minus(projection)
    
    def cross_product_with(self, v):
        if self.dimension == 3 & v.dimension == 3:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = v.coordinates
            new_coordinates = [y1*z2 - y2*z1,
                              -(x1*z2 - x2*z1),
                               x1*y2 - x2*y1]
            return Vector(new_coordinates)
                
        elif self.dimension == 2 & v.dimension == 2:
            x1, y1 = self.coordinates
            x2, y2 = v.coordinates
            new_coordinates = [0,
                               0,
                               x1*y2 - x2*y1]
            return Vector(new_coordinates)
        
        else:
            raise ValueError('Only defined in two or three dimensions')
            
    def area_of_parallelogram_with(self, v):
        cross_product = self.cross_product_with(v)
        return cross_product.magnitude()
    
    def area_of_triangle_with(self, v):
        return Decimal(0.5)*self.area_of_parallelogram_with(v)
            













