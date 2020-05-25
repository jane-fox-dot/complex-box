#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from singleblock import SingleBlock
import numpy as np
from numpy.linalg import det

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from itertools import combinations

vertices = 8

class MultiBlock(object):
    u"""
    Класс для описания объекта, состоящего из n соприкасающихся 
    параллелепипедов.
    Содержит сам объект и описание секущей плоскости
    """
    
    def __init__(self, r=None):
        self.n = len(r)
        self.part = np.array([])
        
        try:
            for i in range(self.n):
                self.part = np.append(self.part,SingleBlock(r[i]))
        except:
            pass
        
        # коэффициенты в уравнении секущей плоскости
        self.pA = None
        self.pB = None
        self.pC = None
        self.pD = None
        
    
    def set_plane(self, pl):
        u"""
            Функция-сеттер для плоскости сечения
            
        Parameters
        ----------
        pl - массив с пространственными координатами 3 точек, по которым
        строится секущая плоскость
        """
        
        plane = np.array(pl)
        
        x = plane[:,0]
        y = plane[:,1]
        z = plane[:,2]
        
        d1 = det([[y[1]-y[0], z[1]-z[0]], [y[2]-y[0], z[2]-z[0]]]) 
        d2 = det([[x[1]-x[0], z[1]-z[0]], [x[2]-x[0], z[2]-z[0]]]) 
        d3 = det([[x[1]-x[0], y[1]-y[0]], [x[2]-x[0], y[2]-y[0]]])
    
        self.pA = d1
        self.pB = -d2
        self.pC = d3
        self.pD = -x[0]*d1 + y[0]*d2 - z[0]*d3 
        
        
    def deviation_from_plane(self, point):        
        u"""
            Функция, определяющая отклонение заданной точки от плоскости 
            сечения.
            
        Parameters
        ----------
        point - координаты точки, массив 1x3
            
        Returns
        ----------
        result (double) - числовое значение отклонения точки от плоскости
        """
        
        return self.pA*point[0] + self.pB*point[1] + self.pC*point[2] + self.pD
    
    
    def check_intercept(self):
        u"""
            Функция проверки факта пересечения плоскостью параллелепипедов
            
        Returns
        ----------
        2D list - массив координат точек пересечения
        False - плоскость не пересекает ни одну часть объекта
        """
        
        if self.pA is None or self.pB is None or self.pC is None or \
        self.pD is None:
            return []
        
        result = []
        
        for i in range(len(self.part)):
            for pair in list(combinations(self.part[i].vertex, 2)):
                if self.is_edge(pair):
                    d = self.deviation_from_plane(pair[0])
                    dd = self.deviation_from_plane(pair[1])
                    if d*dd <= 0:
                        point = self.find_point(pair) 
                        if point: result.append(point)
        return result
    
    
    def is_edge(self,points):
        u"""
            Функция, проверяющая, является ли пара произвольных точек ребром 
            параллелепипеда
            
        Returns
        ----------
        boolean - результат проверки
    
        """
        
        p1 = np.array(points[0])
        p2 = np.array(points[1])
        
        if p1[0] != p2[0] and p1[1] == p2[1] and p1[2] == p2[2]:
            return True
        if p1[0] == p2[0] and p1[1] != p2[1] and p1[2] == p2[2]:
            return True
        if p1[0] == p2[0] and p1[1] == p2[1] and p1[2] != p2[2]:
            return True
        return False
    
    
    def find_point(self, edge):
        u"""
            Функция для определения координат точки пересечения отдельно 
            взятого ребра и плоскости сечения. 
         
        Parameters
        ----------
        edge - координаты концов отрезка (ребра)
            
        """
  
        q = np.array(edge[0])
        v = np.array(edge[1]) - np.array(edge[0])
        
        if v[0] != 0 and (self.pA == 0 or self.pA % v[0] == 0): 
            return None
        if self.pA != 0 and v[0] % self.pA == 0:
            return None
        if v[1] != 0 and (self.pB == 0 or self.pB % v[1] == 0): 
            return None
        if self.pB != 0 and v[1] % self.pB == 0:
            return None
        if v[2] != 0 and (self.pC == 0 or self.pC % v[2] == 0): 
            return None
        if self.pC != 0 and v[2] % self.pC == 0:
            return None
        
        k = 1
        if self.pA != 0 and self.pB == 0 and self.pC == 0:
            k = -self.pD/self.pA
        elif self.pA == 0 and self.pB !=0 and self.pC == 0:
            k = -self.pD/self.pB
        elif self.pA == 0 and self.pB ==0 and self.pC != 0:
            k = -self.pD/self.pC

        if v[0] != 0 and v[1] == 0 and v[2] == 0:       # \\ Ox
            return [k, q[1], q[2]]
        if v[0] == 0 and v[1] != 0 and v[2] == 0:      # \\ Oy
            return [q[0], k, q[2]]
        if v[0] == 0 and v[1] == 0 and v[2] != 0:      # \\ Oz
            return [q[0], q[1], k]    
        return None
       
            
    def define_borders(self):
        u"""
            Вспомогательная функция для построения плоскости сечения.
            Находит границы изменения каждой координаты для всех составных 
            частей объекта
            
        Returns
        ----------
        x_min, x_max - границы изменения x
        y_min, y_max - границы изменения y
        z_min, z_max - границы изменения z
        """
        
        x_min = np.amin(self.part[0].vertex[:,0])
        x_max = np.amax(self.part[0].vertex[:,0])
        
        y_min = np.amin(self.part[0].vertex[:,1])
        y_max = np.amax(self.part[0].vertex[:,1])
    
        z_min = np.amin(self.part[0].vertex[:,2])
        z_max = np.amax(self.part[0].vertex[:,2])
        
        for i in range(1, len(self.part)):
                a = np.amin(self.part[i].vertex[:,0])
                if a < x_min: x_min = a
                a = np.amax(self.part[i].vertex[:,0])
                if a > x_max: x_max = a
    
                b = np.amin(self.part[i].vertex[:,1])
                if b < y_min: y_min = b
                b = np.amax(self.part[i].vertex[:,1])
                if b > y_max: y_max = b
                
                c = np.amin(self.part[i].vertex[:,2])
                if c < z_min: z_min = c
                c = np.amax(self.part[i].vertex[:,2])
                if c > z_max: z_max = c
         
        return x_min, x_max, y_min, y_max, z_min, z_max
    
    
    def show_blocks(self, *points, plane = 0):
        u"""
            Построение составного объекта в трёхмерном пространстве
        
        Parameters
        ----------
        points (optional) - массив точек для отображения на чертеже
        plane - флаг, отвечающий за построение плоскости сечения    

        """
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        
        for i in range(len(self.part)):
            self.plot_cuboid(self.part[i].v1, self.part[i].v2,ax)
            
        ax.mouse_init()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        if points:
            for i in range(len(points[0])):
                ax.scatter(points[0][i][0], points[0][i][1], points[0][i][2], 
                           color='r')
            
        if plane:
            b = self.define_borders()
           
            x_range = np.arange(b[0], b[1], 0.1)
            y_range = np.arange(b[2], b[3], 0.1)
                
            xx, yy = np.meshgrid(x_range, y_range)
                
            x = np.linspace(b[0], b[1], num=10)
            y = np.linspace(b[2], b[3], num=10)
            z = np.linspace(b[4], b[5], num=10)
                
            x1, z1 = np.meshgrid(x, z)
            x2, y2 = np.meshgrid(x, y)
            y3, z3 = np.meshgrid(y, z)
                
            # плоскость с уравнением вида x=const
            if self.pA != 0 and self.pB == 0 and self.pC == 0:
                x31 = np.ones_like(y3)*(-self.pD/self.pA)           
                ax.plot_surface(x31, y3, z1, color='limegreen', alpha = 0.6)
            
            # плоскость с уравнением вида y=const
            if self.pA == 0 and self.pB !=0 and self.pC == 0:
                y11 = np.ones_like(x1)*(-self.pD/self.pB)           
                ax.plot_surface(x1, y11, z1, color='limegreen', alpha = 0.6)
                
            # плоскость с уравнением вида z=const  
            if self.pA == 0 and self.pB == 0 and self.pC != 0:      
                z21 = np.ones_like(x2)*(-self.pD/self.pC)       
                ax.plot_surface(x2, y2, z21, color='limegreen', alpha = 0.6)
        plt.show()
        
        
    def plot_cuboid(self, v1, v2, ax): 
        u"""
            Построение отдельного блока объекта
            
        Parameters
        ----------
        v1, v2 - векторы, на которых был построен объект типа SingleBlock
        ax - вспомогательная переменная для построения графика    
        """
        x_min = np.minimum(v1[0], v2[0])
        x_max = np.maximum(v1[0], v2[0])
    
        y_min = np.minimum(v1[1], v2[1])
        y_max = np.maximum(v1[1], v2[1])
    
        z_min = np.minimum(v1[2], v2[2])
        z_max = np.maximum(v1[2], v2[2])
    
        x = np.linspace(x_min, x_max, num=10)
        y = np.linspace(y_min, y_max, num=10)
        z = np.linspace(z_min, z_max, num=10)
        
        x1, z1 = np.meshgrid(x, z)
        y11 = np.ones_like(x1)*(y_min)
        y12 = np.ones_like(x1)*(y_max)
        x2, y2 = np.meshgrid(x, y)
        z21 = np.ones_like(x2)*(z_min)
        z22 = np.ones_like(x2)*(z_max)
        y3, z3 = np.meshgrid(y, z)
        x31 = np.ones_like(y3)*(x_min)
        x32 = np.ones_like(y3)*(x_max)
        
        # outside surface
        ax.plot_wireframe(x1, y11, z1, color='k', rcount=4, ccount=4,\
                          alpha = 0.5)
        # inside surface
        ax.plot_wireframe(x1, y12, z1, color='k', rcount=4, ccount=4,\
                          alpha = 0.5)
        # bottom surface
        ax.plot_wireframe(x2, y2, z21, color='k', rcount=4, ccount=4,\
                          alpha = 0.5)
        # upper surface
        ax.plot_wireframe(x2, y2, z22, color='k', rcount=4, ccount=4,\
                          alpha = 0.5)
        # left surface
        ax.plot_wireframe(x31, y3, z3, color='k', rcount=4, ccount=4,\
                          alpha = 0.5)
        # right surface
        ax.plot_wireframe(x32, y3, z3, color='k', rcount=4, ccount=4,\
                          alpha = 0.5)