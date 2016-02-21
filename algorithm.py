import numpy
from numpy import random
import pickle

#Source: University of IOWA
SEEDS_PER_BUSHEL_CORN = .00001 #1/100,000
SEEDS_PER_BUSHEL_SOY = .0000067 #1/150,000

COST_CORN_SEEDS_PER_BUSHEL = 4.94
COST_SOY_SEEDS_PER_BUSHEL = 9.57

#balanced: .33, .33, .33
#profit: .1, .8, .1
#water conservation: .6, .01, .3
#chemical-free: .1, .01, .8
def croptimize(least_water, most_profit, least_chemicals, diversity, num_fields):
    costs = croptimize_init() #negative means you should bias, positive is a cost to lean away from
    normalize_costs(costs)

    best_crops = {}
    crop_counts = {}

    for elem in costs["yield"]:
        crop_counts[elem] = 0
        best_crops[elem] = most_profit*costs["yield"][elem] \
                           + least_chemicals*costs["spray"][elem] \
                           + least_water*costs["water"][elem]

    for i in range(0, num_fields):
        crop = min(best_crops.items(), key=lambda x: x[1])
        crop_counts[crop[0]] += 1
        div_factor = (diversity*diversity*random.random_sample()*random.random_sample()*numpy.abs(best_crops[crop[0]]))
        best_crops[crop[0]] += div_factor

    return crop_counts

def normalize_costs(costs):
    for elem in costs["spray"]:
        costs["spray"][elem] /= 5
    for elem in costs["yield"]:
        costs["yield"][elem] /= 2
    for elem in costs["water"]:
        costs["water"][elem] /= 1

def data_init():
    with open('JOHNDEEREdata.pkl', 'rb') as f:
        return pickle.load(f)

#Only run this once per log-in
def croptimize_init():

    data = data_init()
    crop_yield_cost = {}

    #find relative cost of crops by yield
    for elem in data["seeds"]:
        if("CORN" in data["harvest"][elem][1]):
            bushels_per_area = data["harvest"][elem][2]
            seeds_per_area = data["seeds"][elem][2] / data["seeds"][elem][0]
            expected_bushel = seeds_per_area*SEEDS_PER_BUSHEL_CORN
            actual_bushel = bushels_per_area - expected_bushel
            crop_yield_cost["CORN"] = -1*actual_bushel/1000
        if("SOY" in data["harvest"][elem][1]):
            bushels_per_area = data["harvest"][elem][2]
            seeds_per_area = data["seeds"][elem][2] / data["seeds"][elem][0]
            expected_bushel = seeds_per_area*SEEDS_PER_BUSHEL_SOY
            actual_bushel = bushels_per_area - expected_bushel
            crop_yield_cost["SOY"] = -1*actual_bushel/1000

    add_false_data_yield(crop_yield_cost)

    #find relative cost of crops by water consumption
    water_cost = {}
    add_false_data_water(water_cost)

    #find relative cost of spray
    spray_cost = {}
    soy_count = 0
    corn_count = 0
    for elem in data["spray"]:
        spray_cost[data["spray"][elem][3]] = 0
        if data["spray"][elem][3] == "CORN":
            corn_count +=1
        else:
            soy_count += 1
        for i in range(4, len(data["spray"][elem])):
            spray_cost[data["spray"][elem][3]] += data["spray"][elem][2]
    spray_cost["CORN"] /= (corn_count*30)
    spray_cost["SOY"] /= (soy_count*30)

    add_false_data_spray(spray_cost)

    costs = {}
    costs["spray"] = spray_cost #chemicals used
    costs["water"] = water_cost #water used
    costs["yield"] = crop_yield_cost #utility/profit

    return costs
    #find total spray product per plant
    #find cost fertilizer per plant, cost chemicals

def add_false_data_yield(cost_dict):
    data = data_init()
    for elem in data["crop_types"]:
        x = random.randint(49000, 50000)
        y = random.randint(49000, 50000)
        cost_dict[elem[0]] = (elem[1]*x - elem[1]*y)/1000000

def add_false_data_water(cost_dict):
    data = data_init()
    water_val = random.random_sample()*20 + 50
    for elem in data["crop_types"]:
        cost_dict[elem[0]] = (-1*elem[1] + water_val)/water_val
    cost_dict["CORN"] = (-1*random.random_sample()*20 + 50 - water_val)/water_val
    cost_dict["SOY"] = (-1*random.random_sample()*20 + 50 - water_val)/water_val

def add_false_data_spray(cost_dict):
    data = data_init()
    for elem in data["crop_types"]:
        cost_dict[elem[0]] = random.randint(20, 30)/30

croptimize(.1, .8, .1, .5, 12)
croptimize(.1, .8, .1, 1, 12)
croptimize(.1, .8, .1, 1.5, 12)
croptimize(.1, .8, .1, 1.75, 12)
croptimize(.1, .8, .1, 2, 12)
croptimize(.1, .8, .1, 5, 12)