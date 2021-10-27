from os import close
from random import randint
from py2neo import Graph
import conf




def createFamily(db, list_relatives):
    
    for i in range(0, len(list_relatives)):
        for j in range(i+1, len(list_relatives)):
            if (7 < randint(0, 10)):
                db.run("MATCH (a:Person), (b:Person) "
                        "WHERE a.name = $name1 AND b.name = $name2 "
                        "CREATE (a)-[r:FAMILY_CONTACT]->(b)"
                        , name1 = list_relatives[i].get("name"), name2 = list_relatives[j].get("name"))
                
                #relazione inversa
                db.run("MATCH (a:Person), (b:Person) "
                        "WHERE a.name = $name1 AND b.name = $name2 "
                        "CREATE (a)<-[r:FAMILY_CONTACT]-(b)"
                        , name1 = list_relatives[i].get("name"), name2 = list_relatives[j].get("name"))

    return             






def createPopulation(db, n):
    f = open('nomi_italiani.txt', 'r')

    for i in range(n):
        
        family_list = []
        pater_familias = {}
        pater_familias["name"] = f.readline().strip('\n')
        pater_familias["age"] = randint(0, 100)
        family_list.append(pater_familias)

        db.run("CREATE (a:Person) "
                        "SET a.name = $name "
                        "SET a.age = $age"
                        , name = pater_familias.get("name"), age = pater_familias.get("age"))

        for j in range(randint(0,6)):
            parente = {}
            parente["name"] = f.readline().strip('\n')
            parente["age"] = randint(0, 100)
            family_list.append(parente)
            
            db.run("CREATE (a:Person) "
                        "SET a.name = $name "
                        "SET a.age = $age"
                        , name = parente.get("name"), age = parente.get("age"))


        createFamily(db, family_list)

    f.close()
    return


if __name__ == "__main__":
    #database connection
    graph = Graph("bolt://localhost:7687", auth=(conf.username, conf.password))
    createPopulation(graph, conf.pop_num)


    