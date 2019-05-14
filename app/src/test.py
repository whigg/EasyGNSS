#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:41:55 2019

@author: edgar
"""
import glob

dir = glob.glob('/home/prout')
print(dir)
if len(dir)==0:
    dir = glob.glob('/home/')
print(dir)
from time import gmtime, strftime
date = strftime('%Y-%m %d-%H %M',gmtime())
print(date)