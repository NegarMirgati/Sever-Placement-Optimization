from __future__ import division
import matplotlib.pyplot as plt
import math
import random

import Global
import Database
import Request


class SimAnneal(object):
	def __init__(self, db, T = -1, alpha = -1, stopping_T = -1, stoppingIter = -1):
		self.outfile = open('log.txt', 'w')
		self.dimension = Global.NUM_OF_REQUESTS
		self.temprature = math.sqrt(self.dimension) if T == -1 else temprature
		self.alpha = 0.995 if alpha == -1 else alpha
		self.stoppingTemperature = 0.00000001 if stopping_T == -1 else stopping_T
		self.stoppingIter = 1000 if stoppingIter == -1 else stopping_iter
		self.iteration = 1
		self.curSolution = self.initialSolution()
		self.database = db
		self.numUsedDCs = 0
		self.numPlacedReqs = 0

		self.curFitness = self.calcFitness(self.curSolution)
		self.initialFitness = self.curFitness
		self.bestFitness = self.curFitness

		self.fitnessList = [self.curFitness]

	def initialSolution(self):
		retList = []
		for i in range(0, Global.NUM_OF_REQUESTS):
			retList.append(random.choice(range(1, Global.NUM_OF_NODES + 1)))
		print(retList)
		return retList

	def calcFitness(self, sol):
		usedDCs = set()
		numOfPlacedReqs = 0
		for i in range(0, self.dimension):
			correspondingReq = Request.requests[i]
			(cpu, mem) = correspondingReq.getCPUAndMem()
			currentNode = sol[i]
			currentDC = self.database.getCorrespondingDC(currentNode)
			currentDC = self.database.getCorrespondingDC(currentNode)
			if(self.database.canPlaceReqOnNode(currentNode, cpu, mem)):
				self.database.updateNodeTable(currentNode, cpu, mem)
				self.database.updateDCTable(currentDC, cpu, mem)
				numOfPlacedReqs += 1
				usedDCs.add(currentDC)

		print ('reqs = ', str(numOfPlacedReqs), ' used dcs = ', len(usedDCs),  ' fitness = ',  ((Global.NUM_OF_DCS - len(usedDCs)) * numOfPlacedReqs))
		self.outfile.write('%%%%%%%%%%%%%%%%%%%%%%')
		for n in usedDCs:
				self.outfile.write(str(n) + " ,")

		self.outfile.write('&&&&&&&&&&&&&&&&&&&')
		return ((Global.NUM_OF_DCS - len(usedDCs)) * numOfPlacedReqs) + 0.01
	
	def calcAcceptProbability(self, candidateFitness):
		 return math.exp(-abs(candidateFitness - self.curFitness) / self.temprature)
	
	def acceptCandidate(self, candidate):
		candidateFitness = self.calcFitness(candidate)
		if(candidateFitness > self.curFitness):
			self.curFitness = candidateFitness
			print('candft', candidateFitness)
			self.curSolution = candidate
			self.updateBestSolutionAndFitness(candidate, candidateFitness)
		else:
			if (random.random() < self.calcAcceptProbability(candidateFitness)):
				self.curFitness = candidateFitness
				self.curSolution = candidate
	
	def updateBestSolutionAndFitness(self, candidate, candidateFitness):
		if (candidateFitness > self.bestFitness):
				self.bestFitness = candidateFitness
				self.bestSolution = candidate

	def anneal(self):
		while (self.temprature >= self.stoppingTemperature and self.iteration < self.stoppingIter):
			self.database.renewConnection()
			candidate = list(self.curSolution)
			l = random.randint(2, self.dimension - 1)
			i = random.randint(0, self.dimension - l)
			candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
			self.acceptCandidate(candidate)
			self.temprature *= self.alpha
			self.iteration += 1

			self.fitnessList.append(self.curFitness)
			for i in range(0, len(self.curSolution)):
				self.outfile.write(str(i + 1) + " : " + str(self.curSolution[i]) + ", ")

			self.outfile.write('\n***********\n')


		print('Best fitness obtained: ', self.bestFitness)
		print('Improvement over greedy heuristic: ',
			  round((self.initialFitness - self.bestFitness) / (self.initialFitness), 4))

		self.printDBStatus()
		self.printSolution()

	def printDBStatus(self):
			self.database.printDCTable()
			self.database.printNodeTable()
	
	def printSolution(self):
		solFile = open('solution.txt', 'w')
		solFile.write('###################')
		for i in range(0, Global.NUM_OF_REQUESTS):
			solFile.write("Req No : " + str(i + 1) + " : "  + str(self.bestSolution[i]) + "\n")
		solFile.write("###################")

	def plotLearning(self):
		plt.plot([i for i in range(len(self.fitnessList))], self.fitnessList)
		plt.ylabel('Fitness')
		plt.xlabel('Iteration')
		plt.show()

