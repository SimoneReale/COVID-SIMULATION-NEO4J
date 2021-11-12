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
probability_of_infection_with_vaccine = 0.3

#simulation parameters
proportion_of_people_initially_infected_no_vax = 0.6
proportion_of_people_initially_infected_1_vax = 0.2
proportion_of_people_initially_infected_2_vax = 0.1
proportion_of_people_initially_infected_3_vax = 0.07
proportion_of_people_initially_infected_4_vax = 0.03

type_of_places = ('Restaurant', 'Hospital', 'Theatre')
type_of_test = ("MOLECULAR_TEST", "ANTIGEN_TEST", "ANTIBODY_TEST")

proportion_n_of_people_n_of_place = 10 / 1
proportion_n_of_relationship_n_of_people = 1 / 1
#proportion for creating test connection with person
proportion_n_of_molecular_test_n_of_people = 1 / 10
proportion_n_of_antigen_test_n_of_people = 1 / 20
proportion_n_of_antibody_test_n_of_people = 1 / 50
#proportion of positivity per test
proportion_n_of_positive_n_of_molecular_test = 1 / 10
proportion_n_of_positive_n_of_antigen_test = 2 / 10
proportion_n_of_positive_n_of_antibody_test = 5 / 10
proportion_n_of_people_n_of_infected = 8 / 1
proportion_n_of_daily_test_n_of_people = 1 / 10
