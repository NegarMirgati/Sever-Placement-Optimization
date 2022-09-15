from __future__ import division
import customeDatabase
import Request
import Global

import math

class Honey :
	def __init__(self, size):
		self.MAX_LENGTH = size;
		self.nectar = [-1] * self.MAX_LENGTH
		self.usedDCs = set()
		self.numUsedDCs = 0
		self.numPlacedReqs = 0
		self.score = 0
		self.trials = 0
		self.fitness = 0.0
		self.selectionProbability = 0.0
		self.db = customeDatabase.customeDatabase()
		self.initNectar()
		
	def initNectar(self):
		for i in range(0, self.MAX_LENGTH):
			self.nectar[i] = self.db.getRandomNode()
	
	def getFitness(self):
		return self.fitness
	
	def setFitness(self, fitness):
		self.fitness = fitness
	
	def getNectar(self, index):
		return self.nectar[index]

	def getIndex(self, value):
		pos = 0
		for pos in range(0, self.MAX_LENGTH):
			if(self.nectar[pos] == value):
				break
		return pos

	def setNectar(self, index, value):
		self.nectar[index] = value

	def getTrials(self):
		return self.trials
	
	def setTrials(self, value):
		self.trials = value
	
	def getSelectionProbability(self):
		return self.selectionProbability
	
	def setSelectionProbability(self, value):
		self.selectionProbability = value
			
	def getUsedDCs(self):
		return self.usedDCs

	def getScore(self):
		return self.score
	
	def getNumPlacedReqs(self):
		return self.numPlacedReqs
	
	def computeScore(self):
		self.numPlacedReqs = 0
		self.usedDCs = set()	
		self.score = 0
		for i in range(0, self.MAX_LENGTH):
				node = self.nectar[i]
				dc = self.db.getCorrespondingDC(node)
				(cpu, mem) = Request.requests[i].getCPUAndMem()
				if self.db.canPlaceReqOnNode(node, cpu, mem):
						self.db.updateNodeTable(node, cpu, mem)
						self.db.updateDCTable(dc, cpu, mem)
						self.usedDCs.add(dc)
						self.numPlacedReqs += 1
						
		self.numUsedDCs = len(self.usedDCs)
		self.score = self.scoreFunc()
		#print('placedReqs', self.numPlacedReqs, 'numUsedDCs', self.numUsedDCs, 'score = ', self.score)
	
	def scoreFunc(self):
		#return (((Global.NUM_OF_DCS - self.numUsedDCs)/Global.NUM_OF_DCS)) + ((self.numPlacedReqs/Global.NUM_OF_REQUESTS))
		return (((Global.NUM_OF_DCS - self.numUsedDCs) ** 2)) + ((self.numPlacedReqs ** 2))
    		
	def printDatabaseStatus(self):
		self.computeScore()
		self.printScore()
		self.db.printDCTable()
		self.db.printNodeTable()

	def printScore(self):
		fp = open("solutions.txt", "w")
		fp.write("$$$$$ num of placed reqs = ")
		fp.write(str(self.numPlacedReqs) + " num of unused Datacenters " + str(Global.NUM_OF_DCS - self.numUsedDCs))
		sc = self.scoreFunc()
		fp.write(", score = " + str(sc))
		fp.write("$$$$\n")
		fp.close()

	def reinitDB(self):
		self.db.reinit()
	
