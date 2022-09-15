import random
import Global

class Request:
    def __init__(self, _id, cpu, mem):
        self.id = _id
        self.cpu = cpu
        self.mem = mem
        self.node = -1

    def printStatus(self, fp):
        fp.write(str(self.id))
        fp.write(", " + str(self.cpu))
        fp.write(", " + str(self.mem)  + "\n")
    
    def getCPUAndMem(self) :
        return (self.cpu, self.mem)

def createRequests(numOfRequests):
    fp = open("requests.txt", "w")
    for i in range(0, numOfRequests):
        request = Request(i+1, random.randint(1, Global.MAX_CPU), random.randint(1, Global.MAX_MEM))
        request.printStatus(fp)

def readRequests():
    reqList = []
    fp = open("requests.txt", "r")
    for line in fp :
        splitted = line.split(',')
        id = int(splitted[0])
        cpu = int(splitted[1])
        mem = int(splitted[2])
        print(id,cpu,mem)
        request = Request(id, cpu, mem)
        reqList.append(request)
    global requests   
    requests = reqList