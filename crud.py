from model import db, User, Trails, Training_path, Activity_log, Training_trails, connect_to_db


def create_user(name, email, password):
    """Create and return a new user."""

    user = User(name=name, email=email, password=password)


    return user

def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_training_path_by_user_id(user_id):
    """Return a training path by user id"""

    return Training_path.query.filter(Training_path.user_id == user_id).first()




def create_trail(trail_id, trail_name, city_name, state_name, latitude, longitude, length, elevation_gain, difficulty, route_type):
    trail =  Trails(trail_id=trail_id,
                    trail_name=trail_name,
                    city_name=city_name,
                    state_name=state_name,
                    latitude=latitude,
                    longitude=longitude,
                    length=length,
                    elevation_gain=elevation_gain,
                    difficulty=difficulty,
                    route_type=route_type,
                    )



    return trail

def get_states():

    return Trails.query.order_by(Trails.state_name).all()

def search_trails_by_name(trail_name):
    
    return Trails.query.filter_by(trail_name=trail_name).first()

def get_trails():

    return Trails.query.order_by(Trails.trail_name).all()

def get_trail_by_id(trail_id):

    return Trails.query.get(trail_id)

def create_training_path(user_id, summit_goal):

    training_path = Training_path(user_id=user_id, summit_goal=summit_goal)

    return training_path

def create_training_trail(trail_id, training_path_id):

    training_trail = Training_trails(trail_id=trail_id, training_path_id=training_path_id)

    return training_trail

def create_activity_log(mileage_log, trail_notes, training_path_id):

    activity_log = Activity_log(mileage_log=mileage_log, trail_notes=trail_notes, training_path_id=training_path_id)
    print(activity_log.mileage_log)
    return activity_log

def get_completed_trails(training_path_id):
    """Return the number of completed trails for a given training path."""
    return Training_trails.query.filter_by(training_path_id=training_path_id, trails_completed=True).count()

def get_total_trails(training_path_id):
    """Return the total number of trails for a given training path."""
    return Training_trails.query.filter_by(training_path_id=training_path_id).count()

def get_training_path_mileage(training_path_id):
    all_trails = Training_trails.query.filter_by(training_path_id=training_path_id).all()
    total_mileage = 0
    for trail in all_trails:
        tr_trail = get_trail_by_id(trail.trail_id)
        total_mileage += tr_trail.length
    print(total_mileage)
    return total_mileage
    
def activity_log_mileage(training_path_id):
    activity_mileage = Activity_log.query.filter_by(training_path_id=training_path_id).all()

    total_activity_mileage = 0
    for mileage in activity_mileage:
        if mileage.mileage_log:
            total_activity_mileage += mileage.mileage_log
    print(total_activity_mileage)
    return total_activity_mileage