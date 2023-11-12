from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

from dotenv import load_dotenv
import os
from flask_migrate import Migrate
import secrets
import requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

load_dotenv()

app.config['GMAIL_USERNAME'] = os.getenv("GMAIL_USERNAME")
app.config['GMAIL_PASSWORD'] = os.getenv("GMAIL_PASSWORD")

scheduler = BackgroundScheduler()


from app import models, utils, routes


@scheduler.scheduled_job('cron', hour=10, minute=0)
# @scheduler.scheduled_job('interval', minutes=1)
def schedule_send_daily_tarot_email():
    try:
        with app.app_context():
            users = models.User.query.all()
            for user in users:
                utils.send_daily_tarot_email(user, app)
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")