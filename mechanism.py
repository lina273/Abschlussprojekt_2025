import numpy as np

class mechanism:
    def __init__(self,circleGenerator = [],linkMatrix = [],linkLengths = [],fixPoints = [],freePoints = []):
        
        self.circleGenerator = circleGenerator
        
        self.linkMatrix = linkMatrix
        self.linkLengths = linkLengths
        
        self.fixPoint = fixPoints
        self.freePoints = freePoints
        
        
    def updatePoints(self,circleGenerator,fixPoints,freePoints):
        
        self.circleGenerator = circleGenerator
        
        self.fixPoints = fixPoints
        self.freePoints = freePoints
        
        
    def getPoints(self):
        
        return np.concatenate((self.circleGenerator,self.freePoints,self.fixpoints))
    
    
    def generateLinkMatrix(self,linkConnections):
        
        elements = np.size(linkConnections)
        
        uniquePoints = len(np.unique(np.concatenate(linkConnections)))
        
        matrix = np.zeros((elements,uniquePoints*2))
        
        for i in linkConnections:
            
            matrix[i[0]*2,i[0]*2] = 1
            matrix[i[0]*2,i[1]*2] = -1
            
            matrix[i[0]*2+1,i[0]*2+1] = 1
            matrix[i[0]*2+1,i[1]*2+1] = -1
        
        self.linkMatrix = matrix
        
        return matrix