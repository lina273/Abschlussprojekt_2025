import numpy as np

class mechanism:
    def __init__(self,circleGenerator ,linkLengths,fixPoints,freePoints,linkMatrix = []):
        #Initializing values, under normal conditions the link matrix has to be generated
        self.circleGenerator = circleGenerator
        
        self.linkMatrix = linkMatrix
        self.linkLengths = linkLengths
        
        self.fixPoints = fixPoints
        self.freePoints = freePoints
        
        print("Mechanism object created.")
        
        
    def updatePoints(self,circleGenerator,fixPoints,freePoints):
        #In case a manual update is required
        self.circleGenerator = circleGenerator
        
        self.fixPoints = fixPoints
        self.freePoints = freePoints
        
        
    def getPoints(self):
        #for debugging
        fixPoints = self.mechanism.fixPoints.flatten()
        
        return np.concatenate((self.circleGenerator,self.freePoints,fixPoints))
    
    
    def generateLinkMatrix(self,linkConnections,linkNumbers):
        
        print("Begin generating matrix...")
        
        #Initializing an empty matrix of the correct size
        elements = np.size(linkConnections)
        uniquePoints = len(np.unique(np.concatenate(linkConnections)))
        
        matrix = np.zeros((elements,uniquePoints*2))
        
        print("Empty matrix created.")
        
        #Building the matrix line by line
        for i,j in zip(linkConnections,linkNumbers):
            print("Building matrix...")
            matrix[j*2,i[0]*2] = 1
            matrix[j*2,i[1]*2] = -1
            
            matrix[j*2+1,i[0]*2+1] = 1
            matrix[j*2+1,i[1]*2+1] = -1
        
        self.linkMatrix = np.matrix(matrix)
        
        print("Matrix generated.")
        
        return matrix
    
    def showLinkMatrix(self):
        #For debugging
        print("linkMatrix:\n",self.linkMatrix)
        return self.linkMatrix