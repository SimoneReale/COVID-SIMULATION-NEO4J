from dataclasses import dataclass
from pickle import NONE
from random import randint, random
from py2neo import Graph
import conf
import numpy as np
import datetime
import random as rm



@dataclass
class Person :
    
    @staticmethod
    def createPerson(name, surname):
        
        age = abs(int(np.random.normal(45, 30)))

        if(age > 12 and conf.vaccine_probability > random()):
            person = Person(name, surname, age, conf.vaccines[randint(0, len(conf.vaccines) - 1)], randint(1, 4))
            return person

        else:
            person = Person(name, surname, age, "no vaccine", 0)
            return person


    name : str
    surname : str
    age : int
    vaccine : str
    number_of_doses : int




@dataclass
class Place :

    name : str
    type : str
    

def returnRandomDate():
    start_date = conf.start_date
    end_date = conf.end_date

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = rm.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date




def createDataset(db, n, progress_bar, progress_bar_label):

    def createFamily(list_relatives):
        for i in range(0, len(list_relatives)):
            for j in range(i+1, len(list_relatives)):
                if (7 < randint(0, 10)):
                    db.run("MATCH (a:Person), (b:Person) "
                            "WHERE a.p01_name = $name1 AND b.p01_name = $name2 "
                            "CREATE (a)-[r:FAMILY_CONTACT]->(b)"
                            , name1 = list_relatives[i].name, name2 = list_relatives[j].name)
                    
                    #relazione inversa
                    """db.run("MATCH (a:Person), (b:Person) "
                            "WHERE a.p01_name = $name1 AND b.p01_name = $name2 "
                            "CREATE (a)<-[r:FAMILY_CONTACT]-(b)"
                            , name1 = list_relatives[i].get("name"), name2 = list_relatives[j].get("name"))"""

        return     


    def createPlaces():

        #n is the number of people, the number of places
        p = int(n / conf.proportion_n_of_people_n_of_place)

        f_names = open('txts\\namesRight.txt', 'r')
        list_names = f_names.readlines()
        
        progress_bar['value'] = 0
        progress_bar_label.config(text = "Creating places and relationships places-people...")

        for i in range(p):
            
            choice = randint(1,3)

            if(choice == 1):
                db.run("CREATE (a:Place) "
                        "SET a.p01_name = $name "
                        "SET a.p02_type = $type", name = "Restaurant " +str(i), type = conf.type_of_places[0]
                            )

                for j in range(0, abs(int(np.random.normal(p, 10)))):
                    db.run("MATCH (a:Person), (b:Place) "
                            "WHERE b.p01_name = $name2 AND a.p01_name = $randomname "
                            "CREATE (a)-[r:VISITS {date: $random}]->(b)"
                            , name2 = "Restaurant " +str(i), randomname = list_names[randint(0, n)].strip('\n'), random = returnRandomDate())


            if(choice == 2):
                db.run("CREATE (a:Place) "
                        "SET a.p01_name = $name "
                        "SET a.p02_type = $type", name = "Hospital " +str(i), type = conf.type_of_places[1]
                            )
                for j in range(0, abs(int(np.random.normal(p, 10)))):
                    db.run("MATCH (a:Person), (b:Place) "
                            "WHERE b.p01_name = $name2 AND a.p01_name = $randomname "
                            "CREATE (a)-[r:VISITS {date: $random}]->(b)"
                            , name2 = "Hospital " +str(i) , randomname = list_names[randint(0, n)].strip('\n'), random = returnRandomDate())

            if(choice == 3):
                db.run("CREATE (a:Place) "
                        "SET a.p01_name = $name "
                        "SET a.p02_type = $type", name = "Theatre " +str(i), type = conf.type_of_places[2]
                            )
                for j in range(0, abs(int(np.random.normal(p, 10)))):
                    db.run("MATCH (a:Person), (b:Place) "
                            "WHERE b.p01_name = $name2 AND a.p01_name = $randomname "
                            "CREATE (a)-[r:VISITS {date: $random}]->(b)"
                            , name2 = "Theatre " +str(i),  randomname = list_names[randint(0, n)].strip('\n'), random = returnRandomDate())


            progress_bar['value'] += 100 / p

        return


    def createMeetRelations():

        progress_bar['value'] = 0
        progress_bar_label.config(text = "Creating 'Meets' relationships...")

        f_names = open('txts\\namesRight.txt', 'r')
        list_names = f_names.readlines()

        for i in range(0, int(n / conf.proportion_n_of_relationship_n_of_people)):
            db.run("MATCH (a:Person), (b:Person) "
                            "WHERE b.p01_name = $randomname1 AND a.p01_name = $randomname2 AND b.p02_surname <> a.p02_surname "
                            "CREATE (a)-[r:MEETS {date: $random}]->(b)"
                            , randomname1 = list_names[randint(0, n)].strip('\n'), randomname2 = list_names[randint(0, n)].strip('\n'), random = returnRandomDate())
            
            progress_bar['value'] += 100 / (n / conf.proportion_n_of_relationship_n_of_people)


        return




    
    f_names = open('txts\\namesRight.txt', 'r')
    f_surnames = open('txts\\surnamesRight.txt', 'r')

    count_pop = 0
    progress_bar_label.pack()
    progress_bar_label.configure(text="Creating people and family relationships...")
    progress_bar.pack(pady=5)
    progress_bar['value'] = 0

    for i in range(n):
        
        if (count_pop > n):
            break
        
        family_list = []
        family_surname = f_surnames.readline().strip('\n')


        pater_familias = Person.createPerson(f_names.readline().strip('\n'), family_surname)

        family_list.append(pater_familias)

        db.run("CREATE (a:Person) "
                        "SET a.p01_name = $name "
                        "SET a.p02_surname = $surname "
                        "SET a.p03_age = $age "
                        "SET a.p04_vaccine = $vaccine "
                        "SET a.p05_number_of_doses = $number_of_doses"
                        , name = pater_familias.name, surname = family_surname, age = pater_familias.age, vaccine = pater_familias.vaccine, number_of_doses = pater_familias.number_of_doses)
                        
                        

        count_pop += 1
        progress_bar['value'] += 100 / n
        

        for j in range(randint(0,10)):
            
            parente = Person.createPerson(f_names.readline().strip('\n'), family_surname)
            family_list.append(parente)
            
            db.run("CREATE (a:Person) "
                        "SET a.p01_name = $name "
                        "SET a.p02_surname = $surname "
                        "SET a.p03_age = $age "
                        "SET a.p04_vaccine = $vaccine "
                        "SET a.p05_number_of_doses = $number_of_doses"
                        , name = parente.name, surname = family_surname, age = parente.age, vaccine = parente.vaccine, number_of_doses = parente.number_of_doses)

            count_pop += 1
            progress_bar['value'] += 100 / n

            if (count_pop > n):
                break

        

        createFamily(family_list)



    createPlaces()
    createMeetRelations()
        
        
    progress_bar.pack_forget()
    progress_bar_label.pack_forget()

    f_names.close()
    f_surnames.close()
    return


def deletePopulation(db):
    db.run("MATCH (n) Detach Delete n")
    return