from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
   """A user"""
   
   __tablename__ = "users"
   
   user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   email = db.Column(db.String, unique=True)
   password = db.Column(db.String)
   hiking_experience = db.Column(db.String)



class Trails(db.Model):
   """A Trail list"""
   
   __tablename__= "trails"
   
   trail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   trail_name = db.Column(db.String)
   state_name = db.Column(db.String)
   city_name =db.Column(db.String)
   latitude = db.Column(db.Float)
   longitude = db.Column(db.Float)
   length = db.Column(db.Integer)
   elevation_gain = db.Column(db.Integer)
   difficulty = db.Column(db.Integer)
   route_type = db.Column(db.String)



class Training_Path(db.Model):
    """user training path"""

    __tablename__ = "training_path"

    Training_Path_id =db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    summit_goal = db.Column(db.String)
    training_trails = db.Column(db.String)
    trails_completed = db.Column(db.String)
    progress_mileage = db.Column(db.Float)


class Activity_log(db.Model):
    """user log"""

    __tablename__ = "activities"

    training_path_id = db.Column(db.Integer, db.ForeignKey("training_path.training_path-id"))
    mileage_log = db.Column(db.Integer)
    sub_summit_trails = db.Column(db.String)
    trail_notes = db.Column(db.Text)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trail_id"))





def connect_to_db(flask_app, db_uri="postgresql:///hiking-buddy", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)