import Population
import customeDatabase
import Global

def main():
    customeDatabase.generateDBFile()
    pop = Population.Population(Global.MAX_POP, Global.MUTATION_RATE, Global.PERFECT_SCORE)
    pop.evolve()
    
if __name__ == "__main__":
    main()