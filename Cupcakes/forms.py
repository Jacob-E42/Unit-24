from flask_wtf import FlaskForm
from wtforms import StringField, FloatField #etc ..................................

class CupcakeForm(FlaskForm):
    """Form for new Cupcakes"""

    name = StringField(" Name")


