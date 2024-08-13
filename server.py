from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, Trails
# from crud import get_trails, get_trail_by_id, get_users, create_user, create_training_trail
import crud
import random


app = Flask(__name__)
app.secret_key = "dev"


@app.route("/")
def homepage():
    """Homepage"""
    return render_template("homepage.html")


@app.route("/trails")
def all_trails():
    """View all trails."""

    trails = crud.get_trails()

    states_trails = {

    }

    for trail in trails:
        state = trail.state_name
        check_trail_state = states_trails.get(state)
        if check_trail_state is None:
            states_trails[state]=[trail]
        else:
            states_trails[state].append(trail)

    state_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", 
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", 
    "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", 
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", 
    "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", 
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", 
    "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", 
    "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    

    return render_template("trails_route.html", states_trails=states_trails, state_list=state_list)

@app.route("/search-trails")
def search_trails():
    query = request.args.get('query')
    # the user types in a trail name that needs to be validated
    state_list = crud.get_states()
    states_trails = crud.search_trails_by_name(query) # returns a single item
    states_trails = [states_trails]

    # check if states_trails returned None

    
    return render_template("trails_route.html", state_list=state_list, states_trails=states_trails)


@app.route("/trails/<trail_id>")
def get_trail(trail_id):
    """Show details on a particular trail."""

    trail = crud.get_trail_by_id(trail_id)

    return render_template("trail_details.html", trail=trail)


@app.route("/register", methods=["POST"])
def create_user():
    """Create a new user."""

    user_name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    print(user_name, email, password)
    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
        return redirect("/")
    else:
        user = crud.create_user(user_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")

        """Account created, and logged in"""
        session["user_email"] = user.email
        flash(f"Welcome, {user.name}!")
        return redirect("/account")
    

    
@app.route("/users/<user_id>")
def show_user(user_id):
    """User details"""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else: # log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

        return redirect("/account")

    return redirect("/")


@app.route("/account")
def user_details():
    """Users account"""
    
    user = crud.get_user_by_email(session["user_email"])
    training_path = crud.get_training_path_by_user_id(user.user_id)
    training_trails = []
    if training_path:
        activity_log_mileage = crud.activity_log_mileage(training_path.training_path_id)
        # print(activity_log_mileage)
        total_trails = crud.get_training_path_mileage(training_path.training_path_id) # fix => based on length of each trail
        # convert total_trails from feet to miles
        calculated_miles = total_trails/5280
        print(calculated_miles)
        completed_trails = crud.get_completed_trails(training_path.training_path_id)
        # TODO - fix calculation for completion based on mileage
        completion_percentage = (activity_log_mileage / calculated_miles * 10)
        print(completion_percentage)
        
        for trail in training_path.training_trails:
            tr_trail = crud.get_trail_by_id(trail.trail_id)
            training_trails.append(tr_trail)

            # end up with list of objects
    else:
        completion_percentage = 0

    
    return render_template("user_details.html", user=user, training_path=training_path, completion_percentage=completion_percentage, training_trails=training_trails, activity_log_mileage=activity_log_mileage)
# get training path by user id
    # pass training path / summit goal to jinja template
    # might create crud function to crud.get_training_path_by_user_id()

    #  query for the user's activity to display the activity log

@app.route("/users")
def get_users():
    """View all users."""

    users = crud.get_users(users)

    return render_template("users.html", users=users)

            
@app.route("/choose_summit", methods=["POST"])
def summit_goal():

    trail_id = request.form.get("trail_id")
    summit_goal = request.form.get("summit_goal")

    trail = crud.get_trail_by_id(trail_id)

    user = crud.get_user_by_email(session["user_email"])

    training_path = crud.create_training_path(user.user_id, trail.trail_name)
    db.session.add(training_path)
    db.session.commit()

    training_trails = Trails.query.filter(Trails.state_name == trail.state_name, Trails.difficulty < trail.difficulty, Trails.length < trail.length).all()
    

    for i in range(5):
        trail_1 = random.choice(training_trails)
        training_trail = crud.create_training_trail(trail_1.trail_id, training_path.training_path_id)
        db.session.add(training_trail)
        db.session.commit()

    flash("Summit goal created!")
    return redirect("/account")
    
@app.route("/activity_log")
def activity_log():

    return render_template("activity_log.html")

@app.route("/trail_notes", methods=["POST"])
def make_trail_data():

    trail_notes = request.json.get("notes")
    miles_hiked = request.json.get("miles")
    hours_hiked = request.json.get("hours")
    
    user = crud.get_user_by_email(session["user_email"])
    # call crud.get_training
    training_path = crud.get_training_path_by_user_id(user.user_id)
    create_activity_log = crud.create_activity_log(mileage_log=miles_hiked, trail_notes=trail_notes, training_path_id=training_path.training_path_id)

    db.session.add(create_activity_log)
    db.session.commit()

    return {
        "message": "Your hike has been logged",
        "success": True
    }


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)