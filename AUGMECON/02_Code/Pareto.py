# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 18:36:59 2022

@author: amiri
"""
import sys
import numpy as np
import pandas as pd
import gurobipy as gp
from itertools import product
from gurobipy import GRB,Model,quicksum; qsum=quicksum
from pandas import ExcelWriter 
import xlsxwriter
from model import *

Iterations = 10 

intervalland = payoff12 - payoff22 
step1 = [payoff12 - (intervalland/Iterations)*step for step in range(0, Iterations+1)]
step1 = [round(num, 6) for num in step1] 

intervalwater = payoff13 - payoff33
step2 = [payoff13 - (intervalwater/Iterations)*steps for steps in range(0, Iterations+1)]
step2 = [round(nums, 9) for nums in step2] 

writer = pd.ExcelWriter('pareto_solutions.xlsx', engine='xlsxwriter')
solutions = []
varInfo = {}
psolu={}
mf.params.NoRelHeurWork=900

softlimit =5000 
hardlimit =20000 

def softtime(mf, where):
    if where == GRB.Callback.MIP:
        runtime = mf.cbGet(GRB.Callback.RUNTIME)
        objbst = mf.cbGet(GRB.Callback.MIP_OBJBST)
        objbnd = mf.cbGet(GRB.Callback.MIP_OBJBND)
        gap = abs((objbst - objbnd) / objbst)

        if runtime > softlimit and gap < MIPgap*2: #0.03:
            mf.terminate()

mf.setParam('TimeLimit', hardlimit)
# =============================================================================
# # pareto layer with three objective function -- outer loop water 
# =============================================================================
print("*"*100)
for i__, ew in enumerate(step2):  
    slw = mf.addVar(name="slw", vtype=GRB.CONTINUOUS) #slack variable for water objective function
    e_constraint_w = mf.addConstr((slw == ew - Total_water), 'water_slack_constraint')
    for j__, el in enumerate(step1):
        print(f"*** outer iteration is(water):  {i__} , inner iteration is(land):  {j__}")
        print(f"epsilon_water is:{ew}")
        print(f"epsilon_land is:{el}")  
        sll = mf.addVar(name="sll", vtype=GRB.CONTINUOUS) #slack variable for land objective function
        e_constraint_l = mf.addConstr((sll == el - Total_land), 'land_slack_constraint')
        e_obj = mf.addVar(name="e_obj", vtype=GRB.CONTINUOUS) 
        epsilonobjectivefunction = mf.addConstr(e_obj == Total_cost - (epsilon*((sll/intervalland)+(slw/intervalwater))))
        mf.setObjective(e_obj, GRB.MINIMIZE)
        mf.update()
        try: 
            mf.optimize(softtime)
            solutions.append((Total_cost.getAttr("x"), Total_land.getAttr("x"), Total_water.getAttr("x"))) 
            varInfo[i__,j__] = [(v.varName, v.X) for v in mf.getVars() if v.X >= 0]   
            psolu[i__, j__]=pd.DataFrame(varInfo[i__,j__])
            psolu[i__, j__].to_excel(writer, sheet_name = str(i__) + ',' + str(j__))
            mf.remove(e_constraint_l)
            mf.remove(epsilonobjectivefunction)
            mf.update()
        except Exception as error:
            print(error)
            print(f"*******iteration {i__} , {j__} is infeaseable*******")
            solutions.append((0, 0, 0)) 
            mf.remove(e_constraint_l)
            mf.remove(epsilonobjectivefunction)
            mf.update()
            pass 
    mf.remove(e_constraint_w)
    mf.update()
        
    
writer.save() 
pareto = pd.DataFrame(solutions)
pareto.to_excel("pareto.xlsx")
 