import random
import Global
import sqlite3

def init (address):
  
  conn = sqlite3.connect(address)
  c = conn.cursor()
  return (conn, c)

def createDataCenterTable(c):
  c.execute('PRAGMA foreign_keys = ON')
  c.execute('''CREATE TABLE IF NOT EXISTS `DataCenter` (
  `DCID`    INTEGER,
  `TOT_CPU` INTEGER,
  `CPU`    INTEGER,
  `TOT_MEM` INTEGER DEFAULT 0,
  `MEM`    INTEGER,
  PRIMARY KEY(`DCID`)
);'''
)

def  createNodeTable(c):
  c.execute('PRAGMA foreign_keys = ON')
  c.execute('''CREATE TABLE IF NOT EXISTS `Node` (
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

def initiateDCTable(c): 
  print("creating " + str(Global.NUM_OF_DCS) + " datacenters")
  for row in range(1, Global.NUM_OF_DCS + 1):
    insertIntoDCTable(c, row)

def insertIntoDCTable(c, rowid):
  exec_str = "INSERT INTO DataCenter VALUES (" + str(rowid) + ", " + "NULL" + ", " + "NULL" + ", " + "NULL" + ", " +"NULL" + ")" 
  c.execute(exec_str)


def initiateNodeTable(c):
  node_table_cntr = 1
  for dc_cnt in range(1, Global.NUM_OF_DCS + 1):
      num_of_nodes = random.randint(1, Global.NUM_OF_NODES)
      cpu = random.randint(1, Global.MAX_CPU * Global.SCALE)
      mem = random.randint(1, Global.MAX_MEM * Global.SCALE)

      total_cpu = cpu * num_of_nodes
      total_mem = mem * num_of_nodes

      for node_cnt in range(1, num_of_nodes + 1):
            insertIntoNodeTable(c, node_table_cntr, dc_cnt, cpu, cpu, mem, mem)
            node_table_cntr += 1
      
      completeDCTable(c, total_cpu, total_mem, dc_cnt)
    
def insertIntoNodeTable(c, rowid, dcid, tot_cpu, cpu, tot_mem, mem):
  exec_str = "INSERT INTO Node VALUES (" + str(rowid) + ", " +str(dcid) + ", " +str(cpu) + ", " +str(cpu) + ", " + str(mem) + ", " + str(mem)+ ")"  
  c.execute(exec_str)

def completeDCTable(c, total_cpu, total_mem, dc_cnt):
  c.execute("UPDATE DataCenter SET TOT_CPU = " + str(total_cpu) + ", CPU = " + str(total_cpu) +
                       ", TOT_MEM =  " + str(total_mem) + ", MEM = " + str(total_mem) + " WHERE DCID = " + str(dc_cnt))
  

def canPlaceReqOnNode(c, node, cpu, mem):
  for row in c.execute("SELECT * FROM Node WHERE NodeID = " + str(node)):
    node_cpu = row[3]
    node_mem = row[5]
    if(node_cpu >= cpu and node_mem >= mem):
      return True
    return False

def getPossibleNodes(c, CPU, MEM):
    retval = (c.execute("SELECT * FROM Node WHERE CPU >= " + str(CPU) + " AND MEM >= " + str(MEM)))
    return retval


def updateNodeTable(c, NodeID, CPU, MEM):
  c.execute("UPDATE Node SET CPU = CPU - " + str(CPU) + ", MEM = MEM - " + str(MEM) + " WHERE NodeID = " + str(NodeID))

def getCorrespondingDC(c, NodeID):
  ans = c.execute("SELECT FDCID FROM Node WHERE NodeID = " + str(NodeID))
  for row in ans:
    return row[0]

def updateDCTable(c, DCID, CPU, MEM):
  c.execute("UPDATE DataCenter SET CPU = CPU - " + str(CPU) + ", MEM = MEM - " + str(MEM) + " WHERE DCID = " + str(DCID))

def getCPUAndMemOfNode(c, nodeID):
  retval = (c.execute("SELECT CPU, MEM FROM Node WHERE NodeID = " + str(nodeID)))
  for row in retval:
    return row[0], row[1]
  
def printDCTable(c):
    for row in c.execute("SELECT * FROM DataCenter"):
      print(row)

def printNodeTable(c):
    for row in c.execute("SELECT * FROM Node"):
     print(row)

def commit(conn):
  conn.commit()

def close(conn):
    conn.close()


def getRandomNode() :
      return random.randint(1, Global.NUM_OF_NODES)

def generateDBFile():
    DCFile = open("DCs.txt","w")
    nodeFile = open("Nodes.txt", "w")
    node_table_cntr = 1
    for i in range(1, Global.NUM_OF_DCS + 1):
        num_of_nodes = random.randint(1, Global.MAX_NUM_OF_NODES)
        cpu = random.randint(1, Global.MAX_CPU * Global.SCALE)
        mem = random.randint(1, Global.MAX_MEM * Global.SCALE) 

        total_cpu = cpu * num_of_nodes
        total_mem = mem * num_of_nodes

        for node_cnt in range(1, num_of_nodes + 1):
            nodeFile.write(str(node_table_cntr) + ", " + str(i) + ", "  + str(cpu) + ", " + str(cpu) + ", " + str(mem) + ", " + str(mem) + "\n") 
            node_table_cntr += 1

        DCFile.write(str(i) + ", " + str(total_cpu) + ", " + str(total_cpu) + ", " + str(total_mem) + ", " + str(total_mem) + "\n")

    Global.NUM_OF_NODES = node_table_cntr - 1    