from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, EmailField
from wtforms.validators import InputRequired,  Email, Length

class RegisterForm(FlaskForm):
    """Form for registering a new user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=60)])
    email = EmailField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Login in a preexisting user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=60)])

class AddFeedback(FlaskForm):
    """Add feedback to site"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])

class EditFeedback(FlaskForm):
    """Add feedback to site"""

    title = StringField("Title", validators=[ Length(max=100)])
    content = StringField("Content")



