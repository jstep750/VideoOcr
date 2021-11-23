#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 12:52:13 2019

@author: jordansauchuk
"""

import pandas as pd

df = pd.read_csv('demodf.txt', sep=" ", header=None, names=['a', 'b', 'c',])
print(df)

dataset = pd.read_csv('demodf.txt', delimiter="\t")
print(dataset)
dataset.head(10)




