""""""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func



db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Pet(db.Model):

     
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

   

    def __repr__(self):
        p = self
        return f" {self.id} {p.name} {p.species} {p.age} {p.notes} {p.available} "   
    
    
     



   