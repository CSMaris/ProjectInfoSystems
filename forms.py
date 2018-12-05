from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired,Email,Length, InputRequired


class loginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password',validators= [InputRequired(), Length(min=8, max=20)])


class signupForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])

class searchCategoryForm(FlaskForm):
    Choices = []

    category = SelectField('Select category', choices=Choices ,validators=[InputRequired()])

    def myChoices(self,var1):
        newC=[]
        for x in var1:
           newC.append(x)
        self.category.choices=newC



class BuyForm(FlaskForm):
    quantities=[('1','1'),
                ('2', '2'),
                ('3', '3')]

    quantity=SelectField('How many?',choices=quantities,validators=[InputRequired()])

class CommentForm(FlaskForm):
    comment=TextAreaField('Write here your comment...')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    address = StringField('Address',validators=[InputRequired()])
    city = StringField('City',validators=[InputRequired()])
