import csv
from pprint import pprint
from crud import create_trail
from model import connect_to_db, db
from server import app

connect_to_db(app)
app.app_context().push()



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
            geoloc = eval(line['_geoloc'])
            latitude = geoloc['lat']
            longitude = geoloc['lng']
            length = line['length']
            elevation_gain = line['elevation_gain']
            difficulty = line['difficulty_rating']
            route_type = line['route_type']

            trail = create_trail(trail_id, trail_name, city_name, state_name, latitude, longitude, length, elevation_gain, difficulty, route_type)

            db.session.add(trail)
        db.session.commit()

# test_dict = eval(line['_geoloc'])
# print(test_dict['lat'])

trail_data()


