from flask import Flask, request, url_for, render_template, session, redirect
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "vjhbgkyutgum"


@app.route('/homeC', methods=['POST','GET'])
def homeC():
    formHomeC=searchCategoryForm()
    return render_template('homeC.html', formHomeC=formHomeC)

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


if __name__ == '__main__':
    app.run(debug=True)
