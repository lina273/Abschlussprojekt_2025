import numpy as np
from scipy.optimize import least_squares
import mechanism

class solver:
    def __init__(self,mechanism: mechanism):

        self.mechanism = mechanism
        print("Solver object created.")
    
    
    def validateMechanism(self):
        pass
    
    def presolve(self):
        pass
    
    def solve(self,deltaPhi):
        
        #Required for least squares optimization
        
        #The function takes an array of free points and returns the difference
        #between the correct link lengths and the lengths caused by moving the free point
        def errorFun(points):

            #Moving circle point to new position
            cLength = self.mechanism.circleGenerator[0] - self.mechanism.circleGenerator[1]
            cLength = np.sqrt(cLength[0]**2 + cLength[1]**2)
            newCPoint = self.mechanism.circleGenerator[0] + np.array([cLength*np.cos(deltaPhi), cLength*np.sin(deltaPhi)])

            #Creating column vector x
            x = np.concatenate((self.mechanism.fixPoints,points,newCPoint))[np.newaxis].T
            
            #Calculting current link length after moving corcle point
            l = self.mechanism.linkMatrix*x
            L = l.reshape((-1,2))
            newLinkLengths = []
        
            for i in L:
                newLinkLengths.append(np.sqrt(i[0,0]**2 + i[0,1]**2))       

            lengthError = []
        
            for new, old in zip(newLinkLengths,self.mechanism.linkLengths):
                lengthError.append(old-new)
            
            return lengthError
        
        
        #Solving free points
        #By minimizing the error returned by the error function
        #the points are being "put in the right position"
        solvedPoints = least_squares(errorFun,self.mechanism.freePoints)
        print("Point(s) solved.")
        return solvedPoints
        
    def saveKinematics(self):
        #TODO: Implement a function to calculate and save all positions of the mechanism
        pass