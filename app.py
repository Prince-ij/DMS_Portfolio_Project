#!/usr/bin/python3
from flask import Flask, render_template, url_for, redirect, flash
from flask import request
from forms import RegistrationForm, LoginForm
from models import User, Debtor, db
from flask_bcrypt import Bcrypt, check_password_hash

bcrypt = Bcrypt()

app = Flask('__name__')
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        confirm_pasword = request.form['confirm_password']

        # check if passwords match
        if password != confirm_password:
            flash('passwords do not match, please try again.', 'error')
            return redirect(url_for('register'))

        # check if email is unique
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already exists. please use a a different one',
                  'error')
            return redirect(url_for('register'))
        # hash password before storage
        hashed_password = (bcrypt.generate_password_hash(password).
                           decode('utf-8'))
        # create a new user object and add to Database
        new_user = User(email=email, password=hashed_password,
                        first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()

        flash('User registered Successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid email or password, try again!', 'error')
            return redirect(url_for('login'))

        # check if provided password is correct

        if not check_password_hash(user.password, password):
            flash('Invalid email or password, try again', 'error')
            return redirect(url_for('login'))

        # login successful

        flash('Login Successful!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    debtors = Debtor.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', debtors=debtors)

@app.route('/settle_debt/<int:debtor_id>', methods=['POST'])
def settle_debt(debtor_id):
    if request.method == 'POST':
        debtor = Debtor.query.get_or_404(debtor_id)
        settled_on = request.form['settled_on']
        debtor.settled_on = settled_on
        db.session.commit()
        flash('Debt Settled Successfully!', 'success')
        return redirect(url_for('dashboard'))

@app.route('/add_debtor', methods=['GET', 'POST'])
def add_debtor():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        purchase = request.form['purchase']
        quantity = request.form['quantity']
        amount = request.form['amount']
        date = request.form['collected_on']

        debtor = Debtor(first_name=first_name, last_name=last_name,
                        purchase=purchase, amount=amount,
                        collected_on = date)
        db.session.add(debtor)
        db.session.commit()
        flash('Debtor added successfully!', 'success')
        return redirect(url_for('dashbaord'))
    return render_template('add_debtor.html')

@app.route('/history')
def history():
    settled_debts = Debtor.query.filter(Debtor.settled_on.isnot(None)
                    ).all()
    return render_template('history.html', settled_debts=settled_debts)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    settled_debts = Debtor.query.filter(Debtor.settled_on.isnot (None)
                    ).all()
    for debtor in settled_debts:
        db.session.delete(debtor)
    db.session.commit()
    flash('Settled debts history cleared successfully!', 'success')
    return redirect(url_for('history'))


if __name__ == '__main__':
    app.run()
