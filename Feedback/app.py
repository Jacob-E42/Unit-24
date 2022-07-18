"""
"""

from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, AddFeedback, EditFeedback
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Nope'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


# connects db and creates all tables on the db server
connect_db(app)
db.create_all()


@app.route('/')
def show_homepage():
    """No homepage, redirects to register or user's page"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Show register form and update db and login upon submission"""

    # If user already exists and is logged in, they are redirected back to their page
    if "username" in session:
        return redirect(f"/users/{session['username']}")f

    form = RegisterForm()

    if form.validate_on_submit():
        # collects a list of all form values
        data = [v for k, v in form.data.items() if k != "csrf_token"]
        new_user = User.register(*data) #User class convenience method

        db.session.add(new_user)
        db.session.commit()

        #username is stored in session to validate in other routes that the user is logged in
        session["username"] = new_user.username
        flash("New User Created!", "success")
        return redirect(f"/users/{new_user.username}")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """"Login an existing user and redirect them to their home page"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data) #User class convenience method
        if user:
            session["username"] = user.username
            flash("You are now logged in!", "success")
            return redirect(f"/users/{user.username}")
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


@app.route("/users/<username>")
def display_user(username):
    """display a user's home page, with their basic info and display a list of all their feedback"""

    #if the user isn't logged in, or is accessing a different user's page, they are warned and told to login
    if "username" in session and username == session["username"]:
        user = User.query.get(username)
        return render_template("user.html", user=user)
    else:
        flash("You must be logged in, in order to view this", "danger")
        return redirect("/login")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """delete user and update db"""
    if "username" in session and username == session["username"]:

        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")
        flash("User has been deleted", "success")

        return redirect("/")
    else:
        flash("You must be logged in, in order to do this", "danger")
        return redirect("/login")


@app.route("/logout")
def logout():
    """User is logged out and the session data is updated"""

    session.pop("username")
    flash("You are now logged out", "success")
    return redirect("/login")


#----------------------------------------------------------------------------------------Feedback Routes

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """display form for logged-in user to add a new piece of feedback"""

    if "username" in session and username == session["username"]:

        form = AddFeedback()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_feedback = Feedback(
                title=title, content=content, username=username)

            db.session.add(new_feedback)
            db.session.commit()

            flash("New Feedback Added!", "success")
            return redirect(f"/users/{username}")
        else:
            return render_template("add_feedback.html", form=form)

    else:
        flash("You must be logged in, in order to do this", "danger")
        return redirect("/login")


@app.route("/feedback/<id>/update", methods=["GET", "POST"])
def update_feedback(id):
    """Update a user's feedback and update db. Both fields are optional."""

    feedback = Feedback.query.get(id)
    if "username" in session and feedback.username == session["username"]:
        form = EditFeedback()


        if form.validate_on_submit():
            feedback.title = form.title.data or feedback.title
            feedback.content = form.content.data or feedback.content
            db.session.add(feedback)
            db.session.commit()
            flash("Feedback updated!", "success")
            return redirect(f"/users/{feedback.username}")
        else:
            return render_template("update_feedback.html", form=form)
    else:
        flash("You must be logged in, in order to do this", "danger")
        return redirect("/login")


@app.route("/feedback/<id>/delete", methods=["POST", "GET"])
def delete_feedback(id):
    """Delete a piece of feedback"""
    
    feedback = Feedback.query.get(id)
    if "username" in session and feedback.username == session["username"]:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!", "secondary")
        return redirect(f"/users/{feedback.username}")
    else:
        flash("You must be logged in, in order to do this", "danger")
        return redirect("/login")
