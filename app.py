from flask import Flask, request, url_for, render_template, session, redirect
from forms import loginForm, signupForm

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("layout.html")

@app.route('/loginPage')
def log():
    form1=loginForm()
    form2=signupForm()
    #if form1.validate_on_submit():

    #elif form2.validate_on_submit():



    return "YOU LOGGED"


if __name__ == '__main__':
    app.run(debug=True)
