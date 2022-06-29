from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, AnyOf

class NewPetForm(FlaskForm):
    """Form for creating a new pet """

    name = StringField("Pet Name", validators=[InputRequired()])
    species = SelectField("Species", choices=[("dog", "Dog"), ("cat", "Cat"), ("porc", "Porcupine")],  validators=[AnyOf(values=("dog", "cat", "porc"))])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[NumberRange(min=0, max=30), Optional()])
    notes = StringField("Notes")


class EditPetForm(FlaskForm):
    """Form for editing an existing pet"""

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = StringField("Notes")
    available = BooleanField("Available")