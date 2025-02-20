import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

p0 = np.array([0,0]) #Stationary
p1 = np.array([10,35]) #Needs to be solved
p2 = np.array([-25,10]) #Moves in circles

c = np.array([-30,0])

circleGenerator = np.array([c, p2])

x = np.concatenate((p0,p1,p2))[np.newaxis].T

phiStart = np.arctan(10/5)

A = np.matrix([[1,0,-1,0,0,0],[0,1,0,-1,0,0],[0,0,1,0,-1,0],[0,0,0,1,0,-1]])

l = A*x

L = l.reshape((-1,2))

length = []

for i in L:
    length.append(np.sqrt(i[0,0]**2 + i[0,1]**2))

def errorFun(jPoints,cPoints,fPoints,linkMatrix,deltaPhi,linkLengths):
    
    cLength = cPoints[0] - cPoints[1]
    cLength = np.sqrt(cLength[0]**2 + cLength[1]**2)
    newCPoint = cPoints[0] + np.array([cLength*np.cos(deltaPhi), cLength*np.sin(deltaPhi)])
    
    x = np.concatenate((fPoints,jPoints,newCPoint))[np.newaxis].T
    
    l = linkMatrix*x
    L = l.reshape((-1,2))
    
    newLinkLengths = []
    
    for i in L:
        newLinkLengths.append(np.sqrt(i[0,0]**2 + i[0,1]**2))       

    lengthError = []
    
    for new, old in zip(newLinkLengths,linkLengths):
        lengthError.append(old-new)
            
    return lengthError

phi = []
currentPhi = 0
while(currentPhi <= 4*np.pi):
    phi.append(currentPhi)
    currentPhi+=0.1

newPoint = p1

for i in phi:
    plt.clf()
    oldPoint = newPoint
    
    cLength = circleGenerator[0] - circleGenerator[1]
    cLength = np.sqrt(cLength[0]**2 + cLength[1]**2)
    cPoint = circleGenerator[0] + np.array([cLength*np.cos(phiStart+i), cLength*np.sin(phiStart+i)])
    
    def opFun(points):
        return errorFun(points,circleGenerator, p0, A, phiStart+i,length)
    
    solvedPoints = least_squares(opFun,p1)
    newPoint = solvedPoints.x
    
    plt.xlim(-50,20)
    plt.ylim(-20,40)
    
    plt.scatter(cPoint[0],cPoint[1], color="red")
    plt.scatter(circleGenerator[0,0],circleGenerator[0,1], color="red")
    
    plt.scatter(newPoint[0], newPoint[1], color = "blue")
    plt.scatter(p0[0],p0[1],color="blue")
    
    plt.plot([circleGenerator[0,0], cPoint[0]],[circleGenerator[0,1],cPoint[1]],color="red",linestyle="dashed")
    plt.plot([cPoint[0], newPoint[0]],[cPoint[1], newPoint[1]],color="black")
    plt.plot([newPoint[0],p0[0]],[newPoint[1],p0[1]],color="black")
    
    plt.pause(0.1)