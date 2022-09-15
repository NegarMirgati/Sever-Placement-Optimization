import random
import Global

class customeDatabase():
    def __init__(self):
        self.DCTable = [[0 for x in range(4)] for y in range(Global.NUM_OF_DCS)] 
        self.nodeTable = [[0 for x in range(5)] for y in range(Global.NUM_OF_NODES)] 
        self.initiateDCTable()
        self.initiateNodeTable()

    def initiateNodeTable(self):
        f = open("Nodes.txt", "r")
        for line in f:
            splitted = line.split(',')
            nodeID = int(splitted[0])
            dcID = int(splitted[1])
            cpu = int(splitted[2])
            mem = int(splitted[4])
            self.insertIntoNodeTable(nodeID, dcID, cpu, mem)
    
    def initiateDCTable(self):
        f = open("DCs.txt", "r")
        for line in f:
            splitted = line.split(',')
            dcID = int(splitted[0])
            cpu = int(splitted[1])
            mem = int(splitted[3])
            self.insertIntoDCTable(dcID, cpu, mem)

    def insertIntoNodeTable(self, rowid, dcid, cpu, mem):
        self.nodeTable[rowid - 1][0] = dcid
        self.nodeTable[rowid - 1][1] = cpu
        self.nodeTable[rowid - 1][2] = cpu
        self.nodeTable[rowid - 1][3] = mem
        self.nodeTable[rowid - 1][4] = mem

    def insertIntoDCTable(self, dcid, cpu, mem):
        self.DCTable[dcid - 1][0] = cpu
        self.DCTable[dcid - 1][1] = cpu
        self.DCTable[dcid - 1][2] = mem
        self.DCTable[dcid - 1][3] = mem
        
    def canPlaceReqOnNode(self, node, cpu, mem):
        node_cpu = self.nodeTable[node - 1][2]
        node_mem = self.nodeTable[node - 1][4]
        if(node_cpu >= cpu and node_mem >= mem):
            return True
        return False

    def getPossibleNodes(self, CPU, MEM):
        rows = []
        ids = []
        for i in range(0, Global.NUM_OF_NODES):
            nodecpu = self.nodeTable[i][2]
            nodemem = self.nodeTable[i][4]
            if((nodecpu >= CPU) and (nodemem >= MEM)):
                rows.append(self.nodeTable[i])
                ids.append(i + 1)
        return ids, rows

    def updateNodeTable(self, NodeID, CPU, MEM):
        self.nodeTable[NodeID - 1][2] -= CPU
        self.nodeTable[NodeID - 1][4] -= MEM

    def getCorrespondingDC(self, NodeID):
        return self.nodeTable[NodeID - 1][0]

    def updateDCTable(self, DCID, CPU, MEM):
        self.DCTable[DCID - 1][1] -= CPU
        self.DCTable[DCID - 1][3] -= MEM

    def getCPUAndMemOfNode(self,nodeID):
        return (self.nodeTable[nodeID - 1][2], self.nodeTable[nodeID - 1][4])


    def printDCTable(self):
        f = open("log.txt", "a")
        f.write("***********************************NODE*******************************\n")
        for i in range(0, len(self.DCTable)):
            f.write("row " + str(i+1) + " ")
            f.write(self.DCTable[i])
            f.write("\n")

    def printNodeTable(self):
        f = open("log.txt", "a")
        f.write("***********************************DataCenter*******************************\n")
        for row in self.nodeTable :
            #f.write("row " + str(i+1) + " ")
            f.write("%s\n" % row)
            f.write("\n")

    def getRandomNode(self) :
        return random.randint(1, Global.NUM_OF_NODES)

def generateDBFile():
    DCFile = open("DCs.txt","w")
    nodeFile = open("Nodes.txt", "w")
    node_table_cntr = 1
    for i in range(1, Global.NUM_OF_DCS + 1):
        num_of_nodes = random.randint(1, Global.MAX_NUM_OF_NDOES)
        cpu = random.randint(1, Global.MAX_CPU * Global.SCALE)
        mem = random.randint(1, Global.MAX_MEM * Global.SCALE) 

        total_cpu = cpu * num_of_nodes
        total_mem = mem * num_of_nodes

        for node_cnt in range(1, num_of_nodes + 1):
            nodeFile.write(str(node_table_cntr) + ", " + str(i) + ", "  + str(cpu) + ", " + str(cpu) + ", " + str(mem) + ", " + str(mem) + "\n") 
            node_table_cntr += 1

        DCFile.write(str(i) + ", " + str(total_cpu) + ", " + str(total_cpu) + ", " + str(total_mem) + ", " + str(total_mem) + "\n")

    Global.NUM_OF_NODES = node_table_cntr - 1    