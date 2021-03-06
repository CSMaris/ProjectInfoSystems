# -*- coding: utf-8 -*-
from __future__ import division
from flask import Flask, request, url_for, render_template, session, redirect
from forms import *
import os
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message



app = Flask(__name__)
app.config['SECRET_KEY'] = "vjhbgkyutgum"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///DATABASE.db'
app.config['MAIL_SERVER']='smtp.mail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_TLS']=True
app.config['MAIL_USERNAME']=os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD']=os.environ['MAIL_PASSWORD']

Bootstrap(app)
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
mailobject=Mail(app)


class Users(db.Model):
    __tablename__ = "Users"
    email=db.Column(db.String, primary_key=True)
    password=db.Column(db.String, nullable=True)
    city=db.Column(db.String, nullable=True)
    products=db.relationship("ConsumerProducts", back_populates="consumer")

class ConsumerProducts(db.Model):
    __tablename__= "ConsumerProducts"
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
    quality=db.Column(db.Float, nullable=True)
    qualityInt=db.Column(db.Integer, nullable=True)
    numberRatings=db.Column(db.Integer)
    image=db.Column(db.String)
    consumers=db.relationship("ConsumerProducts", back_populates="product")
    supermarkets= db.relationship("Sells", back_populates="product")
    comments = db.relationship('Comments', backref='product')
    def __repr__(self):
        return "<Product %r>" % self.name

class Comments(db.Model):
    __tablename__ = "Comments"
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.TEXT,nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))



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

cats=[('Pasta&Rice','Pasta&Rice'),('Fruits','Fruits'),( 'Cheese','Cheese'),( 'Biscuits','Biscuits'),('Crackes&Breadsticks','Crackers&Breadsticks'),
      ('Sweets','Sweets'),('Water','Water'),('Non-alcoholic drinks','Non-alcoholic drinks'),('Alcoholic drinks','Alcoholic drinks'),('Frozen food','Frozen food'),
      ('Yogurts%Milk','Yogurts&Milk'),('Meat&Fish','Meat&Fish'),('Chips','Chips'),('Seasoning','Seasoning'),('Pets food','Pets food')]
bs=[('Barilla','Barilla'), ('Martini', 'Martini'), ('Muller', 'Muller'), ('Guizza', 'Guizza'),('Chiquita','Chiquita'),('Fage','Fage'),('Buitoni','Buitoni'),('Knorr','Knorr'),('Fini','Fini'), ('Rana','Rana'),('Agnesi','Agnesi'),('Divella','Divella'),('Scotti','Scotti'),('Flora','Flora'),
    ('Galbani', 'Galbani'), ('Camemebert', 'Camembert'), ('Prealpi', 'Prealpi'), ('Biraghi', 'Biraghi'), ('Mulino bianco', 'Mulino bianco'),
    ('Colussi', 'Colussi'), ('Galbusera', 'Galbusera'), ('Gentilini', 'Gentilini'), ('Pavesi', 'Pavesi'),
    ('Balocco', 'Balocco'), ('Misura', 'Misura'), ('Saiwa', 'Saiwa'), ('Ferrero', 'Ferrero'), ('Nestle', 'Nestle'),
    ('Milka', 'Milka'), ('Lindt', 'Lindt'), ('Novi', 'Novi'), ('Cameo', 'Cameo'),
    ('Haribo', 'Haribo'), ('Dufour', 'Dufour'), ('Caffarel', 'Caffarel'), ('Levissima', 'Levissima'),
    ('Rocchetta', 'Rocchetta'), ('Vitasnella', 'Vitasnella'), ('CocaCola', 'CocaCola'), ('Lipton', 'Lipton'),
    ('Bravo', 'Bravo'), ('Santal', 'Santal'), ('Sanbitter', 'Sanbitter'), ('Baileys', 'Baileys'),
    ('Campari', 'Campari'), ('Bacardi', 'Bacardi'), ('Orogel', 'Orogel'), ('Findus', 'Findus'),
    ('Bonduelle', 'Bonduelle'), ('Activia', 'Activia'), ('Amadori', 'Amadori'), ('Simmenthal', 'Simmenthal'),
    ('RIO mare', 'RIO mare'), ('Pai', 'Pai'), ('San Carlo', 'San Carlo'), ('Pringles', 'Pringles'),
    ('Chipster', 'Chipster'), ('Carapelli', 'Carapelli'), ('Monini', 'Monini'), ('Cirio', 'Cirio'), ('Bertolli', 'Bertolli'),
    ('Ponti', 'Ponti'), ('Gourmet', 'Gourmet'), ('Felix', 'Felix'), ('Friskies', 'Friskies')]


@app.before_first_request
def setup_db():
    db.create_all()


def send_mail(to,subject,template,**kwargs):
    msg=Message(subject,recipients=[to],sender=app.config['MAIL_USERNAME'])
    msg.body= render_template(template + '.txt',**kwargs)
    msg.html= render_template(template + '.html',**kwargs)
    mailobject.send(msg)









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
                       qualityInt=0,
                       numberRatings=0,
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
    product=Products.query.get(p)

    comments=product.comments
    listComments=[]
    for c in comments:
        listComments.append(c.text)

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
         return render_template('productpage.html', formQ=formQ, formC=formC, sells=supermarketsSell, message="Added to your list", pid=p, comments=listComments)

      if request.form['which-form'] == 'formC':
          if formC.validate_on_submit():
              text=formC.comment.data

              rating=int(request.values.get('stars'))

              pid=session['selectedProduct']
              p=Products.query.get(pid)
              nold=p.numberRatings
              n=nold+1
              totalS=nold*p.quality
              p.numberRatings=n
              totalS=totalS+rating
              newQuality=totalS/n
              newQualityInt=int(newQuality +0.5)
              p.quality= newQuality
              p.qualityInt=newQualityInt
              c=Comments(text=text, product=p)
              db.session.commit()
              return render_template('productpage.html', formQ=formQ, formC=formC, sells=supermarketsSell, pid=pid, comments=listComments)

    return render_template('productpage.html', formQ=formQ, formC=formC, sells=supermarketsSell, pid=p, comments=listComments)

@app.route('/listC',methods=['POST', 'GET'])
def listC():
   list=[]
   cps=ConsumerProducts.query.filter_by(right_id=session['email'].upper()).all()
   totPrice=0
   for cp in cps:
       product=Products.query.get(cp.left_id)
       pid=product.id
       supermarket = Supermarkets.query.get(cp.smail)
       sell = Sells.query.filter_by(right_id=cp.smail).filter_by(left_id=cp.left_id).first()
       namep=product.name
       price=sell.price
       pricex=price*cp.number
       totPrice=totPrice+pricex
       names=supermarket.name
       address=supermarket.address
       number=cp.number

       list.append({'namep':namep, 'price':price, 'names':names, 'address':address, 'number':number, 'idp':pid})

   if 'Remove' in request.form:
        pid=request.values.get('product')
        cp=ConsumerProducts.query.filter_by(left_id=pid).filter_by(right_id=session['email'].upper()).first()
        db.session.delete(cp)
        db.session.commit()
        return redirect(url_for('listC'))

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
        sl=Sells.query.filter_by(left_id=pid).all() # check if that was the last supermarket selling the product
        if len(sl) == 0:
            p=Products.query.get(pid)
            path = 'C:\Users\Stefan Maris\PycharmProjects\Project' +p.image
            os.remove(path)
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



@app.route('/profile', methods=['POST','GET'])
def profile():
    smail=request.values.get('supermarket')
    s=Supermarkets.query.get(smail)
    data={'name':s.name, 'address':s.address, 'city':s.city, 'tel':s.tel, 'email':smail}

    return render_template('profile.html', data=data)

@app.route('/profileS',  methods=['POST','GET'])
def profileS():
    form=ProfileForm()
    if form.validate_on_submit():
        smail=session['email']
        supermarket=Supermarkets.query.get(smail.upper())
        supermarket.name=form.name.data
        supermarket.address = form.address.data
        supermarket.city = form.city.data
        supermarket.tel = form.tel.data
        db.session.commit()
        message="Profile updated"
        return render_template('profileS.html', form=form, message=message)

    return render_template('profileS.html', form=form)

@app.route('/homec', methods=['POST','GET'])
def homec():
    formhomec=searchCategoryForm()
    formhomec.myChoices(cats)
    if formhomec.validate_on_submit():
        session['category']=formhomec.category.data
        return redirect(url_for('products'))

    return render_template('homec.html', formhomec=formhomec)

@app.route('/products',methods=['POST','GET'] )
def products():
 flag=True
 list=[]
 mymail = session['email']
 me = Users.query.get(mymail.upper())
 city = me.city
 superCity = Supermarkets.query.filter_by(city=city).all()
 category = session['category']
 filterForm = FilterForm()
 filterForm.myBrands(bs)

 if request.method == 'POST':
    if 'formProduct' in request.form:
     session['selectedProduct']=request.values.get('hidden')
     return redirect(url_for('product'))
    elif filterForm.validate_on_submit():
        flag=False
        qual = int(filterForm.quality.data)
        brand = filterForm.brand.data
        if qual > 0 and brand != "NOFILTER":
            for s in superCity:
                sells = Sells.query.filter_by(right_id=s.email)
                for sell in sells:
                    prod = Products.query.get(sell.left_id)
                    if prod.category == category and prod not in list and prod.qualityInt == qual and prod.brand==brand:
                        list.append(prod)
        elif qual > 0:
            for s in superCity:
                sells = Sells.query.filter_by(right_id=s.email)
                for sell in sells:
                    prod = Products.query.get(sell.left_id)
                    if prod.category == category and prod not in list and prod.qualityInt== qual:
                        list.append(prod)
        elif brand != "NOFILTER":
            for s in superCity:
                sells = Sells.query.filter_by(right_id=s.email)
                for sell in sells:
                    prod = Products.query.get(sell.left_id)
                    if prod.category == category and prod not in list and prod.brand==brand:
                        list.append(prod)
        else:
            for s in superCity:
                sells = Sells.query.filter_by(right_id=s.email)
                for sell in sells:
                    prod = Products.query.get(sell.left_id)
                    if prod.category == category and prod not in list:
                        list.append(prod)

 if(flag):
     for s in superCity:
         sells=Sells.query.filter_by(right_id=s.email)
         for sell in sells:
             prod=Products.query.get(sell.left_id)
             if prod.category == category and prod not in list:
                 list.append(prod)
 products=[]
 for product in list:
     quality=0
     if product.qualityInt == 0:
         quality= 'NO REVIEWS'
     elif product.qualityInt ==1:
         quality=u'★'
     elif product.qualityInt ==2:
         quality=u'★★'
     elif product.qualityInt ==3:
         quality=u'★★★'
     elif product.qualityInt ==4:
         quality=u'★★★★'
     elif product.qualityInt ==5:
         quality=u'★★★★★'
     products.append({'name':product.name,'image':product.image,'brand':product.brand,'quality':quality, 'id':product.id})
 return render_template('productspage.html', products=products, filterForm=filterForm)


@app.route('/', methods=['POST', 'GET'])
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
                          password=password,
                          city=form2.city.data)
            db.session.add(reg)
            db.session.commit()
            send_mail(session['email'], 'Welcome', 'mail', message_body='Welcome mail')
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
                           city=form2.city.data.upper(),
                           tel=form2.tel.data,
                           address=form2.address.data )

        db.session.add(reg)
        db.session.commit()
        send_mail(session['email'], 'Welcome', 'mail', message_body='Welcome mail')
        return redirect(url_for('homes'))

    return render_template('signupS.html', form2=form2, message=message)


if __name__ == '__main__':
    app.run(debug=True)
