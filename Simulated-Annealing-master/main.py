import Database
import anneal
import Request
import Global

def main():
    print('simulated annealing')
    Database.generateDBFile()
    db = Database.Database("./testdb.db")
    Request.createRequests(Global.NUM_OF_REQUESTS)
    Request.readRequests()
    initDB(db)
    sm = anneal.SimAnneal(db)
    sm.anneal()
    sm.plotLearning()

def initDB(db):
    db.createDataCenterTable()
    db.createNodeTable()
    db.initiateDCTable()
    db.initiateNodeTable()
    db.commit()


if __name__ == main():
    main()

