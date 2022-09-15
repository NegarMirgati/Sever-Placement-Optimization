import random
import Global
import sqlite3

class Database():
    def __init__(self, address):
        self.conn = sqlite3.connect(address)
        self.c = self.conn.cursor()
        self.dbAddress = address
    
    def createDataCenterTable(self):
        self.c.execute('PRAGMA foreign_keys = ON')
        self.c.execute('''CREATE TABLE IF NOT EXISTS `DataCenter` (
        `DCID`    INTEGER,
        `TOT_CPU` INTEGER,
        `CPU`    INTEGER,
        `TOT_MEM` INTEGER DEFAULT 0,
        `MEM`    INTEGER,
        PRIMARY KEY(`DCID`)
        );'''
    )

    def  createNodeTable(self):
        self.c.execute('PRAGMA foreign_keys = ON')
        self.c.execute('''CREATE TABLE IF NOT EXISTS `Node` (
         `NodeID`    INTEGER,
        `FDCID`    INTEGER,
        `TOT_CPU` INTEGER DEFAULT 0,
        `CPU`    INTEGER DEFAULT 0,
        `TOT_MEM` INTEGER DEFAULT 0,
        `MEM`    INTEGER DEFAULT 0,
        PRIMARY KEY(`NodeID`)
        FOREIGN KEY (`FDCID`) REFERENCES DataCenter(`DCID`) ON DELETE CASCADE
        );
    ''')

    def initiateDCTable(self): 
        f = open("DCs.txt", "r")
        for line in f:
            splitted = line.split(',')
            dcID = int(splitted[0])
            cpu = int(splitted[1])
            mem = int(splitted[3])
            self.insertIntoDCTable(dcID, cpu, mem)
    
    def insertIntoDCTable(self, rowid, cpu, mem):
        exec_str = "INSERT INTO DataCenter VALUES (" + str(rowid) + ", " + str(cpu) + ", " + str(cpu) + ", " + str(mem) + ", " +str(mem) + ")" 
        self.c.execute(exec_str)

    def initiateNodeTable(self):
        f = open("Nodes.txt", "r")
        for line in f:
            splitted = line.split(',')
            nodeID = int(splitted[0])
            dcID = int(splitted[1])
            cpu = int(splitted[2])
            mem = int(splitted[4])
            self.insertIntoNodeTable(nodeID, dcID, cpu, cpu, mem, mem)

    def insertIntoNodeTable(self, rowid, dcid, tot_cpu, cpu, tot_mem, mem):
        exec_str = "INSERT INTO Node VALUES (" + str(rowid) + ", " +str(dcid) + ", " +str(cpu) + ", " +str(cpu) + ", " + str(mem) + ", " + str(mem)+ ")"  
        self.c.execute(exec_str)
    
    def canPlaceReqOnNode(self, node, cpu, mem):
        for row in self.c.execute("SELECT * FROM Node WHERE NodeID = " + str(node)):
            node_cpu = row[3]
            node_mem = row[5]
            if(node_cpu >= cpu and node_mem >= mem):
                return True
            return False

    def getPossibleNodes(c, CPU, MEM):
        retval = (c.execute("SELECT * FROM Node WHERE CPU >= " + str(CPU) + " AND MEM >= " + str(MEM)))
        return retval


    def updateNodeTable(self, NodeID, CPU, MEM):
        self.c.execute("UPDATE Node SET CPU = CPU - " + str(CPU) + ", MEM = MEM - " + str(MEM) + " WHERE NodeID = " + str(NodeID))

    def getCorrespondingDC(self, NodeID):
        row = self.c.execute("SELECT FDCID FROM Node WHERE NodeID = " + str(NodeID))
        retval = row[0]
        print("Corresponding DCID = " + str(retval))
        return retval

    def updateDCTable(self, DCID, CPU, MEM):
        self.c.execute("UPDATE DataCenter SET CPU = CPU - " + str(CPU) + ", MEM = MEM - " + str(MEM) + " WHERE DCID = " + str(DCID))

    def getCPUAndMemOfNode(self, nodeID):
        retval = (self.c.execute("SELECT CPU, MEM FROM Node WHERE NodeID = " + str(nodeID)))
        for row in retval:
            return row[0], row[1]
  
    def printDCTable(self):
        f = open("DBStat.txt", "a")
        f.write("***********************************Datacenters*******************************\n")
        for row in self.c.execute("SELECT * FROM DataCenter"):
            f.write(str(row))
            f.write("\n")

    def printNodeTable(self):
        f = open("DBStat.txt", "a")
        f.write("***********************************Nodes*******************************\n")
        for row in self.c.execute("SELECT * FROM Node"):
            f.write(str(row))
            f.write("\n")

    def commit(self):
            self.conn.commit()
    
    def renewConnection(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.dbAddress)
        self.c = self.conn.cursor()

    def getCorrespondingDC(self, nodeID):
        retval =  self.c.execute("SELECT FDCID FROM Node WHERE NodeID = " + str(nodeID))
        for row in retval :
            return row[0]

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

