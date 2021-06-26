import hashlib
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from workshop import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///countries.sqlite3'

db = SQLAlchemy(app)
app.secret_key = 'blabla'


class User(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['search']
        name = main(city)
        return render_template('index.html', **locals())
    else:
        return render_template('index.html', **locals())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session['logged']:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            username = request.form['uname']
            password = request.form['psw']
            checkUser = User.query.filter_by(username=username).count()

            if checkUser == 0:
                flash("check username")
                return redirect(url_for('login'))

            else:
                user = User.query.filter_by(username=username).first()
                userPassword = user.password
                hashedPassword = hashlib.md5(password.encode('utf8')).hexdigest()
                if hashedPassword == userPassword:
                    session['logged'] = True
                    session['user_id'] = user._id
                    session['username'] = user.username
                    return redirect(url_for('index'))

                else:
                    flash("username or password is not correct!")
                    return redirect(url_for('login'))
        else:
            return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session['logged']:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['psw']
            username = request.form['uname']
            checkUser = User.query.filter_by(username=username).count()
            if checkUser == 0:
                hashedPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
                user = User(name=name, username=username, email=email, password=hashedPassword)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash('user already exists')
                return redirect(url_for('signup'))
        else:
            return render_template('signup.html')


@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/lgt')
def lgt():
    session.pop("user_id", None)
    session.pop("username", None)
    session['logged'] = False
    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
