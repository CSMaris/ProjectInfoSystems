# -*- coding: utf-8 -*-
from flask import Flask, request, url_for, render_template, session, redirect
from forms import *
import os
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = "vjhbgkyutgum"
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///NEWDB.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)


class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String, nullable=True,unique=True)
    password=db.Column(db.String, nullable=True)


class Products(db.Model):
    __tablename__ = "Products"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=True)
    brand=db.Column(db.String(30),nullable=True)
    category=db.Column(db.String(30),nullable=True)
    quality=db.Column(db.Integer, nullable=True)
    image=db.Column(db.String)
    supermarkets= db.relationship("Sells", back_populates="product")

    def __repr__(self):
        return "<Product %r>" % self.name

class Supermarkets(db.Model):
    __tablename__ = "Supermarkets"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String,nullable=True,unique=True )
    name=db.Column(db.String(20),nullable=True)
    address= db.Column(db.String(40),nullable=True)
    city= db.Column(db.String(20),nullable=True)
    tel=db.Column(db.String,nullable=True, unique=True)
    products = db.relationship("Sells", back_populates="supermarket")
    password = db.Column(db.String(20), nullable=True)


    def __repr__(self):
        return "<Supermarket %r>" % self.name

class Sells(db.Model):
    __tablename__="Sells"
    left_id=db.Column(db.Integer,db.ForeignKey("Products.id"), primary_key=True)
    right_id=db.Column(db.Integer,db.ForeignKey("Supermarkets.id"), primary_key=True)
    price= db.Column(db.Float, primary_key=True)
    product = db.relationship("Products", back_populates="supermarkets")
    supermarket = db.relationship("Supermarkets", back_populates="products")

cats=[('category1','cat1'),( 'category2','cat2'),( 'category3','cat3')]
bs=[('brand1','Barilla'),( 'brand2','Ferrero'),( 'brand3','Nestle')]


@app.before_first_request
def setup_db():
    db.create_all()



















@app.route('/homes',methods=['POST','GET'])
def homes():
    return render_template('homes.html')
@app.route('/newProduct',methods=['POST','GET'])
def newProduct():
    form= NewProductForm()
    form.myValues(cats,bs)
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('static/' + filename)
        newP=Products(name=form.name.data,
                      brand=form.brand.data,
                      category=form.category.data,
                      quality=0,
                      image=url_for('static',filename=filename))
        db.session.add(newP)
        db.session.commit()


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
         return render_template('productpage.html', markets=cats, formQ=formQ, formC=formC)

      if request.form['which-form'] == 'formC':
         #update DB
         print("SUBMITTED C")
         return render_template('productpage.html', markets=cats, formQ=formQ, formC=formC)

    return render_template('productpage.html', markets=cats, formQ=formQ, formC=formC)


@app.route('/homec', methods=['POST','GET'])
def homec():
    formhomec=searchCategoryForm()
    formhomec.myChoices(cats)
    return render_template('homec.html', formhomec=formhomec)

@app.route('/profile', methods=['POST','GET'])
def profile():
    form=ProfileForm()
    return render_template('profile.html', form=form)

@app.route('/loginPage', methods=['POST', 'GET'])
def log():
    form1=loginForm()
    message=''
    if form1.validate_on_submit():
        pass_check = bcrypt.generate_password_hash(form1.password.data).decode('utf-8')
        user=Users.query.filter_by(email=form1.email.data.upper()).first()
        supermarket=Supermarkets.query.filter_by(email=form1.email.data.upper()).first()
        if user and bcrypt.check_password_hash(user.password,form1.password.data):
           return redirect(url_for('homec') )
        elif supermarket and bcrypt.check_password_hash(supermarket.password,form1.password.data):
            return redirect(url_for('homes') )
        else:
           message='INCORRECT CREDENTIALS'

    return render_template('login.html', form1=form1, message=message)

@app.route('/signupPageC', methods=['POST','GET'])
def signupc():
    form2 = signupFormC()
    message=''

    if form2.validate_on_submit():
        if Users.query.filter_by(email=form2.email.data.upper()).first() or Supermarkets.query.filter_by(email=form2.email.data.upper()).first():
            message="Already existing email"
        else:
            session['email2'] = form2.email.data
            session['password2'] = form2.password.data
            password = bcrypt.generate_password_hash(form2.password.data)
            reg = Users(  email=form2.email.data.upper(),
                          password=password )
            db.session.add(reg)
            db.session.commit()
            return redirect(url_for('homec'))

    return render_template('signupC.html', form2=form2, message=message)

@app.route('/signupPageS', methods=['POST','GET'])
def signups():
    form2 = signupFormS()
    message=''

    if form2.validate_on_submit():
      if Supermarkets.query.filter_by(email=form2.email.data.upper()).first() or Supermarkets.query.filter_by(tel=form2.tel.data).first() or Users.query.filter_by(email=form2.email.data.upper()).first() :
          message = "Already existing email or telephone number"
      else:
        session['email2'] = form2.email.data
        session['password2'] = form2.password.data

        password = bcrypt.generate_password_hash(form2.password.data)
        reg = Supermarkets(email=form2.email.data.upper(),
                           password=password,
                           name=form2.name.data,
                           city=form2.city.data,
                           tel=form2.tel.data,
                           address=form2.address.data )

        db.session.add(reg)
        db.session.commit()
        return redirect(url_for('homes'))

    return render_template('signupS.html', form2=form2, message=message)


@app.route('/products',methods=['POST','GET'] )
def products():
 #path='C:\Users\Stefan Maris\PycharmProjects\Project\static'
 #list = os.listdir(path)
 images={}
 filterForm=FilterForm()
 list=Products.query.all()
 for product in list:
     images[product.name]=product.image


 #for immagine in list:
    # nome=immagine.replace('.jpg', '')
     #images[nome]=(url_for('static', filename=immagine))

 #del(images['style.css'])

 return render_template('productspage.html', products=images, filterForm=filterForm)


if __name__ == '__main__':
    app.run(debug=True)
