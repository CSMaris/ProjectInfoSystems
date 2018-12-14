# -*- coding: utf-8 -*-
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms.fields.html5 import *
from wtforms.widgets import html5
import re


class loginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password',validators= [InputRequired(), Length(min=8, max=20)])


class signupFormC(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])

class signupFormS(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    name = StringField('Name', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    tel = TelField('Tel', validators=[TelField])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])



class searchCategoryForm(FlaskForm):
    Choices = []

    category = SelectField('Select category', choices=Choices ,validators=[InputRequired()])

    def myChoices(self,var1):
        newC=[]
        for x in var1:
           newC.append(x)
        self.category.choices=newC

class changePrice(FlaskForm):
    price = StringField('New price', validators=[InputRequired()])

    def validate_price(form, price):
        if not re.search('^[0-9]+\.[0-9]{0,2}$', form.price.data):
            raise ValidationError('Invalid input syntax')
        form.euros = int(form.price.data.split('.')[0])
        form.cents = int(form.price.data.split('.')[1])


class BuyForm(FlaskForm):
    quantities=[('1','1'),
                ('2', '2'),
                ('3', '3')]

    quantity=IntegerRangeField('How many?',widget=html5.NumberInput(), validators=[NumberRange(min=1)])


class CommentForm(FlaskForm):
    comment=TextAreaField('Write here your comment...', validators=[InputRequired()])

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    address = StringField('Address',validators=[InputRequired()])
    city = StringField('City',validators=[InputRequired()])
    tel=TelField('Tel',validators=[TelField])
    email=StringField('Email', validators=[InputRequired(), Email()])

class FilterForm(FlaskForm):
    qualities=[('0','NOFILTER'),('1',u'★'),('2',u'★★'),('3',u'★★★'),('4',u'★★★★'),('5',u'★★★★★')]
    quality= SelectField('Filter by quality',choices=qualities)
    brands=[('NOFILTER','NOFILTER'),('brand1','brand1'),('brand2','brand2')]
    brand=SelectField('Filter by brand',choices=brands)

class NewProductForm(FlaskForm):
    name=StringField('Name', validators=[InputRequired()])
    brand=SelectField('Choose the brand of the product',choices=[],validators=[InputRequired()])
    category= SelectField('Choose the category of the product',choices=[], validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    image = FileField('Insert an image of the product')

    def validate_price(form, price):
        if not re.search('^[0-9]+\.[0-9]{0,2}$', form.price.data):
            raise ValidationError('Invalid input syntax')
        form.euros = int(form.price.data.split('.')[0])
        form.cents = int(form.price.data.split('.')[1])

    def myValues(self,cats, bs):
        C=[]
        B=[]
        for x in cats:
           C.append(x)
        self.category.choices=C

        for y in bs:
            B.append(y)
        self.brand.choices=B

