from __future__ import division
from operator import attrgetter
import matplotlib.pyplot as plt
import copy
import random
import math

import Honey
import Global

class ArtificialBeeColony :
	def __init__(self, MAX_LENGTH, numOfBees, numOfFoods, limit, maxIters):
		self.MAX_LENGTH = MAX_LENGTH 		# number of paramaters to be optimized
		self.numOfBees = numOfBees      # total number of bees(colony size) : employed + onlookers
		self.numOfFoods = numOfFoods 	# The number of food sources equals the half of the colony size
		self.limit = limit              #A food source which could not be improved through "limit" trials is abandoned by its employed bee			
		self.maxIters = maxIters	
		self.foodSources = []
		self.solutions = []
		self.bestScore = 0
		self.fitnessList = []
		self.outfile = open('solutions.txt', 'a')
		gBest = None
	
	def initialize(self):
		newFoodIndex = 0
		shuffles = 0
		
		for i in range(0, self.numOfFoods):
			newHoney = Honey.Honey(self.MAX_LENGTH)
			self.foodSources.append(newHoney);
			newFoodIndex = self.foodSources.index(newHoney)
			shuffles = random.randint(Global.MIN_SHUFFLE, Global.MAX_SHUFFLE)
			
			for j in range(0, shuffles):
				self.randomlyArrange(newFoodIndex)
			
			self.foodSources[newFoodIndex].computeScore()
			self.foodSources[newFoodIndex].reinitDB()
	
	def evolve(self):
		done = False
		numIters = 0

		self.initialize();
		self.memorizeBestFoodSource()

		while(done is False):
			if(numIters < self.maxIters): 		
				self.sendEmployedBees()
				self.getFitness()
				self.calculateProbabilities()
				self.sendOnlookerBees()
				self.memorizeBestFoodSource()
				self.sendScoutBees()
				
				numIters += 1
				print("Iteration: " + str(numIters))
			else:
				done = True

		print("done")
		print("Completed " + str(numIters) + " epochs.")
		self.printSolution(self.gBest)
		self.gBest.printDatabaseStatus()

	def sendEmployedBees(self):
		neighborBeeIndex = 0
		currentBee = None
		neighborBee = None
		
		for i in range(0, self.numOfFoods):
			#A randomly chosen solution is used in producing a mutant solution of the solution i
			neighborBeeIndex = self.getExclusiveRandomNumber(self.numOfFoods - 1, i)
			currentBee = self.foodSources[i]
			neighborBee = self.foodSources[neighborBeeIndex]
			self.sendToWork(currentBee, neighborBee)
		
	def getExclusiveRandomNumber(self, high, exc):
		done = False
		getRand = 0
		while(done is False):
			getRand = random.randint(0, high)
			if(getRand != exc):
				done = True

		return getRand  
	
	def sendOnlookerBees(self):
		i = 0
		t = 0
		neighborBeeIndex = 0
		while(t < self.numOfFoods):
			currentBee = self.foodSources[i]
			if(random.uniform(0, 1) < currentBee.getSelectionProbability()):
				t += 1
				neighborBeeIndex = self.getExclusiveRandomNumber(self.numOfFoods-1, i)
				neighborBee = self.foodSources[neighborBeeIndex]
				self.sendToWork(currentBee, neighborBee)

			i += 1
			if(i == self.numOfFoods):
				i = 0
  
	def sendScoutBees(self):
		shuffles = 0
		for i in range(0, self.numOfFoods):
			currentBee = self.foodSources[i]
			if(currentBee.getTrials >= self.limit):
				#shuffles = self.getRandomNumber(Global.MIN_SHUFFLE, Global.MAX_SHUFFLE)
				currentBee.initNectar()

				#for j in range(0, shuffles) : 
					#self.randomlyArrange(i)

	def sendToWork(self, currentBee, neighborBee):
		newValue = 0
		tempValue = 0
		tempIndex = 0
		prevScore = 0
		currScore = 0
		parameterToChange = 0

		prevScore = currentBee.getScore()
		parameterToChange = random.randint(0, self.MAX_LENGTH - 1)

		tempValue = currentBee.getNectar(parameterToChange)
		newValue = int((tempValue + (tempValue - neighborBee.getNectar(parameterToChange))*(random.uniform(0, 1)-0.5)*2))
		newValue = self.trap(newValue)
		#tempIndex = currentBee.getIndex(newValue)
		currentBee.setNectar(parameterToChange, newValue)
		#currentBee.setNectar(tempIndex, tempValue)
		currentBee.computeScore()
		currentBee.reinitDB()
		currScore = currentBee.getScore()

		if(prevScore < currScore):				
			currentBee.setNectar(parameterToChange, tempValue)
			currentBee.setNectar(tempIndex, newValue)
			currentBee.computeScore()
			currentBee.reinitDB()
			#currentBee.setTrials(currentBee.getTrials() + 1)
			currentBee.setTrials(0)
		else:											
			#currentBee.setTrials(0)
			currentBee.setTrials(currentBee.getTrials() + 1)

	def trap(self, newValue):
		if(newValue < 1):
			newValue = 1

		if(newValue > Global.NUM_OF_NODES): 
			newValue = Global.NUM_OF_NODES
		
		return newValue

	def randomlyArrange(self, index):
		positionA = self.getRandomNumber(0, self.MAX_LENGTH - 1);
		positionB = self.getExclusiveRandomNumber(self.MAX_LENGTH - 1, positionA);
		thisHoney = self.foodSources[index]
		temp = thisHoney.getNectar(positionA)
		thisHoney.setNectar(positionA, thisHoney.getNectar(positionB))
		thisHoney.setNectar(positionB, temp) 

	def memorizeBestFoodSource(self):
		bestSol = max(self.foodSources, key = attrgetter('score'))
		best = max(food.getScore() for food in self.foodSources)

		if(best > self.bestScore):
			self.bestScore = best
			self.gBest = copy.deepcopy(bestSol)

		self.fitnessList.append(best)

	def printSolution(self, honey):
		for i in range(0, self.MAX_LENGTH):
			self.outfile.write(str(i + 1) + " : " + str(honey.getNectar(i)) + '\n')
		self.outfile.write('###########################\n')

	def getFitness(self) :
		thisFood = None
		bestScore = 0.0
		worstScore = 0.0

		##The worst score would be the one with the highest energy, best would be lowest.
		worstScore = self.findWorstScore()
		bestScore = self.findBestScore()
		difference = bestScore - worstScore + 1

		for i in range(0, self.numOfFoods):
			thisFood = self.foodSources[i]
			thisFood.setFitness(((thisFood.getScore() - worstScore) * 100.0 / difference) + 0.01)
	
	def findWorstScore(self):
		score = min( food.getScore() for food in self.foodSources)
		return score
	
	def findBestScore(self):
		score = max( food.getScore()  for food in self.foodSources)
		return score

	def calculateProbabilities(self):
		thisFood = None;
		maxfit = self.foodSources[0].getFitness()
		for i in range(1, self.numOfFoods):
			thisFood = self.foodSources[i]
			if(thisFood.getFitness() > maxfit):
				maxfit = thisFood.getFitness()
		
		for j in range(0, self.numOfFoods):
			thisFood = self.foodSources[j]
			thisFood.setSelectionProbability((0.9 * (thisFood.getFitness() / maxfit)) + 0.1)
	
	def getRandomNumber(self, low, high):
		return int(round((high - low) * random.uniform(0, 1) + low, 0))

	def plotLearning(self):	
		plt.plot([i for i in range(len(self.fitnessList))], self.fitnessList)
		plt.ylabel('Score')
		plt.xlabel('Iteration')
		plt.savefig('fig.png')
		plt.show()
		
