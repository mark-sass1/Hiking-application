import csv
from pprint import pprint
# # Load trails data from CSV file
# with open('all-trails.csv') as csvfile:
#     trail_file = csv.reader(csvfile)

def trail_data():
    # print(trail_file)
    # data = open(trail_file)

# Load trails data from CSV file
    with open('all-trails.csv') as csvfile:
        trail_file = csv.DictReader(csvfile)

        for line in trail_file:
            trail_id = line['trail_id']
            trail_name = line['name']
            city_name = line['city_name']
            state_name = line['state_name']
            lattitude = line['_geoloc']['lat']
            longitude = line['_geoloc']['long']
            length = line['length']
            elevation_gain = line['elevation_gain']
            difficulty = line['difficulty_rating']
            route_type = line['route_type']
            

    # pprint(data[0])

    
    
    # print(trail_id, trail_name, length)

trail_data()

