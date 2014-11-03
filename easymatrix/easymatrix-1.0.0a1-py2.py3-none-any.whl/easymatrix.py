#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       easymatrix.py
#       
#       Copyright 2014 Francisco Vicent <franciscovicent@outlook.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

class Matrix:
    
    def __init__(self, matrix=None, size=None):
        self.matrix = matrix
        
        if self.matrix is not None:
            self.rows = len(self.matrix)
            self.columns = len(self.matrix[0])
            self.size = self.rows, self.columns
        else:
            if size is not None:
                self.rows, self.columns = size
                self.size = size
                self.matrix = [[0 for j in range(self.columns)]
                               for i in range(self.rows)]
            else:
                raise ValueError("Expected matrix or size arguments.")
        
        self.rrows, self.rcolumns = range(self.rows), range(self.columns)
    
    def __add__(self, other):
        return self._arithmetic_operation(other, True)
    
    def __div__(self, other):
        if isinstance(other, Matrix):
            raise RuntimeError("Matrix division isn't supported yet.")
        elif isinstance(other, (int, float)):
            return self._geometric_operation(other, False)
        else:
            raise ValueError("Expected Matrix, int or float.")
    
    def __getitem__(self, row):
        return self.matrix[row]
    
    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.columns == other.rows:
                result = Matrix(size=(self.rows, other.columns))
                for i in self.rrows:
                    for k in other.rcolumns:
                        num = 0
                        for j in self.rcolumns:
                            num += self[i][j] * other[j][k]
                        result[i][k] = num
                return result
            else:
                raise ValueError("Expected ?x%d and %dx? matrices." %
                                 (self.columns, self.rows))
        elif isinstance(other, (int, float)):
            return self._geometric_operation(other, True)
        else:
            raise ValueError("Expected Matrix, int or float.")
    
    def __pow__(self, other):
        if other > 0:
            result = self
            for i in range(other - 1):
                result *= self
            return result
        else:
            raise ValueError("Expected exponent greater than 0.")
    
    def __str__(self):
        spacing = 0
        for i in self.rrows:
            for j in self.rcolumns:
                cur = len(str(self[i][j]))
                if cur > spacing:
                    spacing = cur
        spacing += 1
        result = ""
        for i in self.rrows:
            if result:
                result += "\n"
            for j in self.rcolumns:
                result += (("%-" + str(spacing) + "s") % str(self[i][j]))
        return result
    
    def __repr__(self):
        return self.__str__()
    
    def __sub__(self, other):
        return self._arithmetic_operation(other, False)
    
    def __truediv__(self, other):
        return self.__div__(other)
    
    def _arithmetic_operation(self, other, add):
        if isinstance(other, Matrix):
            if self.size == other.size:
                result = Matrix(size=(self.size))
                for i in self.rrows:
                    for j in self.rcolumns:
                        op_result = (
                            self[i][j] + other[i][j] if add else
                            self[i][j] - other[i][j]
                        )
                        result[i][j] = op_result
                return result
            else:
                raise ValueError(
                    "Can't %s matrices with different sizes." %
                    ("add" if add else "subtract"))
        else:
            raise TypeError("Expected a Matrix instance.")
    
    def _geometric_operation(self, other, mul):
        result = Matrix(size=(self.size))
        for i in self.rrows:
            for j in self.rcolumns:
                op_result = (
                    self[i][j] * other if mul else
                    self[i][j] / other
                )
                result[i][j] = op_result
        return result