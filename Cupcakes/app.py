"""app for RESTful JSON api that supports CRUD operations for a list of cupcakes
"""

from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, Cupcake
from forms import CupcakeForm


from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Nope'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#connects db and creates all tables on the db server
connect_db(app)
db.create_all()


#No homepage, instead redirects to user list
@app.route('/')
def show_homepage():

    return render_template()




