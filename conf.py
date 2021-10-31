import datetime


#database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "sr"


#initial date and final date

start_date = datetime.date(2020, 3, 1)
end_date = datetime.date(2020, 3, 31)



vaccines = ('Pfizer', 'Astrazeneca', 'Moderna', 'Sputnik')
vaccine_probability = 0.7
#1 vaccine 0,5 2 vaccines 0,5 x 0,5 = 0,25
probability_of_infection_with_vaccine = 0.5



type_of_places = ('Restaurant', 'Hospital', 'Theatre')

proportion_n_of_people_n_of_place = 10 / 1
proportion_n_of_relationship_n_of_people = 1 / 1
proportion_n_of_people_n_of_infected = 20 / 1

