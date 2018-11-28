from flask import Flask, request, url_for, render_template, session, redirect
from forms import *
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "vjhbgkyutgum"


@app.route('/homec', methods=['POST','GET'])
def homec():
    formhomec=searchCategoryForm()
    return render_template('homec.html', formhomec=formhomec)

@app.route('/loginPage', methods=['POST', 'GET'])
def log():
    form1=loginForm()
    namePage=""
    if form1.validate_on_submit():
        session['email1'] = form1.email.data
        session['password1'] = form1.password.data
    return render_template('login.html', form1=form1, namePage=session.get('email1', False) )

@app.route('/signupPage', methods=['POST','GET'])
def signup():
    form2 = signupForm()

    if form2.validate_on_submit():
        session['email2'] = form2.email.data
        session['password2'] = form2.password.data

    return render_template('signup.html', form2=form2 )

data = [
    {
        'title': 'product1',
        'content':'Please Use Python 2.7.15 for Windows10',
        'author': 'Mohammad',
        'date': '14 Nov 2018'
    },
{
        'title': 'Second Lesson',
        'content':'Please Use Python 2.7.15 for Windows10',
        'author': 'Mohammad',
        'date': '12 Nov 2018'
    },
{
        'title': 'Third Lesson',
        'content':'Please Use Python 2.7.15 for Windows10',
        'author': 'Mohammad',
        'date': '10 Nov 2018'
    }
]




@app.route('/',methods=['POST','GET'] )
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
