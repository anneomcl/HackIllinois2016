from numpy import random
import pickle

#University of IOWA
SEEDS_PER_BUSHEL_CORN = 1/100,000
SEEDS_PER_BUSHEL_SOY = 1/150,000

COST_CORN_SEEDS_PER_BUSHEL = 4.94
COST_SOY_SEEDS_PER_BUSHEL = 9.57

def data_init():
    with open('JOHNDEEREdata.pkl', 'rb') as f:
        return pickle.load(f)

#Only run this once per log-in
def croptimize_init():

    data = data_init()
    crop_yield_cost = {}

    #find relative cost of crops by yield
    for elem in data["seeds"]:
        if(data["harvest"][elem] in data["harvest"]):
            if(elem[1] not in crop_yield_cost):
                crop_yield_cost[elem[1]] = 0

            bushels_per_area = data["harvest"][2]
            seeds_per_area = data["seeds"][2] / data["seeds"][0]
            if(elem[1] == "SOY"):
                expected_bushel = seeds_per_area*SEEDS_PER_BUSHEL_SOY
            else:
                expected_bushel = seeds_per_area*SEEDS_PER_BUSHEL_CORN
            actual_bushel = bushels_per_area - expected_bushel

            crop_yield_cost[elem[1]] -= actual_bushel

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
        x = random.randint(20000, 50000)
        y = random.randint(20000, 50000)
        cost_dict[elem[0]] = (elem[1]*x - elem[1]*y)/1000000

def add_false_data_water(cost_dict):
    data = data_init()
    water_val = random.random_sample()*20 + 50
    for elem in data["crop_types"]:
        cost_dict[elem[0]] = (-1*elem[1] + water_val)/water_val
    cost_dict["CORN_WET"] = (-1*random.random_sample()*20 + 50 - water_val)/water_val
    cost_dict["SOYBEANS"] = (-1*random.random_sample()*20 + 50 - water_val)/water_val

def add_false_data_spray(cost_dict):
    data = data_init()
    for elem in data["crop_types"]:
        cost_dict[elem[0]] = random.randint(20, 30)/30

def croptimize():
    return

croptimize_init()