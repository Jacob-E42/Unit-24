from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Optional, URL


class CupcakeForm(FlaskForm):
    """Form for new Cupcakes"""

    flavor = StringField("Flavor", validators=[InputRequired()])
    size = StringField("Size", validators=[InputRequired()])
    rating = FloatField("Rating", validators=[InputRequired()])
    image = StringField("Image_URL", validators=[Optional(), URL()])
