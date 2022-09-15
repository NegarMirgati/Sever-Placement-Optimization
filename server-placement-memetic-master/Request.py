import random
import Global

class Request:
    def __init__(self, _id, cpu, mem):
        self.id = _id
        self.cpu = cpu
        self.mem = mem
        self.node = -1

    def printStatus(self):
        f = open("requests.txt", "a")
        f.write("Request ID = " + str(self.id) +" ")
        f.write("CPU = " + str(self.cpu)  + " ")
        f.write("MEM = " + str(self.mem)  + "\n")
        f.write("***\n")
    
    def getCPUAndMem(self) :
        return (self.cpu, self.mem)

def createRequests(numOfRequests):
    reqList = []
    for i in range(0, numOfRequests):
        request = Request(i+1, random.randint(1, Global.MAX_CPU), random.randint(1, Global.MAX_MEM))
        request.printStatus()
        reqList.append(request)
    return reqList

requests = createRequests(Global.NUM_OF_REQUESTS)