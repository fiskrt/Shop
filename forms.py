from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField



class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Sign up nibba')

class Admin(FlaskForm):
    #addbutton
    pass
