import datetime


#database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "sr"


#initial date and final date

start_date = datetime.date(2020, 3, 1)
end_date = datetime.date(2020, 3, 15)
time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days

#Exposure interval i.e. how many days before a positive test we check for trasmission of covid
exposure_interval = 10

vaccines = ('Pfizer', 'Astrazeneca', 'Moderna', 'Sputnik')
vaccine_probability = 0.7
#1 vaccine 0,5 2 vaccines 0,5 x 0,5 = 0,25
probability_of_infection_with_vaccine = 0.3

#simulation parameters
proportion_of_people_initially_infected_no_vax = 0.6
proportion_of_people_initially_infected_1_vax = 0.2
proportion_of_people_initially_infected_2_vax = 0.1
proportion_of_people_initially_infected_3_vax = 0.07
proportion_of_people_initially_infected_4_vax = 0.03






type_of_places = ('Restaurant', 'Hospital', 'Theatre')

proportion_n_of_people_n_of_place = 10 / 1
proportion_n_of_relationship_n_of_people = 1 / 1
proportion_n_of_people_n_of_infected = 8 / 1
