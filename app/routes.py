from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User
from app.utils import send_daily_tarot_email
from sqlalchemy.exc import IntegrityError

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        user = User(name=name, email=email)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Signed up successfully!', 'success')

            send_daily_tarot_email(user, app)

            return redirect(url_for('confirmation'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Email already registered. Please use a different email.', 'error')

    return redirect(url_for('index'))

@app.route('/unsubscribe/<email>')
def unsubscribe(email):
    user = User.query.filter_by(email=email).first()

    if user:
        user.subscribed = False
        db.session.commit()
        return render_template('unsubscribed.html', user=user)
    else:
        return render_template('unsubscribe_error.html')
