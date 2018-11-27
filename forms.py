from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


class loginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators= [DataRequired(), Length(min=8, max=20)])
    submit=SubmitField('Log in')


class signupForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Sign up')

class searchCategoryForm(FlaskForm):
    Choices = [('1', 'cat1'),
                ('2', 'cat2'),
                ('3', 'cat3')]
    category = SelectField('Select category', choices=[Choices],validators=[DataRequired()])
    submit = SubmitField('Search')