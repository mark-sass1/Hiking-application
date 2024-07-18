from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from crud import get_trails, get_trail_by_id, get_users, create_user


app = Flask(__name__)
@app.route("/")
def homepage():
    """Homepage"""
    return render_template("homepage.html")


@app.route("/trails")
def all_trails():
    """View all trails."""

    trails = get_trails()

    return render_template("trails_route.html", trails=trails)



@app.route("/trails/<trail_id>")
def get_trail(trail_id):
    """Show details on a particular trail."""

    trail = get_trail_by_id(trail_id)

    return render_template("trail_details.html", trail=trail)


@app.route("/register", methods=["POST"])
def create_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")

        """Account created, and logged in"""
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
    
    
    
    return redirect("/user_account")
    


@app.route("/users")
def get_users():
    """View all users."""

    users = get_users(users)

    return render_template("users.html", users=users)
                




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)