"""
Created on Sat Feb  2 18:37:41 2019

@author: Bharathy
"""
from pulp import *

#Create lists for the methods and grades
method = ['method1','method2']
grade = ['defective', 'grade1','grade2','grade3','grade4']
grade2 = grade

#Dictionaries for demand, cost and yield rates
demand = {
        'defective':0,
        'grade1': 3000,
        'grade2': 3000,
        'grade3': 2000,
        'grade4': 1000        
        }

cost = {
        'method1': 50,
        'method2': 70
        }

refireCost = 25
maxCapacity = 20000

meltingYield = {
                'defective': { 'method1':0.30, 'method2':0.20}, 
                'grade1': { 'method1':0.30, 'method2':0.20},
                'grade2': { 'method1':0.20, 'method2':0.25},
                'grade3': { 'method1':0.15, 'method2':0.20},
                'grade4': { 'method1':0.05, 'method2':0.15},
        }

refireYield = {
        'defective': {'defective': 0.30, 'grade1': 0.25, 'grade2':0.15, 'grade3':0.20, 'grade4':0.10},
        'grade1': {'defective': 0, 'grade1': 0.30, 'grade2':0.30, 'grade3':0.20, 'grade4':0.20},
        'grade2': {'defective': 0, 'grade1': 0, 'grade2':0.40, 'grade3':0.30, 'grade4':0.30},
        'grade3': {'defective': 0, 'grade1': 0, 'grade2':0, 'grade3':0.50, 'grade4':0.50},
        'grade4': {'defective': 0, 'grade1': 0, 'grade2':0, 'grade3':0, 'grade4':0},        
        }

#Create 'prob' variable to contain model data
prob = LpProblem('Minimize Cost', LpMinimize)

#Create model variables
x = LpVariable.dicts('Number Produced in 1st stage', method, 0, None, LpInteger)
y = LpVariable.dicts('Number Refired',grade,0, None, LpInteger)

#Objective function to minimize cost
prob += lpSum(x[m]*cost[m] for m in method) + lpSum(y[g]*refireCost for g in grade)

#Demand constraint
for g in grade:
    prob+= (lpSum(x[m]*meltingYield[g][m] for m in method) - y[g] + lpSum(y[g2]*refireYield[g2][g] for g2 in grade2)) >= demand[g]
      
#capacity Constraint
prob += lpSum(x[m] for m in method) + lpSum(y[g] for g in grade) <= maxCapacity

#refiring contraint
for g in grade:
    prob+= y[g] <= lpSum(meltingYield[g][m]*x[m] for m in method)
    
prob.solve()

for v in prob.variables():
    print(v.name,'=', v.varValue)
    






