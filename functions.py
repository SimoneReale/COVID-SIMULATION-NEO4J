from os import close
from pickle import TRUE
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
                """db.run("MATCH (a:Person), (b:Person) "
                        "WHERE a.name = $name1 AND b.name = $name2 "
                        "CREATE (a)<-[r:FAMILY_CONTACT]-(b)"
                        , name1 = list_relatives[i].get("name"), name2 = list_relatives[j].get("name"))"""

    return             






def createPopulation(db, n, progress_bar):
    f1 = open('nomi.txt', 'r')
    f2 = open('cognomi.txt', 'r')

    count_pop = 0
    progress_bar.pack(pady=40)
    progress_bar['value'] = 0

    for i in range(n):
        
        if (count_pop > n):
            break
        
        family_list = []
        family_surname = f2.readline().strip('\n')
        pater_familias = {}
        pater_familias["name"] = f1.readline().strip('\n')
        pater_familias["surname"] = family_surname
        pater_familias["age"] = randint(0, 100)
        family_list.append(pater_familias)

        db.run("CREATE (a:Person) "
                        "SET a.name = $name "
                        "SET a.surname = $surname "
                        "SET a.age = $age"
                        , name = pater_familias.get("name"), surname = family_surname ,age = pater_familias.get("age"))

        count_pop += 1
        progress_bar['value'] += 100 / n
        

        for j in range(randint(0,10)):
            parente = {}
            parente["name"] = f1.readline().strip('\n')
            parente["age"] = randint(0, 100)
            parente["surname"] = f2.readline().strip('\n')
            family_list.append(parente)
            
            db.run("CREATE (a:Person) "
                        "SET a.name = $name "
                        "SET a.surname = $surname "
                        "SET a.age = $age"
                        , name = parente.get("name"), surname = family_surname, age = parente.get("age"))

            count_pop += 1
            progress_bar['value'] += 100 / n

            if (count_pop > n):
                break

        

        createFamily(db, family_list)
        
        
    progress_bar.pack_forget()

    f1.close()
    return


def deletePopulation(db):
    db.run("MATCH (n) Detach Delete n")
    return