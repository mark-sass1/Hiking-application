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
   city_name =db.Column(db.String)
   state_name = db.Column(db.String)
   latitude = db.Column(db.Float)
   longitude = db.Column(db.Float)
   length = db.Column(db.Integer)
   elevation_gain = db.Column(db.Integer)
   difficulty = db.Column(db.Integer)
   route_type = db.Column(db.String)

   training_trails= db.relationship("Training_trails", back_populates="trails")


class Training_path(db.Model):
    """user training path"""

    __tablename__ = "training_path"

    training_path_id =db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    summit_goal = db.Column(db.String)
    training_trails = db.Column(db.String)
    training_path_completed = db.Column(db.Boolean)
    progress_mileage = db.Column(db.Float)

    activities = db.relationship("Activity_log", back_populates="training_path")
    


class Activity_log(db.Model):
    """user log"""

    __tablename__ = "activities"

    activity_log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    training_path_id = db.Column(db.Integer, db.ForeignKey("training_path.training_path_id"))
    mileage_log = db.Column(db.Integer)
    sub_summit_trails = db.Column(db.String)
    trail_notes = db.Column(db.Text)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trail_id"))

    training_path = db.relationship("Training_path", back_populates="activities")


class Training_trails(db.Model):
    """training trails"""

    __tablename__ = "training_trails"

    training_trail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trail_id"))
    training_path_id = db.Column(db.Integer, db.ForeignKey("training_path.training_path_id"))
    trails_completed = db.Column(db.Boolean)

    trails = db.relationship("Trails" , back_populates="training_trails")



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