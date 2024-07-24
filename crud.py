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

