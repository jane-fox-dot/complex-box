# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 09:40:12 2019

@author: Acer
"""

from singleblock import SingleBlock
from numpy.linalg import det
from math import sqrt

class DuoBlock(object):
    """
    Класс для описания объекта, состоящего из двух параллелепипедов, соприкасающихся одной стороной.
    """
    def __init__(self, r=None):
        self.n = 2
        self.parts = []
        
        try:
            self.parts.append(SingleBlock(r[0]))
            #self.block1 = b1
            self.parts.append(SingleBlock(r[1]))
            #self.block2 = b2
        except:
            pass
        
        self.plane_r = None
        self.plane_dcm = None
    
    
    def set_plane(self, rr, dcm):
        self.plane_r = rr
        self.plane_dcm = dcm
        
    def check_intercept(self):
        u"""
            Функция проверки факта пересечения плоскостью параллелепипедов
            
        Returns
        ----------
        list - список составных частей, которые пересекает плоскость
        False - плоскость не пересекает ни одну часть объекта
        """
        
        if self.plane_r is None:
            return []
        if self.plane_dcm is None:
            return []
        
        # БС, что т.(x_0, y_0, z_0) задается вектором r,
        # т.(x_1, y_1, z_1) и т. (x_2, y_2, z_2) - первым и вторым столбцами
        # матрицы dcm соответственно
        result = []
        for i in range(len(self.parts)):
            print('Block #%1d' %i)
            place = []
            for j in range(len(self.parts[i].points)):
                eq = det([[self.parts[i].points[j][0] - self.plane_r[0], 
                          self.parts[i].points[j][1] - self.plane_r[1],
                          self.parts[i].points[j][2] - self.plane_r[2]],
                          [self.plane_dcm[0][0] - self.plane_r[0], 
                           self.plane_dcm[0][1] - self.plane_r[1], 
                           self.plane_dcm[0][2] - self.plane_r[2]],
                           [self.plane_dcm[1][0] - self.plane_r[0],
                            self.plane_dcm[1][1] - self.plane_r[1],
                            self.plane_dcm[1][2] - self.plane_r[2]]])
#                print(eq>=0)            
                place.append(eq >= 0)
            if sum(place) != 0 and sum(place) != 8:
                result.append(i) 
            print()
        return result
    
if __name__ == "__main__":
    db1 = DuoBlock([[[0, 5, 6], [8, 0, -2]], [[0, 0, 3], [2, -1, 0]]])
    print(db1.parts[0].width)
    print()
    
    # тест 1: плоскость под углом 45гр. к Оху без смещения
    db1.set_plane([0,0,0], [[1, 0, 0], [0, sqrt(2)/2, 0], [0, sqrt(2)/2, 0]])
    print("Test1:")
    arr = db1.check_intercept()
    print(arr)
    print()
    
     # тест 2: плоскость под углом 45гр. к Оху со смещением от начала координат
    db1.set_plane([10,10,10], [[11, 10, 0], [10, 10 + sqrt(2)/2, 0], [10, 10 + sqrt(2)/2, 0]])
    print("Test2:")
    arr1 = db1.check_intercept()
    print(db1.check_intercept())
    print()
    
    # тест 3: плоскость под углом 45гр. к Оху со смещением от начала координат
    db1.set_plane([-10,-10,-10], [[-9, -10, 0], [-10, -10 + sqrt(2)/2, 0], [-10, -10 + sqrt(2)/2, 0]])
    print("Test3:")
    print(db1.check_intercept())
    print()
    
