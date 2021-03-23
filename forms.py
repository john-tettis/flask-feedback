from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email
import email_validator



class RegisterUser(FlaskForm):
    username = StringField('Username', [InputRequired(message = 'Username is required.')])

    password = PasswordField('Password', [InputRequired(message = 'Please enter a password.')])
    
    email = StringField('Email', [Email(message = 'Please use a valid email'), InputRequired()])

    first_name = StringField('First Name', [InputRequired(message='First and last name are required')])

    last_name = StringField('Last Name',[InputRequired(message='First and last name are required')])

class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired(message = 'Username is required.')])

    password = PasswordField('Password', [InputRequired(message = 'Please enter a password.')])
