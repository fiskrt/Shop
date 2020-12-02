from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, validators


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Log In')

class AdminAddProduct(FlaskForm):
    productID = StringField('Product ID')
    stock = IntegerField('Stock')
    description = StringField('Description')
    image = FileField('Image')
    price = IntegerField('Price')
    brand = StringField('Brand')
    submit = SubmitField('Add product')

class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max = 20)])
    email = StringField('Email', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', "Message do not match")
    ])
    confirm = PasswordField('Confirm Password')
    register = SubmitField('Register')

