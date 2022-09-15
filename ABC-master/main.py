import ABC
import Global
import customeDatabase
import Request

def main():
    print('Artificial Bee Colony')
    initDatabase()
    Request.createRequests(Global.NUM_OF_REQUESTS)
    Request.readRequests()
    abc = ABC.ArtificialBeeColony(Global.DIMENSION, Global.POP_SIZE, Global.POP_SIZE/2, Global.LIMIT, Global.MAX_ITERS)
    abc.evolve()
    abc.plotLearning()

def initDatabase():
    customeDatabase.generateDBFile()

if __name__ == main :
    main()

main()