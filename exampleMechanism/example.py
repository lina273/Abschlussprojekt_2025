import numpy as np
from scipy.optimize import least_squares

p0 = np.array([0,0]) #Stationary
p1 = np.array([10,35]) #Needs to be solved
p2 = np.array([-25,10]) #Moves in circles

c = np.array([-30,0])

circleGenerator = np.array([c, p2])

print(circleGenerator)

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
    
    cPoints[1] = cPoints[0] + np.array([cLength*np.cos(deltaPhi), cLength*np.sin(deltaPhi)])
    
    x = np.concatenate((fPoints,jPoints,cPoints[1]))[np.newaxis].T
    
    l = linkMatrix*x
    L = l.reshape((-1,2))
    
    newLinkLengths = []
    
    for i in L:
        newLinkLengths.append(np.sqrt(i[0,0]**2 + i[0,1]**2))       

    lengthError = []
    
    for new, old in zip(newLinkLengths,linkLengths):
        lengthError.append(old-new)
            
    print(lengthError)
    return lengthError



errorFun(p1, circleGenerator, p0, A, phiStart+0.3, length)

#TODO: Implement least squares optimization