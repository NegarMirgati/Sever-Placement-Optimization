from __future__ import division
import math

import Global
import random
import CustomeDatabase
import Request

class Firefly:
    def __init__(self):
        self.illumination = 1.0
        self.fitness = 1.0
        self.genes = [None] * Global.DIMENSION
        self.Database = CustomeDatabase.CustomeDatabase()
        self.numUsedDCs = 0
        self.numPlacedReqs = 0

    def initAgent(self):
        for j in range(0, Global.DIMENSION):
			r = random.uniform(0, 1)
			self.genes[j] = int(math.floor(r * (Global.upperBound[j] - Global.lowerBound[j]) + Global.lowerBound[j]))

    def getFitness(self):
        return self.fitness

    def calcFitness(self):
        usedDCs = set()
        placedReqs = 0
        for i in range(0, Global.DIMENSION):
            correspondingReq = Request.requests[i]
            (cpu, mem) = correspondingReq.getCPUAndMem()
            currentNode = self.genes[i]
            currentDC = self.Database.getCorrespondingDC(currentNode)
            if(currentNode > Global.NUM_OF_NODES):
                continue
            if(self.Database.canPlaceReqOnNode(currentNode, cpu, mem)):
                self.Database.updateNodeTable(currentNode, cpu, mem)
                self.Database.updateDCTable(currentDC, cpu, mem)
                
                usedDCs.add(currentDC)
                placedReqs += 1

        self.fitness = + ((Global.NUM_OF_DCS - len(usedDCs)) ** 2) + ((placedReqs) ** 2)
        self.numPlacedReqs = placedReqs
        self.numUsedDCs = len(usedDCs)
        #print('numUsedDCs', len(usedDCs), ' Num not placed', Global.NUM_OF_REQUESTS - placedReqs)
        #print('fitness = ', self.fitness)

    def setIllumWRTFitness(self):
        self.illumination = self.fitness
    
    def getIllumination(self):
        return self.illumination
    
    def brighterThan(self, firefly):
        if(self.illumination > firefly.illumination):
            return True
        return False

    def getByIndex(self, index):
        return self.genes[index]

    def setByIndex(self, index, val):
        self.genes[index] = val
    
    def getNumPlacedReqs(self):
        return self.numPlacedReqs

    def getNumUsedDCs(self):
        return self.numUsedDCs

    def limitUpperByIndex(self, index):
        if(self.genes[index] > Global.upperBound[index]):
			self.genes[index] = Global.upperBound[index]

    def limitLowerByIndex(self, index):
        if(self.genes[index] < Global.lowerBound[index]):
			self.genes[index] = Global.lowerBound[index]
    
    def reinitDB(self):
        self.Database.reinit()

    def printDBStatus(self):
        self.Database.printDCTable()
        self.Database.printNodeTable()
		