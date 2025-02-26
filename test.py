import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

import mechanism as mech
import solver as sol

import time

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

points = newSolver.solve(phiStart+0.1)

print("Points:",points)

#---------------------------------------------------------
#----------Testing with a more complex mechanism----------
#---------------------------------------------------------
cGen = np.array([[0,0],[0,1]])

p0 = np.array([1,1])
p1 = np.array([2,1])
p2 = np.array([4,1])
p3 = np.array([2,-2])
p4 = np.array([4,-2])

fixPoints = np.array([p3,p4])
freePoints = np.array([p1,p2])

linkConnections = np.array([[0,1],[1,2],[1,3],[2,4]])

linkNumbers = np.array([0,1,2,3])

lengths = np.array([2,2,3,3])

complexMechanism = mech.mechanism(cGen,lengths,fixPoints,freePoints)

complexMechanism.generateLinkMatrix(linkConnections,linkNumbers)

complexMechanism.showLinkMatrix()

complexSolver = sol.solver(complexMechanism)

kinematics = complexSolver.prepareKinematics(0.05)

pauseInterval = 10/len(kinematics)
start = time.time()
for i in kinematics:
    plt.clf()
    plt.scatter(0,0,color="yellow")
    plt.xlim(-3,6)
    plt.ylim(-3,6)
    
    for j in i:
        plt.scatter(j[0],j[1])
    plt.pause(pauseInterval)
print("Animation was on screen for",time.time()-start,"seconds")