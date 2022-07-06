"""app for RESTful JSON api that supports CRUD operations for a list of cupcakes
"""

from flask import Flask, request, redirect, render_template, session, flash, jsonify
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

# connects db and creates all tables on the db server
connect_db(app)
db.create_all()


@app.route('/')
def show_homepage():
    """Client side route that displays a static landing page."""

    # WTForm is used, which contains basic built-in validation
    form = CupcakeForm()
    return render_template("index.html", form=form)

#############################################################################################
# All routes below are api routes that respond with JSON


@app.route("/api/cupcakes", methods=["GET"])
def show_all_cupcakes():
    """Returns list of all cupcakes"""

    # All db cupcakes are queried and returned serialized so that they are JSON compatible
    cupcakes = [c.serialize() for c in Cupcake.query.all()]
    response = jsonify(cupcakes=cupcakes)
    return response


@app.route("/api/cupcakes/<int:id>")
def show_single_cupcake(id):
    """Returns a single specified cupcake, via id"""

    cupcake = Cupcake.query.get_or_404(id).serialize()
    return jsonify(cupcake=cupcake)


@app.route("/api/cupcakes", methods=["POST", "OPTIONS"])
def create_cupcake():
    """Posts a new cupcake to the db"""
    
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()
  
    response = jsonify(cupcake=new_cupcake.serialize())
    
    # Status code 201 is sent back for a POST Request
    return (response, 201)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Route updates the data of a single cupcake given its id. 

    All data attributes use a get method with a second parameter of the preexisting value so 
    that the attribute doesn't become null if the user didn't update that value"""

    c = Cupcake.query.get_or_404(id)
    c.flavor = request.json.get("flavor", c.flavor)
    c.size = request.json.get("size", c.size)
    c.rating = request.json.get("rating", c.rating)
    c.image = request.json.get("image", c.image)
    db.session.commit()

    return jsonify(cupcake=c.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Delete a single cupcake given its id."""

    c = Cupcake.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()

    return jsonify(message="deleted")
