import numpy as np
from scipy.optimize import least_squares
import mechanism
import time

class solver:
    def __init__(self,mechanism: mechanism):

        self.mechanism = mechanism
        print("Solver object created.")
    
    
    def validateMechanism(self):
        #TODO: Implement this
        pass
    
    def solve(self,deltaPhi):
        
        #Required for least squares optimization
        
        #The function takes an array of free points and returns the difference
        #between the correct link lengths and the lengths caused by moving the free point
        def errorFun(points):
            #Calculating the starting angle according to the points chosen
            #(converting absolute angle to relative)
            cDiff = self.mechanism.circleGenerator[1] - self.mechanism.circleGenerator[0]
            startPhi = np.arctan2(cDiff[1],cDiff[0])
            
            #Moving circle point to new position
            cLength = cDiff
            cLength = np.sqrt(cLength[0]**2 + cLength[1]**2)
            newCPoint = self.mechanism.circleGenerator[0] + np.array([cLength*np.cos(startPhi+deltaPhi), cLength*np.sin(startPhi+deltaPhi)])

            #Creating column vector x
            fixPoints = self.mechanism.fixPoints.flatten()
            
            x = np.concatenate((newCPoint,points,fixPoints))[np.newaxis].T
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
        
        freePoints = np.array(self.mechanism.freePoints).flatten()
     
        #Solving free points
        #By minimizing the error returned by the error function
        #the points are being "put in the right position"
        solvedPoints = least_squares(errorFun,freePoints).x
        
        solvedPoints = solvedPoints.reshape((-1,2))
        
        return solvedPoints
        
    def prepareKinematics(self,resolution):
        start = time.time()
        
        cDiff = self.mechanism.circleGenerator[1] - self.mechanism.circleGenerator[0]
        
        startPhi = np.arctan2(cDiff[1],cDiff[0])
        print("startPhi: ",startPhi)
        phi = []
        currentPhi = 0
        
        pointArray = []
        
        while(currentPhi <= 2*np.pi):
            phi.append(currentPhi)
            currentPhi+=resolution
        for i in phi:
            
            freePoints = self.solve(i).flatten()
            fixPoints = self.mechanism.fixPoints.flatten()
            
            cLength = cDiff
            cLength = np.sqrt(cLength[0]**2 + cLength[1]**2)
            cPoint = self.mechanism.circleGenerator[0] + np.array([cLength*np.cos(startPhi+i), cLength*np.sin(startPhi+i)])
            
            allPoints = np.concatenate((cPoint,freePoints,fixPoints)).reshape((-1,2)).tolist()
            
            pointArray.append(allPoints)
            
            csvArray = []
            
        for i in pointArray:
            csvArray.append(np.array(i).flatten())
            
        print("Prepared points in:", time.time()-start,"seconds.")
        print("Printing points to csv...")
        np.savetxt("points.csv", csvArray, delimiter=",")
        return pointArray
    