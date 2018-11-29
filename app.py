from flask import Flask, request, url_for, render_template, session, redirect
from forms import *
import os
from flask_bootstrap import Bootstrap
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "vjhbgkyutgum"
Bootstrap(app)

data = [
    {
        'title': 'supermarket1',
        'content':'description'
    },
{
        'title': 'supermarket2',
        'content':'description'
    }

]

@app.route('/product', methods=['POST','GET'])
def product():
    return render_template('productpage.html', markets=data)


@app.route('/homec', methods=['POST','GET'])
def homec():
    formhomec=searchCategoryForm()
    return render_template('homec.html', formhomec=formhomec)

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
 for immagine in list:
     nome=immagine.replace('.jpg', '')
     images[nome]=(url_for('static', filename=immagine))

 del(images['style.css'])

 return render_template('productspage.html', immagini=images)


if __name__ == '__main__':
    app.run(debug=True)
