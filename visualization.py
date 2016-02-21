import json
from algorithm import croptimize
import numpy

#croptimize(a, b, c, DIVERSITY, data, data)
def map_diversity(jsonData):
    data = centroid_data(jsonData)
    return map_crop_to_field(croptimize(.33, .33, .33, 3, len(data)), data)

def map_water(jsonData):
    data = centroid_data(jsonData)
    return map_crop_to_field(croptimize(.6, .1, .3, 1.5, len(data)), data)

def map_chemical(jsonData):
    data = centroid_data(jsonData)
    return map_crop_to_field(croptimize(.1, .1, .8, 1.5, len(data)), data)

#input map_crop_to_field
#returns {"CORN" : [(lat, long), (lat, long)...] ... }
def map_balanced(jsonData):
    data = centroid_data(jsonData)
    return map_crop_to_field(croptimize(.33, .33, .33, 2, len(data)), data)

def map_crop_to_field(crop_counts, centroids):

    crop_counts = dict((k, v) for k, v in crop_counts.items() if v > 0)

    crop_to_centroid = {} #put icon of key crop on all centroids in value
    for elem in crop_counts:
        crop_to_centroid[elem] = []

    for elem in crop_counts:
        start = centroids.pop()
        crop_to_centroid[elem].append(start)
        for i in range(0, crop_counts[elem] - 1):
            nearest = find_nearest_centroid(start, centroids)
            crop_to_centroid[elem].append(nearest)

    return crop_to_centroid

def find_nearest_centroid(start, centroids):
    best_dst = 1000
    best_centroid = -1
    for item in centroids:
        dst = numpy.sqrt((start[0] - item[0])**2 + (start[1] - item[1])**2)
        if dst < best_dst:
            best_dst = dst
            best_centroid = item
    centroids.remove(best_centroid)
    return best_centroid

def centroid_data(climate_data):
    centroid = []
    '''with open('cods.json', 'r') as f:
        str_data = f.read()
    json_data = json.loads(str_data)'''
    print(climate_data)
    for elem in climate_data["features"]:
        centroid.append(elem["properties"]["centroid"])
    return centroid