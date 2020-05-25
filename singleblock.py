# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:59:38 2019

@author: Acer
"""

import numpy as np

vertices = 8

class SingleBlock(object):
    u"""
    Класс для описания параллелепипеда, заданного двумя векторами.
    """
    
    def __init__(self, r):
        self.v1 = r[0]
        self.v2 = r[1]
       
        self.vertex = np.array([[0, 0, 0] for i in range(vertices)])
        
        self.vertex[0] = np.array([self.v1[0], self.v1[1], self.v1[2]])
        self.vertex[1] = np.array([self.v1[0], self.v2[1], self.v1[2]])
        self.vertex[2] = np.array([self.v2[0], self.v2[1], self.v1[2]])
        self.vertex[3] = np.array([self.v2[0], self.v1[1], self.v1[2]])
        self.vertex[4] = np.array([self.v1[0], self.v1[1], self.v2[2]])
        self.vertex[5] = np.array([self.v2[0], self.v1[1], self.v2[2]])
        self.vertex[6] = np.array([self.v2[0], self.v2[1], self.v2[2]])
        self.vertex[7] = np.array([self.v1[0], self.v2[1], self.v2[2]])
                        
        self.height = abs(self.v2[2] - self.v1[2])
        self.width = abs(self.v2[0] - self.v1[0])
        self.length = abs(self.v2[1] - self.v1[1])
        
