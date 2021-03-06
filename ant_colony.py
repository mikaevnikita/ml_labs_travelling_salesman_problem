import random
import math
from citiesReader import readCities

alpha = 1
beta = 1
ants_number = 10
Q = 10
K = 10

cities = readCities()
visited = {}
pheromones = {}# (city_from, city_to) -> pheromones
city_solve = next(
    filter(
        lambda city: city.cityname == 'A',
        cities),
    None)
ants = []

class Ant:
    def __init__(self, random_city):
        self.city = random_city

def calculate_distance(city_from, city_to):
    x1 = city_from.x
    y1 = city_from.y
    x2 = city_to.x
    y2 = city_to.y

    return math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 )

def get_visibility(city_from, city_to):
    distance = calculate_distance(city_from, city_to)
    if distance == 0:
        return 0
    return 1 / distance

def is_visited(city):
    return visited.get(city, False)

def set_visited(city):
    visited[city] = True

def get_pheromone(city_from, city_to):
    pair = (city_from, city_to)
    if pair in pheromones.keys():
        return pheromones[pair]
    return 0

def update_pheromone(city_from, city_to, trail_length):
    new_pheromone = (1 - random.random()) * get_pheromone(city_from, city_to) + (Q/trail_length)
    pheromones[(city_from, city_to)] = new_pheromone

def update_pheromones(trail):
    trail_length = get_length_of_trail(trail)
    for i in range(len(trail) - 1):
        city_from = trail[i]
        city_to = trail[i+1]
        update_pheromone(city_from, city_to, trail_length)

def get_movement_probability(city_from, city_to, candidates_cities):
    if calculate_distance(city_from, city_to) == 0:
        return 0
    calc_main_part = lambda city_from, city_to: (get_pheromone(city_from, city_to) ** alpha) * (get_visibility(city_from, city_to) ** beta)
    sum = 0
    for candidate in candidates_cities:
        if candidate != city_from:
            sum += calc_main_part(city_from, candidate)
    main_part = calc_main_part(city_from, city_to)
    return main_part / sum

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
        if not is_visited(city):
            unvisited.append(city)
    return unvisited

def init_pheromones():
    pheromones.clear()
    for city_i in cities:
        for city_j in cities:
            if city_i != city_j:
                pheromones[(city_i, city_j)] = 1
            else:
                pheromones[(city_i, city_i)] = 0

def init_ants():
    ants.clear()
    for i in range(ants_number):
        ants.append(Ant(city_solve))

def main():
    init_pheromones()
    init_ants()

    minimal_trail_length = float('inf')
    minimal_trail = []

    for k in range(K):
        for ant in ants:
            current_trail = []
            while True:
                unvisited_cities = get_unvisited_cities()
                if len(unvisited_cities) == 0:
                    current_trail.append(city_solve)
                    break
                current_city = ant.city
                current_trail.append(current_city)
                transition_probabilities = []
                for city_candidate in get_unvisited_cities():
                    p = get_movement_probability(current_city, city_candidate, get_unvisited_cities())
                    transition_probabilities.append((city_candidate, p))
                best_candidate_pair = max(transition_probabilities, key=lambda pair : pair[1])
                best_candidate = best_candidate_pair[0]

                ant.city = best_candidate
                set_visited(current_city)
            current_trail_length = get_length_of_trail(current_trail)
            if current_trail_length < minimal_trail_length:
                minimal_trail_length = current_trail_length
                minimal_trail = current_trail
            visited.clear()
            update_pheromones(current_trail)
        init_ants()
    print_trail(minimal_trail)
    print("Length: " + str(minimal_trail_length))
main()