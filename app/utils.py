import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import random


tarot_url = "https://tarotcards-api-81f4cb400f3a.herokuapp.com/"


def get_random_tarot_card():
    response = requests.get(tarot_url)
    response.raise_for_status()
    tarot_data = response.json()
    return random.choice(tarot_data)

def send_daily_tarot_email(user, app):
    gmail_username = app.config['GMAIL_USERNAME']
    gmail_password = app.config['GMAIL_PASSWORD']

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

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            server.sendmail(sender_email, receiver_email, message.as_string())

        print(f"Email sent successfully to {user.name} ({user.email})")
    except smtplib.SMTPResponseException as e:
        print(f"SMTP Response Exception: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
