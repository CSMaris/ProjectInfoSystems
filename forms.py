from flask_wtf import FlaskForm
from wtforms import SubmitField, validators,SelectField,StringField,PasswordField, TextAreaField
from wtforms.validators import DataRequired,Email,Length, InputRequired


class loginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password',validators= [InputRequired(), Length(min=8, max=20)])


class signupForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])

class searchCategoryForm(FlaskForm):
    Choices = [('1', 'cat1'),
                ('2', 'cat2'),
                ('3', 'cat3')]

    category = SelectField('Select category', choices=Choices ,validators=[InputRequired()])