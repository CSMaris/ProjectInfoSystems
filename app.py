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
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///dataaa.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)


class Users(db.Model):
    __tablename__ = "Users"
    email=db.Column(db.String, primary_key=True)
    password=db.Column(db.String, nullable=True)
    products=db.relationship("ConsumerProducts", back_populates="consumer")

class ConsumerProducts(db.Model):
    __tablename__="ConsumerProducts"
    id=db.Column(db.Integer, primary_key=True)
    left_id=db.Column(db.Integer,db.ForeignKey("Products.id"))
    right_id=db.Column(db.String,db.ForeignKey("Users.email"))
    number= db.Column(db.Integer)
    smail=db.Column(db.String(30))
    product = db.relationship("Products", back_populates="consumers")
    consumer = db.relationship("Users", back_populates="products")


class Products(db.Model):
    __tablename__ = "Products"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=True)
    brand=db.Column(db.String(30),nullable=True)
    category=db.Column(db.String(30),nullable=True)
    quality=db.Column(db.Integer, nullable=True)
    image=db.Column(db.String)
    consumers=db.relationship("ConsumerProducts", back_populates="product")
    supermarkets= db.relationship("Sells", back_populates="product")
    def __repr__(self):
        return "<Product %r>" % self.name

class Supermarkets(db.Model):
    __tablename__ = "Supermarkets"
    email = db.Column(db.String,primary_key= True )
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
    id=db.Column(db.Integer, primary_key=True)
    left_id=db.Column(db.Integer,db.ForeignKey("Products.id"))
    right_id=db.Column(db.String,db.ForeignKey("Supermarkets.email"))
    price= db.Column(db.Float)
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
    message=''

    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        form.image.data.save('static/' + filename)
        flag = True
        products = Products.query.all()
        for product in products:
            if product.name == form.name.data:
                flag=False
                break
        if flag:
         newP=Products(name=form.name.data,
                      brand=form.brand.data,
                      category=form.category.data,
                      quality=0,
                      image=url_for('static',filename=filename))
         db.session.add(newP)
         s = Sells(price=form.price.data)
         s.supermarket = Supermarkets.query.get(session['email'].upper())
         newP.supermarkets.append(s)
         message = 'Product successfully added'

        else:


         productS = Sells.query.filter_by(right_id=session['email'].upper()).all()
         prodotti=Products.query.filter_by(name=form.name.data).all()
         flag2=True
         id=''
         for product in prodotti:
           if product.name == form.name.data:
               id=product.id



         for product in productS:
            if Products.query.get(product.left_id).name == form.name.data:
                flag2=False
                break





         if(flag2):
             s = Sells(price=form.price.data)
             s.supermarket = Supermarkets.query.get(session['email'].upper())
             Products.query.get(id).supermarkets.append(s)
             message = 'Product successfully added'
         else:
             message='You\'ve already uploaded this product'


    db.session.commit()



    return render_template('newProduct.html',form=form, message=message)

@app.route('/product', methods=['POST','GET'])
def product():

    formQ=BuyForm()
    formC=CommentForm()
    p=session['selectedProduct']
    sells=Sells.query.filter_by(left_id=p).all()
    supermarketsSell=[]
    for s in sells:
        supermarketMail=s.right_id
        supermarket=Supermarkets.query.get(supermarketMail)
        supermarketsSell.append({'name':supermarket.name, 'address':supermarket.address, 'price':s.price, 'productid':p, 'smail':supermarket.email})




    if formQ.is_submitted() | formC.is_submitted():
      if request.form['which-form'] == 'formQ':
       if formQ.validate_on_submit():
         #update DB
         cp = ConsumerProducts(number=formQ.quantity.data,smail=request.values.get('smail'))
         cp.consumer = Users.query.get(session['email'].upper())
         p=Products.query.get(request.values.get('productid'))
         p.consumers.append(cp)
         db.session.commit()
         return render_template('productpage.html', formQ=formQ, formC=formC, sells=supermarketsSell, message="Added to your list")

      if request.form['which-form'] == 'formC':
         #update DB
         print("SUBMITTED C")
         return render_template('productpage.html', markets=cats, formQ=formQ, formC=formC)

    return render_template('productpage.html', formQ=formQ, formC=formC, sells=supermarketsSell)

@app.route('/listC',methods=['POST', 'GET'])
def listC():
   list=[]
   cps=ConsumerProducts.query.filter_by(right_id=session['email'].upper()).all()
   totPrice=0
   for cp in cps:
       product=Products.query.get(cp.left_id)
       supermarket = Supermarkets.query.get(cp.smail)
       sell = Sells.query.filter_by(right_id=cp.smail).filter_by(left_id=cp.left_id).first()
       namep=product.name
       price=sell.price
       pricex=price*cp.number
       totPrice=totPrice+pricex
       names=supermarket.name
       address=supermarket.address
       number=cp.number


       list.append({'namep':namep, 'price':price, 'names':names, 'address':address, 'number':number})

   return render_template('listC.html', list=list, totPrice=totPrice)

@app.route('/listS', methods=['POST', 'GET'])
def listS():
    list=[]
    priceForm=changePrice()
    sells=Sells.query.filter_by(right_id=session['email'].upper()).all()
    for s in sells:
        product=Products.query.get(s.left_id)
        idp=product.id
        namep=product.name
        brand=product.brand
        price=s.price
        list.append({'namep':namep,'brand':brand, 'price':price, 'idp':idp })

    if 'Remove' in request.form:
        pid=request.values.get('product')
        s=Sells.query.filter_by(left_id=pid).filter_by(right_id=session['email'].upper()).first()
        db.session.delete(s)
        db.session.commit()
        # check if that was the last supermarket selling the product
        sl=Sells.query.filter_by(left_id=pid).all()

        if len(sl) == 0:
            p=Products.query.get(pid)
            db.session.delete(p)
            db.session.commit()

        return redirect(url_for('listS'))
    if priceForm.validate_on_submit():
        pid = request.values.get('product')
        s = Sells.query.filter_by(left_id=pid).filter_by(right_id=session['email'].upper()).first()
        s.price=priceForm.price.data
        db.session.commit()
        return redirect(url_for('listS'))


    return render_template('listS.html', list=list, priceForm=priceForm)


@app.route('/homec', methods=['POST','GET'])
def homec():
    formhomec=searchCategoryForm()
    formhomec.myChoices(cats)
    if formhomec.validate_on_submit():
        session['category']=formhomec.category.data
        return redirect(url_for('products'))

    return render_template('homec.html', formhomec=formhomec)

@app.route('/profile', methods=['POST','GET'])
def profile():
    form=ProfileForm()
    return render_template('profile.html', form=form)




@app.route('/products',methods=['POST','GET'] )
def products():
 if request.method == 'POST':
     session['selectedProduct']=request.values.get('hidden')
     return redirect(url_for('product'))


 category=session['category']
 #path='C:\Users\Stefan Maris\PycharmProjects\Project\static'
 #list = os.listdir(path)


 products=[]
 filterForm=FilterForm()
 list=Products.query.filter_by(category=category).all()
 for product in list:
     quality=0
     if product.quality == 0:
         quality= 'NO REVIEWS'
     if product.quality == 1:
         quality=u'★'
     if product.quality == 2:
         quality=u'★★'
     if product.quality == 3:
         quality=u'★★★'
     if product.quality == 4:
         quality=u'★★★★'
     if product.quality == 5:
         quality=u'★★★★★'

     products.append({'name':product.name,'image':product.image,'brand':product.brand,'quality':quality, 'id':product.id})


 #for immagine in list:
    # nome=immagine.replace('.jpg', '')
     #images[nome]=(url_for('static', filename=immagine))

 #del(images['style.css'])

 return render_template('productspage.html', products=products, filterForm=filterForm)

@app.route('/loginPage', methods=['POST', 'GET'])
def log():
    form1=loginForm()
    message=''
    if form1.validate_on_submit():
        pass_check = bcrypt.generate_password_hash(form1.password.data).decode('utf-8')
        user=Users.query.filter_by(email=form1.email.data.upper()).first()
        supermarket=Supermarkets.query.filter_by(email=form1.email.data.upper()).first()
        if user and bcrypt.check_password_hash(user.password,form1.password.data):
           session['email'] = form1.email.data
           session['password'] = form1.password.data
           return redirect(url_for('homec') )
        elif supermarket and bcrypt.check_password_hash(supermarket.password,form1.password.data):
            session['email'] = form1.email.data
            session['password'] = form1.password.data
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
            session['email'] = form2.email.data
            session['password'] = form2.password.data
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
        session['email'] = form2.email.data
        session['password'] = form2.password.data

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









if __name__ == '__main__':
    app.run(debug=True)
