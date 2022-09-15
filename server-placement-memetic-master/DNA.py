import random
import customeDatabase
import math
import random
import Request
import Global

class DNA :
    def __init__(self, genesSize):
        self.genes = [-1] * genesSize
        self.fitness = 0
        self.Database = customeDatabase.customeDatabase()
        self.initSolutionAndUpdateRequestAndDB()
 
    def initSolutionAndUpdateRequestAndDB(self):
        genesSize = len(self.genes)
        for i in range(0, genesSize):
            randomNode = self.Database.getRandomNode()
            (cpu, mem) = Request.requests[i].getCPUAndMem()

            if(self.Database.canPlaceReqOnNode(randomNode, cpu, mem)):
                self.genes[i] = randomNode
                self.Database.updateNodeTable(randomNode, cpu, mem)
            else:
                self.genes[i] = -1

    def crossover(self, partner):
        genesSize = len(self.genes)
        child = DNA(genesSize)
        midpoint = math.floor(random.randint(0, genesSize)) 
        for i in range(0, genesSize):
            if (i > midpoint) : 
                targetNodeID = self.genes[i]
                child.replaceCurrentReqWith(i, targetNodeID)
            else :
                targetNodeID = partner.genes[i]
                child.replaceCurrentReqWith(i, targetNodeID)
    
        return child

    def mutate(self, mutationRate):
        genesSize = len(self.genes)
        for i in range(0, genesSize):
            prob = random.uniform(0, 1)
            if(prob < mutationRate):
                randomNode = self.Database.getRandomNode()
                self.replaceCurrentReqWith(i, randomNode)
                
    def getFitness(self) :
        return (self.fitness)

    def calcFitness(self) :
        self.fitness = 0
        genesSize = len(self.genes)
        for i in range(0, genesSize):
            self.fitness += self.calcGeneFitness(i)
        self.fitness = pow(self.fitness, 4)
        
    def calcGeneFitness(self, geneNumber):
        node = self.genes[geneNumber]
        if(node != -1):
            return 1
        return 0

    def hillClimb(self):
        numOfGenes = len(self.genes)
        numIters = 0
        while(numIters != Global.MAX_HILL_CLIMB_ITERS):
        #while(True):
            numOfImprovements = 0
            randomIndexes = random.sample(range(numOfGenes), numOfGenes)
            for i in range(0, numOfGenes):
                index = randomIndexes[i]
                if(self.couldImprove(index)):
                    numOfImprovements += 1
        
            if(numOfImprovements == 0):
                break
        numIters += 1

    def couldImprove(self, geneIndex):
        betterNodeID = self.findBetterNode(geneIndex)
        if(betterNodeID == -1 ):
            return False
        else:
            self.replaceCurrentReqWith(geneIndex, betterNodeID)
            return True
        
    def findBetterNode(self, geneIndex):
        correspondingReq = Request.requests[geneIndex]
        (cpu, mem) = correspondingReq.getCPUAndMem()
        currentNode = self.genes[geneIndex]
        (currentNodeCPU, currentNodeMem) = self.Database.getCPUAndMemOfNode(currentNode)
        (possibleNodeIDs, possibleNodes) = self.Database.getPossibleNodes(cpu, mem)
            
        for i in range(0, len(possibleNodes)):
            targetNodeCPU = possibleNodes[i][2]
            targetNodeMem = possibleNodes[i][4]
            targetNodeID = possibleNodeIDs[i]
            if(targetNodeID == currentNode):
                continue
            
            cpuDiff = (currentNodeCPU + cpu) - targetNodeCPU 
            memDiff = (currentNodeMem + mem) - targetNodeMem

            if(currentNode == -1) :
                cpuDiff -= cpu
                memDiff -= mem
    
            if(cpuDiff + memDiff > 0) :
                return targetNodeID
        return -1
            
    def replaceCurrentReqWith(self, geneIndex, targetNodeID):
        if(targetNodeID == -1):
            return
        correspondingReq = Request.requests[geneIndex]
        (cpu, mem) = correspondingReq.getCPUAndMem()
        currentNode = self.genes[geneIndex]

        if(self.Database.canPlaceReqOnNode(targetNodeID, cpu, mem)):
            if(currentNode != (-1)):
                self.Database.updateNodeTable(currentNode, -cpu, -mem)
            
            self.Database.updateNodeTable(targetNodeID, cpu, mem)
            self.genes[geneIndex] = targetNodeID

    def printGenes(self):
        count = 0
        f = open("log.txt", "a")
        f.write("%%%%%%%%%%%%%%%%%%SOLUTION%%%%%%%%%%%%%%%%%\n")
        for i in range(0, len(self.genes)):
            if(self.genes[i] == -1):
                count +=1
            f.write("Request No " + str(i) + " : " + str(self.genes[i]))
            f.write("\n")
        f.write("count" + str(count))

    def printDatabase(self):
        self.Database.printNodeTable()