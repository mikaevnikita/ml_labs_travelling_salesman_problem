import random
import math
from citiesReader import readCities

city_solve = 'A'
temp = 10000
coolingRate = 0.003

def get_random_initial_state(initial_city, cities):
    cities.remove(initial_city)
    return [initial_city] + random.sample(cities, len(cities)) + [initial_city]

def get_random_next_state(initial_city, current_state):
    current_state_view = list(filter(lambda city: city != initial_city, current_state))

    i = random.randint(0, len(current_state_view) - 1)
    j = random.randint(0, len(current_state_view) - 1)

    return [initial_city] + swapped(current_state_view, i, j) + [initial_city]

def swapped(old_list, i, j):
    new_list = old_list[:]
    new_list[i], new_list[j] = new_list[j], new_list[i]
    return new_list


def calculate_distance(city_from, city_to):
    x1 = city_from.x
    y1 = city_from.y
    x2 = city_to.x
    y2 = city_to.y

    return math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 )


def get_energy(state):
    full_energy = 0

    for i in range(len(state) - 1):
        city_from = state[i]
        city_to = state[i+1]
        energy = calculate_distance(city_from, city_to)
        full_energy += energy
    return full_energy


def get_acceptance_probability(energy, new_energy, temperature):
    if new_energy < energy:
        return 1
    else:
        return math.exp(-(new_energy - energy) / temperature)

def print_path(state):
    for city in state:
        print(city.cityname + " -> ", end='')
    print()


def main():
    global temp

    cities = readCities()
    initial_city = next(
        filter(
            lambda city : city.cityname == city_solve,
                   cities),
        None)

    best_state = get_random_initial_state(initial_city,
                             cities)

    while temp > 1:
        next_state = get_random_next_state(initial_city, best_state)
        energy = get_energy(best_state)
        new_energy = get_energy(next_state)
        probability = get_acceptance_probability(energy, new_energy, temp)

        if probability >= random.random():
            best_state = next_state

        temp *= 1 - coolingRate

    print_path(best_state)
    print("Energy: " + str(get_energy(best_state)))
main()