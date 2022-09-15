from __future__ import division
import matplotlib.pyplot as plt
import copy
import math
import random

import Global
import  Firefly

class Population :
	def __init__(self, _popSize, _perfectScore):
		self.population = []
		self.evolutionEnded = False
		self.popSize = _popSize
		self.perfectScore = _perfectScore
		self.tempPop = []
		self.gBest = None
		self.bestI = 0
		self.fitnessList =[]
 
	def initGeneration(self):
		for i in range(0, self.popSize):
			firefly = Firefly.Firefly()
			self.population.append(firefly)

	def initBounds(self):
		for i in range(0, Global.DIMENSION):
			Global.lowerBound[i] = 0
			Global.upperBound[i] = Global.NUM_OF_NODES

	def initAgents(self):
		for i in range(0, self.popSize):
				 self.population[i].initAgent()

	def evolve(self):
		print("Start Evolution")
		numIters = 0
		self.dumpFirefly(numIters)
		while(numIters < Global.MAX_GENERATIONS):
			Global.ALPHA = self.calcAlpha()
			for i in range(0, self.popSize):
				self.population[i].calcFitness()
				self.population[i].reinitDB()
				self.population[i].setIllumWRTFitness()

			self.copyGeneration()
			self.population = self.sortFireflies(self.population)
			''' for i in range(0, self.popSize):
					print(self.population[i].getIllumination())
			print("%%%%%%%%%%%%") '''
			self.setBests()
			self.moveFirefiles()
			self.dumpFirefly(numIters)
			numIters += 1

		print("End of optimization: best illumination = " +  str(self.bestI) + '\n')
		print('num of used DCs', self.gBest.getNumUsedDCs(), ' num of placed reqs', self.gBest.getNumPlacedReqs())
		self.printSolution()
		self.printDBStatus()


	def calcAlpha(self):		
		delta = 1.0 - pow((pow(10.0, -4.0)/0.9), 1.0/ Global.MAX_GENERATIONS)
		return (1 - delta) * Global.ALPHA

	def sortFireflies(self, inlist):
		less = []
		equal = []
		greater = []
		if len(inlist) > 1:
			pivot = inlist[0]
			for x in inlist:
				xIlum = x.getIllumination()
				pivotIlum = pivot.getIllumination()
				
				if xIlum < pivotIlum:
					less.append(x)
				elif xIlum == pivotIlum:
					equal.append(x)
				else :
					greater.append(x)

			return self.sortFireflies(less)  + equal  + self.sortFireflies(greater)
   
		else: 
			return inlist

	def setBests(self):
		if(self.population[self.popSize - 1].getIllumination() > self.bestI):
			self.bestI = self.population[self.popSize - 1].getIllumination()
			self.gBest = copy.deepcopy(self.population[self.popSize - 1])
		self.fitnessList.append(self.population[self.popSize - 1].getIllumination())

	def moveFirefiles(self):
		print('moving fireflies')
		for i in range(0, self.popSize):
			scale = abs(Global.upperBound[i] - Global.lowerBound[i])
			for j in range(0, self.popSize):
				r = 0.0
				for k in range(0, Global.DIMENSION):
					r += self.calcR(i, j, k)
			r = math.sqrt(r)
			if(self.population[j].brighterThan(self.population[i])):
				beta0 = 1.0
				beta = self.calcBeta(beta0, r)
				
				for k in range(0, Global.DIMENSION) :
					r = (random.uniform(0,1) + (1)) 
					tmpf = Global.ALPHA * (r-0.5) * scale
					value = int(math.floor(self.population[i].getByIndex(k) * (1.0 - beta) + self.tempPop[j].getByIndex(k) * beta + tmpf))
					self.population[i].setByIndex(k, value) 
		
			self.findLimits(i)

	def calcR(self, i, j, k):
		ffa1 = self.population[i].getByIndex(k)
		ffa2 = self.population[j].getByIndex(k)
		return ((ffa1 - ffa2) * (ffa1 - ffa2))

	def calcBeta(self, beta0, r):
		return (beta0 - Global.BETAMIN) * math.exp(- Global.GAMMA * pow(r, 2.0)) + Global.BETAMIN
	
	def dumpFirefly(self, gen):
		print("Dump at gen = " +  str(gen) + " best= " + str(self.bestI) + "\n")

	def copyGeneration(self):
			self.tempPop = copy.deepcopy(self.population)
			
	def findLimits(self, k):
		for i in range(0, Global.DIMENSION):
			self.population[k].limitLowerByIndex(i)
			self.population[k].limitUpperByIndex(i)
	
	def printSolution(self):
		solFile = open('solution.txt', 'w')
		solFile.write('num of used DCs'+ str(self.gBest.getNumUsedDCs()) + ' num of placed reqs'+ str(self.gBest.getNumPlacedReqs()) + "\n")
		solFile.write("################")
		for i  in range(0, Global.NUM_OF_REQUESTS):
			solFile.write("request No. " + str(i + 1) + " : " + str(self.gBest.getByIndex(i)) + "\n")

		solFile.write("################")
	
	def printDBStatus(self):
		self.gBest.calcFitness()
		self.gBest.printDBStatus()
	
	def plotLearning(self):	
		plt.plot([i for i in range(len(self.fitnessList))], self.fitnessList)
		plt.ylabel('Fitness')
		plt.xlabel('Iteration')
		plt.savefig('fig.png')
		plt.show()