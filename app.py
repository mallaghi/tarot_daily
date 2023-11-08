from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import random
import os
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)



tarot_url = "https://tarotcards-api-81f4cb400f3a.herokuapp.com/"

load_dotenv()

gmail_username = os.getenv("GMAIL_USERNAME")
gmail_password = os.getenv("GMAIL_PASSWORD")

def get_random_tarot_card():
    response = requests.get(tarot_url)
    response.raise_for_status()
    tarot_data = response.json()
    return random.choice(tarot_data)

def send_daily_tarot_email():
    try:
        with app.app_context():  # Use the app context
            # Get all users from the database
            users = User.query.all()

            for user in users:
                random_card = get_random_tarot_card()

                card_name = random_card.get("name")
                card_image_url = random_card.get("image")
                card_meaning = random_card.get("meaning")

                message_subject = f"{user.name}'s Tarot Card of the Day"
                message_body = f"Hey {user.name}, here is your daily Tarot card!\n\n"
                message_body += f"Card Name: {card_name}\n"

                message_body += f'<img src="{card_image_url}" alt="{card_name}">\n'

                message_body += f"Card Meaning: {card_meaning}"

                sender_email = gmail_username
                sender_password = gmail_password
                receiver_email = user.email

                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = receiver_email
                message['Subject'] = message_subject


                message.attach(MIMEText(message_body, 'plain'))

                # Connect to Gmail's SMTP server
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)

                    server.sendmail(sender_email, receiver_email, message.as_string())

                print(f"Email sent successfully to {user.name} ({user.email})")

    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")

scheduler = BlockingScheduler()

scheduler.add_job(send_daily_tarot_email, 'cron', hour=10, minute=0)


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')



        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':

    scheduler.start()
    app.run(debug=True)
