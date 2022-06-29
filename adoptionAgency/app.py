"""Website for a Pet Adoption Agency
"""

from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, Pet
from forms import NewPetForm, EditPetForm


from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Nope'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#connects db and creates all tables on the db server
connect_db(app)
db.create_all()

#########################################################################################################################3

@app.route('/')
def show_homepage():
    """Show a list of all pets and whether they are available for adoption or not"""
    pets = Pet.query.all()
    return render_template("index.html", pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def create_pet():
    """Show a form for adding a new pet to the site. Post route for adding to db."""
    form = NewPetForm()

    if form.validate_on_submit():
       

        data = {k:v for k,v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("create_pet.html", form=form)

@app.route('/<int:petid>', methods=['GET', 'POST'] )
def show_pet_details(petid):
    """Show details for a pet, and a form for editing the info for that pet."""
    
    pet = Pet.query.get_or_404(petid)
    form = EditPetForm(obj=pet)
    

    if form.validate_on_submit():
        
        photo_url = form.photo_url.data
        notes = form.notes.data
        available = form.available.data
    
        pet.photo_url = photo_url
        pet.notes = notes
        pet.available = available
        db.session.add(pet)
        db.session.commit()
        
        return redirect("/")
    else:
  
        return render_template("pet_details.html", pet=pet, form=form)








