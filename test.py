import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

import mechanism as mech
import solver as sol

#----------------------------------------------------------------------------------
#--------------------Testing the object oriented implementation--------------------
#----------------------------------------------------------------------------------

p0 = np.array([0,0]) #Stationary
p1 = np.array([10,35]) #Needs to be solved
p2 = np.array([-25,10]) #Moves in circles

c = np.array([-30,0])

linkNumbers = np.array([0,1])
linkConnections = np.array([[0,1],[1,2]])

circleGenerator = np.array([c, p2])

x = np.concatenate((p0,p1,p2))[np.newaxis].T

phiStart = np.arctan(10/5)

A = np.matrix([[1,0,-1,0,0,0],[0,1,0,-1,0,0],[0,0,1,0,-1,0],[0,0,0,1,0,-1]])

l = A*x

L = l.reshape((-1,2))

length = []

for i in L:
    length.append(np.sqrt(i[0,0]**2 + i[0,1]**2))

print("Link lengths: ",length)

newMechanism = mech.mechanism(circleGenerator,length,p0,p1)

newMechanism.generateLinkMatrix(linkConnections,linkNumbers)

newSolver = sol.solver(newMechanism)

points = newSolver.solve(0.1)

print("Points:",points)





#AAAHHHHHHHHHHHHHH