from dataclasses import dataclass
from random import randint, random
from tkinter.ttk import Progressbar
from py2neo import Graph, NodeMatcher
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

    random_number_of_days = rm.randrange(conf.days_between_dates)
    random_date = conf.start_date + datetime.timedelta(days=random_number_of_days)

    return str(random_date)

def returnListOfDates():
    
    dates = []

    for i in range(0, conf.days_between_dates + 1):
        dates.append(conf.start_date + datetime.timedelta(days=i))

    return dates


#date trattata come stringa nel database
def infectSinglePerson(db, name_infected, date_of_infection):

    db.run("MATCH (n : Person) "
                        "WHERE n.p01_name = $name "
                        "SET n:Infected "
                        "SET n.p06_infectionDate = $date"
                        , name = name_infected,  date = str(date_of_infection))
    return

def createDataset(db, n, progress_bar, progress_bar_label, infect_or_not):

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
        p = int(n / int(conf.proportion_n_of_people_n_of_place))

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

        for i in range(0, int(n / int(conf.proportion_n_of_relationship_n_of_people))):
            db.run("MATCH (a:Person), (b:Person) "
                            "WHERE b.p01_name = $randomname1 AND a.p01_name = $randomname2 AND b.p02_surname <> a.p02_surname "
                            "CREATE (a)-[r:MEETS {date: $random}]->(b)"
                            , randomname1 = list_names[randint(0, n)].strip('\n'), randomname2 = list_names[randint(0, n)].strip('\n'), random = returnRandomDate())

            progress_bar['value'] += 100 / (n / int(conf.proportion_n_of_relationship_n_of_people))


        return


    def infectPeople():

        f_names = open('txts\\namesRight.txt', 'r')
        list_names = f_names.readlines()

        progress_bar['value'] = 0
        progress_bar_label.configure(text="Infecting people...")

        for i in range(0, int(n / conf.proportion_n_of_people_n_of_infected)):

           progress_bar['value'] += 100 / int(n / conf.proportion_n_of_people_n_of_infected)

           name_infected = list_names[randint(0, n - 1)].strip('\n')
           matcher = NodeMatcher(db)
           person_infected = matcher.match("Person", p01_name = name_infected).first()

           #probability with 0 vaccines = 0,7 with one 0,5
           probability_of_contagion = 0.7 if person_infected["p05_number_of_doses"] == 0 else conf.probability_of_infection_with_vaccine ** person_infected["p05_number_of_doses"]

           if (random() < probability_of_contagion):
                db.run("MATCH (n : Person) "
                        "WHERE n.p01_name = $name "
                        "SET n:Infected "
                        "SET n.p06_infectionDate = $date"
                        , name = name_infected, date = str(returnRandomDate()))



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

    if(infect_or_not == 1):
        infectPeople()



    progress_bar.pack_forget()
    progress_bar_label.pack_forget()

    f_names.close()
    f_surnames.close()
    return


def deleteDataset(db):
    db.run("MATCH (n) Detach Delete n")
    return



def createDictionaryNumberOfInfectedPerDay(db):

    dictionary = {}

    var2 = db.run('match (x:Infected) return x.p06_infectionDate, count(*)').to_table()

    for index, tupla in enumerate(var2):
        dictionary[tupla[0]] = tupla[1]

    dictionary = dict(sorted(dictionary.items()))

    return dictionary

def getInfectedPerVaccineType(db):

    dictionary = {}

    var = db.run('match (x:Infected) return x.p04_vaccine, count(*)').to_table()

    for index, tupla in enumerate(var):
        dictionary[tupla[0]] = tupla[1]

    """
    dictionary[str("no vaccine")] = db.run('match (x:Infected {p04_vaccine : $vaccine}) return count(*)', vaccine = "no vaccine").evaluate()

    for i in range(0, len(conf.vaccines)):
        dictionary[str(conf.vaccines[i])] = db.run('match (x:Infected {p04_vaccine : $vaccine}) return count(*)', vaccine = str(conf.vaccines[i])).evaluate()
    """

    return dictionary

def getNumberOfVaccinatedPerVaccine(db):
    dictionary = {}

    var = db.run('match (x) return x.p04_vaccine, count(*)').to_table()

    for index, tupla in enumerate(var):
        if tupla[0] != "no vaccine" and tupla[0] is not None:
            dictionary[tupla[0]] = tupla[1]

    return dictionary

def getMostEffectiveVaccine(infectedPerVaccine, vaccinatedPerVaccine):
    lowestRatio = 1.01
    bestVaccine = None
    ratio = 0

    for key, value in infectedPerVaccine.items():
        if (key != "no vaccine"):
            ratio = value / vaccinatedPerVaccine[key]
            if ratio < lowestRatio:
                lowestRatio = ratio
                bestVaccine = key

    return bestVaccine, lowestRatio


def simulatePandemic(db, n, progress_bar, progress_bar_label, initial_number_of_infected):
    deleteDataset(db)
    #no person infected at beginning
    createDataset(db, n, progress_bar, progress_bar_label, 0)
    
    db.run( "MATCH (n : Person) "
            "WHERE n.p05_number_of_doses = 0 "
            "WITH n , rand() as r " 
            "ORDER BY r "
            "LIMIT $initial_number "
            "SET n : Infected "
            "SET n.p06_infectionDate = $date", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_no_vax)
            , date = str(conf.start_date))

    db.run( "MATCH (n : Person) "
            "WHERE n.p05_number_of_doses = 1 "
            "WITH n , rand() as r " 
            "ORDER BY r "
            "LIMIT $initial_number "
            "SET n : Infected "
            "SET n.p06_infectionDate = $date", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_1_vax)
            , date = str(conf.start_date))

    db.run( "MATCH (n : Person) "
            "WHERE n.p05_number_of_doses = 2 "
            "WITH n , rand() as r " 
            "ORDER BY r "
            "LIMIT $initial_number "
            "SET n : Infected "
            "SET n.p06_infectionDate = $date", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_2_vax)
            , date = str(conf.start_date))

    db.run( "MATCH (n : Person) "
            "WHERE n.p05_number_of_doses = 3 "
            "WITH n , rand() as r " 
            "ORDER BY r "
            "LIMIT $initial_number "
            "SET n : Infected "
            "SET n.p06_infectionDate = $date", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_3_vax)
            , date = str(conf.start_date))
    
    db.run( "MATCH (n : Person) "
            "WHERE n.p05_number_of_doses = 4 "
            "WITH n , rand() as r " 
            "ORDER BY r "
            "LIMIT $initial_number "
            "SET n : Infected "
            "SET n.p06_infectionDate = $date", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_4_vax)
            , date = str(conf.start_date))

    
    
    current_list_of_dates = []
    progress_bar_label.configure(text="Simulating...", pady = 20)
    progress_bar_label.pack()
    progress_bar.pack()
    progress_bar['value'] = 0
        
    
    for i in range(0, conf.days_between_dates):

        progress_bar['value'] += 100 / conf.days_between_dates

        date = conf.start_date + datetime.timedelta(days=i)
        
        current_list_of_dates.append(str(date))

        df = db.run('match (n : Infected) return n.p01_name, n.p06_infectionDate').data()

        list = [d['n.p01_name'] for d in df]

        for person_name in list:
            df_family = db.run('MATCH (n:Infected {p01_name : $name})-[f : FAMILY_CONTACT]-(b:Person) WHERE not b : Infected RETURN b.p01_name, b.p05_number_of_doses', name = person_name).data()
            for curr_date in current_list_of_dates:
                df_meets = db.run('MATCH (n:Infected {p01_name : $name})-[f : MEETS]-(b:Person) WHERE not b : Infected and f.date = $date RETURN b.p01_name, b.p05_number_of_doses', name = person_name, date = curr_date).data()
            

            for p in df_family:
                probability_of_contagion = 0.35 if p["b.p05_number_of_doses"] == 0 else (conf.probability_of_infection_with_vaccine ** p["b.p05_number_of_doses"]) ** 3
                if(probability_of_contagion > random()):
                    infectSinglePerson(db, p["b.p01_name"], str(date))

            for z in df_meets:
                probability_of_contagion = 0.35 if z["b.p05_number_of_doses"] == 0 else (conf.probability_of_infection_with_vaccine ** z["b.p05_number_of_doses"]) ** 3
                if(probability_of_contagion > random()):
                    infectSinglePerson(db, z["b.p01_name"], str(date))
                

    
    
       



    progress_bar.pack_forget()
    progress_bar_label.pack_forget()