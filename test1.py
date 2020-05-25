#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiblock import MultiBlock
from math import sqrt
import numpy as np

t = MultiBlock([[[0, 8, 5], [7,0,0]], [[0, 3, 4], [-4, 0, 0]]])
   
t.set_plane([[3,4,1], [-2,5,1], [0,9,1]])

t.show_blocks(plane=1)

p = t.check_intercept()
print(p)
t.show_blocks(p, plane=1)