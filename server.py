from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, Trails
# from crud import get_trails, get_trail_by_id, get_users, create_user
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
    print(user)

    # get training path by user id
    # pass training path / summit goal to jinja template
    # might create crud function to crud.get_training_path_by_user_id()

    return render_template("user_details.html", user=user)


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
    




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)