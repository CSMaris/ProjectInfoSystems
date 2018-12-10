# -*- coding: utf-8 -*-
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms.fields.html5 import *
import re


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
    tel=TelField('Tel',validators=[TelField])
    email=StringField('Email', validators=[InputRequired(), Email()])

class FilterForm(FlaskForm):
    qualities=[('0','NOFILTER'),('1',u'★'),('2',u'★★'),('3',u'★★★'),('4',u'★★★★'),('5',u'★★★★★')]
    quality= SelectField('Filter by quality',choices=qualities)
    brands=[('0','NOFILTER'),('1','brand1'),('2','brand2')]
    brand=SelectField('Filter by brand',choices=brands)

class NewProductForm(FlaskForm):
    brands = [ ('1', 'brand1'), ('2', 'brand2')]
    categories = [('category1', 'cat1'), ('category2', 'cat2'), ('category3', 'cat3')]

    name=StringField('Name', validators=[InputRequired()])
    brand=SelectField('Choose the brand of the product',choices=brands,validators=[InputRequired()])
    category= SelectField('Choose the category of the product',choices=categories, validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    image = FileField('Insert an image of the product', validators=[InputRequired()])

    def validate_price(form, field):
        if not re.search('^[0-9]+,[0-9]{0,2}$', form.field.data):
            raise ValidationError('Invalid input syntax')
        form.euros = int(form.data.split(',')[0])
        form.cents = int(form.data.split(',')[1])