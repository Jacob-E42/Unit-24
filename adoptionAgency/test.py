from flask import Flask, request, redirect, render_template, session, flash
from models import db, Pet
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from unittest import TestCase
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_pets' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()




class FlaskTests(TestCase):

    def setUp(self):
        
        pet = Pet(name="henry", species="dog", age=7, notes="he is chill")
        db.session.add(pet)
        db.session.commit()
        
        
  
        
       
    def tearDown(self):
        pet = db.session.query(Pet).first()
        
        db.session.delete(pet)
     
        db.session.commit()
       
        db.session.rollback()
        
        

    def test_homepage(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add a New Pet', html)

    def test_create_pet_form(self):
        with app.test_client() as client:
            resp = client.get("/add")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Photo URL', html)
    def test_post_new_pet(self):
        with app.test_client() as client:
            pet = Pet.query.first()
            d= {'name': pet.name, 'species': pet.species, "age": pet.age}
            resp = client.post("/add", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("henry", html)

    def test_edit_pet(self):
        with app.test_client() as client:
            pet = Pet.query.first()
            resp = client.get(f"/{pet.id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Pet Details', html)
   
            
    


