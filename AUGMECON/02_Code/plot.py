# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:52:36 2022

@author: amiri
"""

import sys
import numpy as np
import pandas as pd
from itertools import product
from pandas import ExcelWriter 
import xlsxwriter
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
from matplotlib.tri import Triangulation
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

data = pd.read_excel("pareto.xlsx")
X = np.array(data['cost']) # land
Y = np.array(data['land']) # cost
Z = np.array(data['water']) # water

fig = plt.figure(figsize=(10,10))           
ax = plt.axes(projection='3d')

surf = ax.plot_trisurf(Z, Y, X, cmap='viridis_r' , alpha=0.9, linewidth=0.5) 

bar=fig.colorbar(surf, shrink=0.5, alpha=0.9, aspect=10, pad=0.1) 
bar.set_label('\nCost [Trillion €]') 

XP= 6.480272773	
YP= 904.532943	
ZP= 2403.729901

ax.scatter(ZP,YP,XP, c='red',s=50, zorder=100) 
ax.view_init(elev=30, azim=-45)  
ax.text(2398, 895	, 6.3	, "Compromise \nSolution", color='red', )

ax.set_xlabel("Water use [Million tonnes]") 
ax.set_ylabel("Land use [Thousand km\u00b2]")
ax.set_zlabel("Cost [Trillion €]")

plt.show()
