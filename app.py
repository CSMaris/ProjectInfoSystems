from flask import Flask, request, url_for, render_template, session, redirect
from forms import loginForm, signupForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "vjhbgkyutgum"


@app.route('/')
def hello_world():
    return render_template("homeC.html")

@app.route('/loginPage', methods=['POST', 'GET'])
def log():
    form1=loginForm()
    form2=signupForm()
    namePage1=""
    namePage2=""
    if form1.validate_on_submit():
        session['email1'] = form1.email.data
        session['password1'] = form1.password.data

    if form2.validate_on_submit():
        session['email2'] = form2.email.data
        session['password2'] = form2.password.data


    return render_template('login.html', form1=form1,form2=form2, namePage1=session.get('email1', False) )


if __name__ == '__main__':
    app.run(debug=True)
