from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, validators, SelectField


class CommentForm(FlaskForm):
    comment = StringField('Write comment here', [validators.DataRequired()])
    rating = SelectField(choices = ['1','2','3','4','5'])
    submit = SubmitField('Post')

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=1, max = 21)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Log In')

class AdminAddProduct(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    price = IntegerField('Price', [validators.DataRequired()])
    description = StringField('Description', [validators.DataRequired()])
    image = FileField('Image', [validators.DataRequired()])
    brand = StringField('Brand', [validators.DataRequired()])
    submit = SubmitField('Add product')

class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max = 20)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', "Message do not match")
    ])
    confirm = PasswordField('Confirm Password')
    register = SubmitField('Register')

