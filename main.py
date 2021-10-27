from os import close
from random import randint
from neo4j import GraphDatabase

class Neo4jInstance:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_dataset(self, n):
        with self.driver.session() as session:
            list_of_people = createPopulation(n)
            session.write_transaction(self._create_nodes, list_of_people)
            

    @staticmethod
    def _create_nodes(tx, list):

        for i in range(len(list)):

            tx.run("CREATE (a:Person) "
                        "SET a.name = $name "
                        "SET a.age = $age"
                        , name = list[i].get("name"), age = list[i].get("age"))

        return





def createPerson():
    f = open('nomi_italiani.txt','r')
    persona = {}
    persona["name"] = f.readline().strip('\n')
    persona["age"] = randint(0, 100)
    f.close()
    return persona




def createPopulation(n):
    
    list_people =[]

    for i in range(n):
        persona = createPerson()

        for j in range(randint(0,6)):
            parente = createPerson()
            list_people.append(parente)


        list_people.append(persona)

    return list_people






if __name__ == "__main__":
    
    dbNeo = Neo4jInstance("bolt://localhost:7687", "neo4j", "sr")
    dbNeo.create_dataset(10)
    dbNeo.close()
    