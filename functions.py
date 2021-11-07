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

    return random_date



def infectSinglePerson(db, name_infected, date_of_infection, *args, **kwargs):

    if(kwargs.get('place', None) != None):
        db.run("MATCH (n : Person) "
                        "WHERE n.p01_name = $name "
                        "SET n:Infected "
                        "SET n.p06_infectionDate = date($date) "
                        "SET n.p07_infectionPlace = $place"
                        , name = name_infected,  date = date_of_infection, place = kwargs.get('place'))

    else:
        db.run("MATCH (n : Person) "
                        "WHERE n.p01_name = $name "
                        "SET n:Infected "
                        "SET n.p06_infectionDate = date($date)"
                        , name = name_infected,  date = date_of_infection)


    
    return

def createDataset(db, n, progress_bar, progress_bar_label, infect_or_not):

    def createFamily():
        #relazione bidirezionale
        db.run("""
                  match (a:Person), (b:Person)
                  where not (a)-[:FAMILY_CONTACT]-(b) and a.p01_name <> b.p01_name and a.p02_surname = b.p02_surname
                  create (a)-[:FAMILY_CONTACT]->(b)

                  """

        )

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
                            "CREATE (a)-[r:VISITS {date: date($random)}]->(b)"
                            , name2 = "Restaurant " +str(i), randomname = list_names[randint(0, n)].strip('\n'), random = returnRandomDate())


            if(choice == 2):
                db.run("CREATE (a:Place) "
                        "SET a.p01_name = $name "
                        "SET a.p02_type = $type", name = "Hospital " +str(i), type = conf.type_of_places[1]
                            )
                for j in range(0, abs(int(np.random.normal(p, 10)))):
                    db.run("MATCH (a:Person), (b:Place) "
                            "WHERE b.p01_name = $name2 AND a.p01_name = $randomname "
                            "CREATE (a)-[r:VISITS {date: date($random)}]->(b)"
                            , name2 = "Hospital " +str(i) , randomname = list_names[randint(0, n)].strip('\n'), random = returnRandomDate())

            if(choice == 3):
                db.run("CREATE (a:Place) "
                        "SET a.p01_name = $name "
                        "SET a.p02_type = $type", name = "Theatre " +str(i), type = conf.type_of_places[2]
                            )
                for j in range(0, abs(int(np.random.normal(p, 10)))):
                    db.run("MATCH (a:Person), (b:Place) "
                            "WHERE b.p01_name = $name2 AND a.p01_name = $randomname "
                            "CREATE (a)-[r:VISITS {date: date($random)}]->(b)"
                            , name2 = "Theatre " +str(i),  randomname = list_names[randint(0, n)].strip('\n'), random = returnRandomDate())


            progress_bar['value'] += 100 / p

        return


    def createMeetRelations():

        progress_bar['value'] = 0
        progress_bar_label.config(text = "Creating 'Meets' relationships...")

        f_names = open('txts\\namesRight.txt', 'r')
        f_streets = open('txts\\places.txt')
        list_names = f_names.readlines()
        list_streets = f_streets.readlines()
        num_streets = len(list_streets)

        for i in range(0, int(n / int(conf.proportion_n_of_relationship_n_of_people))):
            db.run("MATCH (a:Person), (b:Person) "
                            "WHERE b.p01_name = $randomname1 AND a.p01_name = $randomname2 AND b.p02_surname <> a.p02_surname "
                            "CREATE (a)-[r:MEETS {date: date($random), place: $random_place}]->(b)"
                            , randomname1 = list_names[randint(0, n - 1)].strip('\n'), 
                            randomname2 = list_names[randint(0, n - 1)].strip('\n'), 
                            random = returnRandomDate(),
                            random_place = list_streets[randint(0, num_streets - 1)].strip('\n'))

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
                        "SET n.p06_infectionDate = date($date)"
                        , name = name_infected, date = returnRandomDate())



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

        family_surname = f_surnames.readline().strip('\n')


        pater_familias = Person.createPerson(f_names.readline().strip('\n'), family_surname)


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



        createFamily()



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
        dictionary[str(tupla[0])] = tupla[1]

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
            "SET n.p06_infectionDate = date($date)", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_no_vax)
            , date = conf.start_date)

    db.run( "MATCH (n : Person) "
            "WHERE n.p05_number_of_doses = 1 "
            "WITH n , rand() as r "
            "ORDER BY r "
            "LIMIT $initial_number "
            "SET n : Infected "
            "SET n.p06_infectionDate = date($date)", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_1_vax)
            , date = conf.start_date)

    db.run( "MATCH (n : Person) "
            "WHERE n.p05_number_of_doses = 2 "
            "WITH n , rand() as r "
            "ORDER BY r "
            "LIMIT $initial_number "
            "SET n : Infected "
            "SET n.p06_infectionDate = date($date)", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_2_vax)
            , date = conf.start_date)

    db.run( "MATCH (n : Person) "
            "WHERE n.p05_number_of_doses = 3 "
            "WITH n , rand() as r "
            "ORDER BY r "
            "LIMIT $initial_number "
            "SET n : Infected "
            "SET n.p06_infectionDate = date($date)", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_3_vax)
            , date = conf.start_date)

    db.run( "MATCH (n : Person) "
            "WHERE n.p05_number_of_doses = 4 "
            "WITH n , rand() as r "
            "ORDER BY r "
            "LIMIT $initial_number "
            "SET n : Infected "
            "SET n.p06_infectionDate = date($date)", initial_number = int(initial_number_of_infected * conf.proportion_of_people_initially_infected_4_vax)
            , date = conf.start_date)



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
                df_meets = db.run('MATCH (n:Infected {p01_name : $name})-[f : MEETS]-(b:Person) WHERE not b : Infected and f.date = date($date) RETURN b.p01_name, b.p05_number_of_doses, f.place', name = person_name, date = curr_date).data()
                for z in df_meets:
                    probability_of_contagion = 0.35 if z["b.p05_number_of_doses"] == 0 else (conf.probability_of_infection_with_vaccine ** z["b.p05_number_of_doses"]) ** 3
                    if(probability_of_contagion > random()):
                        infectSinglePerson(db, z["b.p01_name"], str(date), place = z["f.place"])
                
                df_places = db.run("""MATCH (a:Person {p01_name : $person})-[f:VISITS {date : date($date)}]-(n:Place) return n.p01_name""", person = person_name, date = curr_date).data()
                list_places = [d['n.p01_name'] for d in df_places]

                list_contact_place = []

                for place in list_places:
                        people = db.run("""MATCH (b:Person)-[f:VISITS {date : date($date)}]-(n:Place{p01_name : $place_name}) 
                        where b.p01_name <> $name and not b:Infected
                        return b.p01_name, b.p05_number_of_doses, n.p01_name""", name = person_name, place_name = place, date = curr_date).data()

                        list_contact_place = list_contact_place + people


                for p in list_contact_place:
                    probability_of_contagion = 0.35 if p["b.p05_number_of_doses"] == 0 else (conf.probability_of_infection_with_vaccine ** p["b.p05_number_of_doses"]) ** 3
                    if(probability_of_contagion > random()):
                        infectSinglePerson(db, p["b.p01_name"], str(date), place = p["n.p01_name"])



            for p in df_family:
                probability_of_contagion = 0.35 if p["b.p05_number_of_doses"] == 0 else (conf.probability_of_infection_with_vaccine ** p["b.p05_number_of_doses"]) ** 3
                if(probability_of_contagion > random()):
                    infectSinglePerson(db, p["b.p01_name"], str(date))

            

                






    progress_bar.pack_forget()
    progress_bar_label.pack_forget()




def findPeopleAtRisk(db):
    return db.run(
        """
        CALL{
          MATCH (a:Infected)-[v1:VISITS]-(p:Place)-[v2:VISITS]-(b:Person)
          WHERE
            duration.inDays(v1.date, a.p06_infectionDate).days < duration({days: $exposure_interval}).days AND
            v1.date = v2.date
          RETURN b.p01_name AS Name, b.p02_surname AS Surname, v2.date AS Date, p.p01_name AS Place

          UNION

          MATCH (a:Infected)-[r:MEETS]-(b:Person)
          WHERE duration.inDays(r.date, a.p06_infectionDate).days < duration({days: $exposure_interval}).days
          RETURN b.p01_name AS Name, b.p02_surname AS Surname, r.date AS Date, "unknown" AS Place
        }
        RETURN Name, Surname, Date, Place
        ORDER BY Date DESC
        """, exposure_interval = conf.exposure_interval
    ).data()



def averageContactNumber(db):
    var = db.run(
        """CALL {
        MATCH (p:Infected)-[d2:VISITS]-(place:Place)-[d1:VISITS]-(unfortunateSoul:Person)
        WHERE  p.p06_infectionDate <= d1.date AND d1.date = d2.date AND NOT unfortunateSoul:Infected
        WITH  count(unfortunateSoul) AS total1
        RETURN total1}

        CALL {
        MATCH (p2:Infected)-[d1:MEETS]-(unfortunateSoul:Person)
        WHERE  p2.p06_infectionDate <= d1.date AND NOT unfortunateSoul:Infected
        WITH  count(unfortunateSoul) AS total2
        RETURN total2}

        CAll{
        MATCH (p3:Infected)-[d2:FAMILY_CONTACT]-(unfortunateSoul:Person)
        WHERE NOT unfortunateSoul:Infected
        WITH count(unfortunateSoul) AS total3
        RETURN total3}

        CALL{MATCH (N:Infected) RETURN count(N) as totalInfected}


        RETURN total1 * 1.0 / totalInfected,
        total2 * 1.0 / totalInfected,
        total3 * 1.0 / totalInfected"""
    ).data()

    dictionary = {}

    contactTypes = ["Contact at Place", "Contact by Application", "Family Contact"]

    for i in range(0,3) :
        dictionary[contactTypes[i]] = round(((list(var[0].values()))[i]), 1)

    print(dictionary.values())

    return dictionary


def commandAddNewDose(db, name, surname, vaccine):
    result = ""

    if vaccine == "PF" :
        vaccine = 'Pfizer'
    elif vaccine == "AS" :
        vaccine = 'Astrazeneca'
    elif vaccine == "MO" :
        vaccine = 'Moderna'
    elif vaccine == "SP" :
        vaccine = 'Sputnik'
    else :
        return "Vaccine not Found"

    command = 'MATCH (n:Person {p01_name :"' + name + '", p02_surname : "' + surname + '", p04_vaccine : "' + vaccine + '"})' + '\nSET n.p05_number_of_doses = 1+n.p05_number_of_doses' + '\nUNION' + '\nMATCH (n:Person {p01_name :"' + name + '", p02_surname : "' + surname + '"})' + '\nWHERE n.p04_vaccine <> "' + vaccine + '"' + '\nSET n.p05_number_of_doses = 1, n.p04_vaccine = "' + vaccine + '"'

    db.run(command)

    var = db.run('MATCH (n:Person {p01_name :"' + name + '", p02_surname : "' + surname + '"})' + 'RETURN n.p01_name, n.p02_surname, n.p04_vaccine, n.p05_number_of_doses').data()

    if len(var) > 0 :
        var = list(var[0].values())
        var[0] = var[0] + " "
        var[1] = var[1] + " : "
        var[2] = var[2] + ", "
        var[3] = str(var[3]) + " dose(s)"
        for i in range(len(var)) :
            result = result + str(var[i])
    else :
        result = "Individual not found"

    return result

def commandInfectFamilies(db):
    db.run('MATCH (x:Person:Infected)-[:FAMILY_CONTACT]-(y:Person) SET y:Person:Infected')

def addContact(db, fn_A, ln_A, fn_B, ln_B, date, place):
    if (fn_A != "" and ln_A != "" and date != ""):
        if (fn_B == "" and ln_B == "" and place != ""):
            db.run(
                """
                MATCH (a:Person {p01_name: $fn_A, p02_surname: $ln_A}), (p:Place {p01_name: $place})
                CREATE (a)-[r:VISITS {date: date($date)}]->(p)
                """, fn_A = fn_A, ln_A = ln_A, date = date, place = place
            )
            return "Created VISITS relationship"
        elif (fn_B != "" and ln_B != "" and place == ""):
            db.run(
                """
                MATCH (a:Person {p01_name: $fn_A, p02_surname: $ln_A}), (b:Person {p01_name: $fn_B, p02_surname: $ln_B})
                CREATE (a)-[r:MEETS {date: date($date)}]->(b)
                """, fn_A = fn_A, ln_A = ln_A, fn_B = fn_B, ln_B = ln_B, date = date
            )
            return "Created MEETS relationship"
    else:
        return "Invalid query paramenters"
