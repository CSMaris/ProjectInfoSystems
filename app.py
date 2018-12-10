# -*- coding: utf-8 -*-
from flask import Flask, request, url_for, render_template, session, redirect
from forms import *
import os
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "vjhbgkyutgum"
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///DB.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

class Product(db.Model):
    __tablename__ = "Product"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=True)
    brand=db.Column(db.String(30),nullable=True)
    category=db.Column(db.String(30),nullable=True)
    supermarket=db.Column(db.Integer,nullable=True)
    supermarkets= db.relationship("Sells", back_populates="product")

    def __repr__(self):
        return "<Product %r>" % self.name

class Supermarket(db.Model):
    __tablename__ = "Supermarket"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=True)
    address= db.Column(db.String(40),nullable=True)
    city= db.Column(db.String(20),nullable=True)
    tel=db.Column(db.String,nullable=True)
    email=db.Column(db.String,nullable=True)
    products = db.relationship("Sells", back_populates="supermarket")

    def __repr__(self):
        return "<Supermarket %r>" % self.name

class Sells(db.Model):
    __tablename__="Sells"
    left_id=db.Column(db.Integer,db.ForeignKey("Products.id"), primary_key=True)
    right_id=db.Column(db.Integer,db.ForeignKey("Supermarkets.id"), primary_key=True)
    price= db.Column(db.Float, primary_key=True)
    product = db.relationship("Product", back_populates="supermarkets")
    supermarket = db.relationship("Supermarket", back_populates="products")

data=[('category1','cat1'),( 'category2','cat2'),( 'category3','cat3')]

@app.before_first_request
def setup_db():
    db.create_all()








@app.route('/homes',methods=['POST','GET'])
def homes():
    return render_template('homes.html')
@app.route('/newProduct',methods=['POST','GET'])
def newProduct():
    form= NewProductForm()
    #have to validate price input before submitting
    return render_template('newProduct.html',form=form)

@app.route('/product', methods=['POST','GET'])
def product():

    formQ=BuyForm()
    formC=CommentForm()

    if formQ.is_submitted() | formC.is_submitted():
      if request.form['which-form'] == 'formQ':
       if formQ.is_submitted():
         #update DB
         print("SUBMITTED Q")
         return render_template('productpage.html', markets=data, formQ=formQ, formC=formC)

      if request.form['which-form'] == 'formC':
         #update DB
         print("SUBMITTED C")
         return render_template('productpage.html', markets=data, formQ=formQ, formC=formC)

    return render_template('productpage.html', markets=data, formQ=formQ, formC=formC)


@app.route('/homec', methods=['POST','GET'])
def homec():
    formhomec=searchCategoryForm()
    formhomec.myChoices(data)
    return render_template('homec.html', formhomec=formhomec)

@app.route('/profile', methods=['POST','GET'])
def profile():
    form=ProfileForm()
    return render_template('profile.html', form=form)

@app.route('/loginPage', methods=['POST', 'GET'])
def log():
    form1=loginForm()
    if form1.validate_on_submit():
        return redirect(url_for('homec') )
    else:
        return render_template('login.html', form1=form1)

@app.route('/signupPage', methods=['POST','GET'])
def signup():
    form2 = signupForm()

    if form2.validate_on_submit():
        session['email2'] = form2.email.data
        session['password2'] = form2.password.data

    return render_template('signup.html', form2=form2 )

@app.route('/products',methods=['POST','GET'] )
def products():
 path='C:\Users\Stefan Maris\PycharmProjects\Project\static'
 list = os.listdir(path)
 images={}
 filterForm=FilterForm()


 for immagine in list:
     nome=immagine.replace('.jpg', '')
     images[nome]=(url_for('static', filename=immagine))

 del(images['style.css'])

 return render_template('productspage.html', immagini=images, filterForm=filterForm)


if __name__ == '__main__':
    app.run(debug=True)
