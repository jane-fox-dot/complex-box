#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiblock import MultiBlock
from math import sqrt
import numpy as np

t = MultiBlock([[[4, 2, 8], [-3,7,-2]], [[1, 2, -5], [-4, -4, 7]]])
for i in range (len(t.part)):
    print('%2d x%2d x%2d' %(t.part[i].width, t.part[i].length,  t.part[i].height))
  
print()
   


#t.set_plane([[5,-3,1], [0,-3,10], [-2,-3,6]])
t.set_plane([[5,-1,1], [0,-1,10], [-2,-1,6]])
#t.set_plane([[5,7,1], [0,7,10], [-2,7,6]])
#t.set_plane([[5,9,1], [0,9,10], [-2,9,6]])

t.show_blocks(plane=1)

p = t.check_intercept()
print(p)
t.show_blocks(p, plane=1)