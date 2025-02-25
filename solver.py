import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import mechanism

class solver:
    def __init__(self,mechanism : mechanism):
        self.mechanism = mechanism
        
    def presolve(self):
        pass
    
    def solve(self):
        pass
    
    def validateMechanism(self):
        pass
    
    def saveKinematics(self):
        pass