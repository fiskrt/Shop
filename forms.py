from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField



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

