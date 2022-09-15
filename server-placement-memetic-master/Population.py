from __future__ import division
from DNA import DNA
import random
import math
import Global
import copy

class Population :
    def __init__(self, popSize, _muteRate, _perfectScore):
        self.population = []
        self.tempPop = []
        self.numGenerations = 0
        self.evolutionEnded = False
        self.mutationRate = _muteRate
        self.maxPop = popSize
        self.perfectScore = _perfectScore

        for i in range(0, popSize):
            dna = DNA(Global.NUM_OF_REQUESTS)
            self.population.append(dna)
        
    def evolve(self):
        self.hillClimbAll()
        while(self.evolutionEnded is not True):
            self.calcFitnessAll()
            self.evaluateGeneration()
            if(self.evolutionEnded is True):
                 break
            self.repopulate()
            self.copyNewGeneration()        
    
    def hillClimbAll(self):
        for i in range(0, self.maxPop):
            self.population[i].hillClimb()

    def calcFitnessAll(self):
        for i in range(0, self.maxPop):
            self.population[i].calcFitness()

    def repopulate(self):
        self.tempPop = [None] * self.maxPop
        maxFitness, maxIndex = self.getMaxFitnessAndIndex()
        normalizedMax = self.normalizeFitness(maxFitness)
        for i in range(0, self.maxPop):
            partnerA = self.choosePartner(normalizedMax)
            partnerB = self.choosePartner(normalizedMax)

            child = partnerA.crossover(partnerB)
            child.mutate(self.mutationRate)
            child.hillClimb()
            self.tempPop[i] = child
            
        self.numGenerations += 1

    def printPop(self):
        for i in range(0, self.maxPop):
            self.population[i].printGenes()

    def choosePartner(self, maxFitness):
        while(True):
            index = random.randint(0, self.maxPop - 1)
            partner = self.population[index]
            probability = random.uniform(0, maxFitness)
            partnerFitness = self.normalizeFitness(partner.getFitness())
            if(probability < partnerFitness):
                return partner
        
        return self.population[index]
        
    def getNumGenerations(self):
        return self.numGenerations

    def getMaxFitnessAndIndex(self):
        maxFitness = -1
        maxIndex = -1
        for i in range(0, self.maxPop):
            elemFitness = self.population[i].getFitness()
            if(elemFitness > maxFitness):
                maxFitness = elemFitness
                maxIndex = i
            return maxFitness, maxIndex
    
    def normalizeFitness(self, fitness):
        fitnessSum = 0
        for i in range(0,self.maxPop):
            fitnessSum += self.population[i].getFitness()
        return (fitness/fitnessSum)

    def evaluateGeneration(self):
        maxFitness, maxIndex = self.getMaxFitnessAndIndex() 
        maxFitness = math.sqrt(math.sqrt(maxFitness))
        maxFitness = maxFitness / Global.NUM_OF_REQUESTS
        self.printCurrentStatus(maxFitness)

        if(maxFitness >= self.perfectScore) :
            self.evolutionEnded = True
            self.displayResult(maxIndex)
        else:
            self.evolutionEnded = False

    def displayResult(self, maxIndex):
        self.population[maxIndex].printGenes()
        self.population[maxIndex].printDatabase()

    def printCurrentStatus(self, maxFitness):
        print("# generation : " + str (self.numGenerations))
        print("Average Fitness = " + str(self.getAverageFitness(maxFitness)))
        #print("Best Fitness = " + str(maxFitness))

    def getAverageFitness(self, maxFitness):
        total = 0
        for i in range(0, self.maxPop):
            total += (math.sqrt(math.sqrt((self.population[i].getFitness()))) / Global.NUM_OF_REQUESTS)
        return (total / self.maxPop)

    def copyNewGeneration(self):
         self.population = copy.deepcopy(self.tempPop)