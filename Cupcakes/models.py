"""models app for cupcakes"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func



db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Cupcake(db.Model):

     
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

   

    def __repr__(self):
        
        return f" {self.id} "
    
    
    
     



   