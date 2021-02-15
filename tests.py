# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:29:56 2021

@author: henrique.caiafa
"""
import numpy as np

file = open('bpmlist.txt', 'r')
bpmlist = file.readlines()
    
for i in bpmlist:
    print(i)
    
a = [1,2,3]
b = np.array(a)
c = np.zeros((2,3))
c[0] = b

print(c)

    