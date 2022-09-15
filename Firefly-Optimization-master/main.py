import Population
import Global
import CustomeDatabase
import Request

def main():
    print("Firefly Optimization")
    #CustomeDatabase.generateDBFile()
    Request.createRequests(Global.NUM_OF_REQUESTS)
    Request.readRequests()
    pop = Population.Population(Global.NUM_OF_FIREFLIES, Global.PERFECT_SCORE)
    pop.initBounds()
    pop.initGeneration()
    pop.initAgents()
    pop.evolve()
    pop.plotLearning()
    
if __name__ == "__main__":
    main()