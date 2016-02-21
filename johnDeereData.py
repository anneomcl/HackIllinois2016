import pickle
from requests_oauthlib.oauth1_session import OAuth1Session
import json
from numpy import random

DEFAULT_JSON_HEADER = {'Accept': 'application/vnd.deere.axiom.v3+json'}
base_url = 'https://apicert.soa-proxy.deere.com/platform'
client_key = 'johndeere-54ET8agkbEm5s5WT83Kfyx57'
client_secret = 'af433adb114ea5539aca09cc0c09f53cb52a2237'
oauth_session = OAuth1Session(client_key, client_secret=client_secret,
                                      resource_owner_key='c2eb1ca4-dc44-4d92-adcd-d0888359af78',
                                      resource_owner_secret='Xi42JPNcK5xKoxsiv2MuK5Wr/TPkGRzmu/oAlCIOk19VBdwP8RzE+ZzAms0dFL7FS96m+qX7ag2Z7WuO24W01bxdZkHaiWf24lNR+BaQwu4=')
r = oauth_session.get(base_url + '/', headers=DEFAULT_JSON_HEADER)

def corn_or_soy():
    if random.randint(2) == 0:
        return "CORN"
    else:
        return "SOY"

def my_handle_endpoint(this_choice):
    _response = None
    _url = this_choice

    if _url is not None:
        _response = oauth_session.get(_url, headers=DEFAULT_JSON_HEADER).json()
        if len(_response) > 0:
            data = json.dumps(_response, indent=4, sort_keys=True)
            return data

    return _response

def get_Deere_Data():


    choice = "https://apicert.soa-proxy.deere.com/platform/organizations/223031/fields"
    data = my_handle_endpoint(choice)
    json_data = json.loads(my_handle_endpoint(choice))
    wr = open('fieldData.json', 'w+')
    wr.write(data)

    product_sprayed = {} #product_sprayed[i][j] : amount of product used PER hectare (L/ha) field i at timeline j
    seeds_planted = {} #seeds_planted [i][j] : seeds planted Per hecare (seeds/ha) field i at time j
    crops_harvested = {} #crops_harvested[i][j] : crops PER hecatre (bu/ha) field i at time j
    for item in json_data["values"]:
        name = item["name"]
        for link in item["links"]:
            if "fieldOperations" in link["uri"]:
                choice = link["uri"]
                data = my_handle_endpoint(choice)
                json_data_field = json.loads(my_handle_endpoint(choice))
                wr = open('field' + name + ".json", 'w+')
                wr.write(data)
                for crop_item in json_data_field["values"]:
                        for crop_link in crop_item["links"]:
                            if crop_link['rel'] == 'measurementTypes':
                                choice = crop_link["uri"]
                                data = my_handle_endpoint(choice)
                                json_data_field2 = json.loads(my_handle_endpoint(choice))
                                if crop_item["fieldOperationType"] == "application":
                                    if name not in product_sprayed:
                                        product_sprayed[name] = {}
                                    for product in json_data_field2["values"][0]["productTotals"]:
                                        product_sprayed[name] = [product["name"],
                                                                 (str(product["averageMaterial"]["value"]) + product["averageMaterial"]["unitId"]),
                                                                product["averageMaterial"]["value"],
                                                                corn_or_soy()]
                                        if "components" in crop_item["product"]:
                                            for comp in crop_item["product"]["components"]:
                                                product_sprayed[name].append((comp["name"], comp['rate']["value"]))
                                        elif "name" in crop_item["product"]:
                                            product_sprayed[name].append(crop_item["product"]["name"])
                                        else:
                                            product_sprayed[name].append("WATER")

                                if crop_item["fieldOperationType"] == "seeding":
                                    seeds_planted[name] = ((json_data_field2["values"][0]["area"]["value"],
                                                                     crop_item["cropName"],
                                                                    json_data_field2["values"][0]["averageMaterial"]["value"]))
                                if crop_item["fieldOperationType"] == "harvest":
                                    crops_harvested[name] = ((json_data_field2["values"][0]["area"]["value"],
                                                                    crop_item["cropName"],
                                                                    json_data_field2["values"][0]["averageYield"]["value"]))

    chemical_types = [] #(type)
    choice = "https://apicert.soa-proxy.deere.com/platform/chemicalTypes"
    data = my_handle_endpoint(choice)
    json_data = json.loads(my_handle_endpoint(choice))
    wr = open('chemicalData.json', 'w+')
    wr.write(data)
    for elem in json_data["values"]:
        chemical_types.append(elem["name"])

    fertilizer_types = [] #(type)
    choice = "https://apicert.soa-proxy.deere.com/platform/fertilizerTypes"
    data = my_handle_endpoint(choice)
    json_data = json.loads(my_handle_endpoint(choice))
    wr = open('fertilizerData.json', 'w+')
    wr.write(data)
    for elem in json_data["values"]:
        fertilizer_types.append(elem["name"])

    crop_types = [] #(name, density)
    choice = "https://apicert.soa-proxy.deere.com/platform/cropTypes"
    data = my_handle_endpoint(choice)
    json_data = json.loads(my_handle_endpoint(choice))
    wr = open('cropTypeData.json', 'w+')
    wr.write(data)
    for elem in json_data["values"]:
        crop_types.append((elem["name"], elem["densityFactor"]["value"]))

    with open('fieldSprayData.json', 'w+') as outfile:
        json.dump(product_sprayed, outfile)

    with open('fieldHarvestData.json', 'w+') as outfile:
        json.dump(crops_harvested, outfile)

    with open('fieldSeedData.json', 'w+') as outfile:
        json.dump(seeds_planted, outfile)

    johndeere_data = {}
    johndeere_data["chemical"] = chemical_types
    johndeere_data["fertilizer"] = fertilizer_types
    johndeere_data["crop_types"] = crop_types
    johndeere_data["spray"] = product_sprayed
    johndeere_data["harvest"] = crops_harvested
    johndeere_data["seeds"] = seeds_planted

    f = open('JOHNDEEREdata.pkl', 'wb')
    pickle.dump(johndeere_data, f)
    f.close()

    return johndeere_data

a = get_Deere_Data()