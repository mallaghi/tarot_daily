import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import requests
import random


tarot_url = "https://tarotcards-api-81f4cb400f3a.herokuapp.com/"

user_agent = "DailyTarotApp/1.0"

def get_random_tarot_card():
    headers = {"User-Agent": user_agent}
    response = requests.get(tarot_url, headers=headers)
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

    unsubscribe_link = f"{app.config['BASE_URL']}/unsubscribe/{user.email}"
    unsubscribe_message = f"<p>If you no longer wish to receive daily Tarot cards, you can unsubscribe here: {unsubscribe_link}</p>"

    message_subject = f"{user.name}'s Tarot Card of the Day"
    message_body = f"<p> Hey {user.name}, here is your daily Tarot card!</p>"
    message_body += f"<p>Card: {card_name}\n</p>"


    image_response = requests.get(card_image_url)
    image_data = image_response.content
    image = MIMEImage(image_data, name=f"{card_name}.jpg", _subtype='jpg')
    image.add_header('Content-ID', '<card_image>')
    message_body += f'<img src="cid:card_image" alt="{card_name}">\n'

    message_body += f"<p>Card Meaning: {card_meaning}</p>"

    message_body += unsubscribe_message

    sender_email = gmail_username
    sender_password = gmail_password
    receiver_email = user.email

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = message_subject

    message.attach(MIMEText(message_body, 'html'))
    message.attach(image)

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

