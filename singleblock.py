# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:59:38 2019

@author: Acer
"""

class SingleBlock(object):
    u"""
    Класс для описания параллелепипеда, заданного двумя векторами.
    """
    
    def __init__(self, r):
        self.v1 = r[0]
        self.v2 = r[1]
        
        self.points = [[0, 0, 0] for i in range(8)]
        
        self.points[0] = [self.v1[0], self.v1[1], self.v1[2]]
        self.points[1] = [self.v1[0], self.v2[1], self.v1[2]]
        self.points[2] = [self.v2[0], self.v2[1], self.v1[2]]
        self.points[3] = [self.v2[0], self.v1[1], self.v1[2]]
        self.points[4] = [self.v1[0], self.v1[1], self.v2[2]]
        self.points[5] = [self.v2[0], self.v1[1], self.v2[2]]
        self.points[6] = [self.v2[0], self.v2[1], self.v2[2]]
        self.points[7] = [self.v1[0], self.v2[1], self.v2[2]]
        
        self.height = abs(self.v2[2] - self.v1[2])
        self.width = abs(self.v2[0] - self.v1[0])
        self.length = abs(self.v2[1] - self.v1[1])
        
        
# if __name__ == "__main__":