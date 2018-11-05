import random
import math
from citiesReader import readCities

alpha = 1
beta = 5
ant_number = 100
Q = 500
K = 100

cities = readCities()
visited = []
pheromones = {}# (city_from, city_to) -> pheromones
city_solve = next(
    filter(
        lambda city: city.cityname == 'A',
        cities),
    None)

def calculate_distance(city_from, city_to):
    x1 = city_from.x
    y1 = city_from.y
    x2 = city_to.x
    y2 = city_to.y

    return math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 )

def get_visibility(city_from, city_to):
    return 1 / calculate_distance(city_from, city_to)

def is_visited(city):
    return city in visited

def set_visited(city):
    visited.append(city)

def get_pheromone(city_from, city_to):
    pair = (city_from, city_to)
    if(pair in pheromones.keys()):
        return pheromones[pair]
    return 0

def update_pheromone(city_from, city_to):
    new_pheromone = (1 - random.random()) * get_pheromone(city_from, city_to) + delta
    pheromones[(city_from, city_to)] = new_pheromone

def get_movement_probability(city_from, city_to, candidates_cities):
    def calc_main_part(city_from, city_to):
        return (get_pheromone(city_from, city_to) ** alpha) * (get_visibility(city_from, city_to) ** beta)
    sum = 0
    for candidate in candidates_cities:
        sum += calc_main_part(city_from, candidate)
    return calc_main_part(city_from, city_to) / sum

def get_length_of_trail(trail):
    full_length = 0

    for i in range(len(trail) - 1):
        city_from = trail[i]
        city_to = trail[i+1]
        length = calculate_distance(city_from, city_to)
        full_length += length
    return full_length

def print_trail(trail):
    for city in trail:
        print(city.cityname + " -> ", end='')
    print()

def get_unvisited_cities():
    unvisited = []
    for city in cities:
        if city not in visited:
            unvisited.append(city)

def main():
    for k in K:
        for ant in ants:
            current_city = ant.current_city
            transition_probabilities = []
            for city_candidate in get_unvisited_cities():
                p = get_movement_probability(current_city, city_candidate)
                transition_probabilities.append(p)

main()