# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 08:45:46 2022

@author: amiri
"""
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

data = pd.read_excel("pareto.xlsx")

X = np.array(data['cost']) # land
Y = np.array(data['land']) # cost
Z = np.array(data['water']) # water

XP= 6.480272773	
YP= 904.532943	
ZP= 2403.729901

ax1 = plt.axes()
fig1 = plt.scatter(X, Y, c=Z, cmap='viridis') 
fig1 = plt.scatter(XP,YP, marker='x', s=70, color='red')   #####line
ax1.text(6.35, 897	, "Compromise \nSolution", color='red',fontsize=8)
bar1 = plt.colorbar(fig1);  
bar1.set_label('\nWater use [Million tonnes]') 
ax1.set_xlabel("Cost [Trillion €]") 
ax1.set_ylabel("Land use [Thousand km\u00b2]")
fig1=plt.show()
#======================########################################################
ax2 = plt.axes()
fig2 = plt.scatter(X, Z, c=Y, cmap='viridis') 
#fig2 = plt.scatter(XP,ZP, c=YP, marker= 'x',color='red')     #####line
fig2 = plt.scatter(XP,ZP, marker='x', s=70, color='red')    #####line
ax2.text(6.6, 2400	, "Compromise \nSolution", color='red',fontsize=8)
bar2=plt.colorbar();  # show color scale
bar2.set_label('\nLand use [Thousand km\u00b2]') 
ax2.set_xlabel("Cost [Trillion €]") 
ax2.set_ylabel("Water use [Million tonnes]")
fig2=plt.show()
# #======================########################################################
ax3 = plt.axes()
fig3 = plt.scatter(Y, Z, c=X, cmap='viridis') 
fig3 = plt.plot(Y1,Z1, color='red')     #####line
bar3=plt.colorbar();  
bar3.set_label('\nCost [Trillion €]') 
ax3.set_xlabel("Land use [Thousand km\u00b2]")
ax3.set_ylabel("Water use [Million tonnes]")
ax3.set_title("(b)") 
fig3=plt.show()
