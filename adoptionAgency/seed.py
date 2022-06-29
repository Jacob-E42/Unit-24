from models import db, Pet
from app import app


db.drop_all()
db.create_all()

Pet.query.delete()

pet1 = Pet(name="wiggles", species="cat", photo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
 age=7, notes="wiggles is friendly", available=True)
pet2 = Pet(name="killdog", species="dog", age="30")
pet3 = Pet(name="snuggly", species="porcupine", available=False)



db.session.add(pet1)
db.session.add(pet2)
db.session.add(pet3)


db.session.commit()



