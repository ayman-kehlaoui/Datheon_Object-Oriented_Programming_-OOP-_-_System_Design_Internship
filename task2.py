
import pywhatkit as kit
import http.client
import json
import smtplib
from email.message import EmailMessage
import requests
import os
from abc import ABC, abstractmethod


# NOTIFICATION ABSTRACTION

class NotificationChannel(ABC):

    @abstractmethod
    def send(self, recipient, message, **kwargs):
        pass


# EMAIL SENDER

class EmailSender(NotificationChannel):

    def send(self, recipient, message, **kwargs):

        sender = kwargs.get("sender")
        subject = kwargs.get("subject", "Notification")
        token = os.getenv("GMAIL_APP_PASSWORD")

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, token)
            server.send_message(msg)

        print("Email sent successfully!")


# SMS SENDER

class SMSSender(NotificationChannel):

    def send(self, recipient, message, **kwargs):

        api_key = os.getenv("INFOBIP_API_KEY")

        conn = http.client.HTTPSConnection("m9lq62.api.infobip.com")

        payload = json.dumps({
            "messages": [
                {
                    "destinations": [
                        {
                            "to": recipient
                        }
                    ],
                    "sender": "ServiceSMS",
                    "content": {
                        "text": message
                    }
                }
            ]
        })

        headers = {
            "Authorization": f"App {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        conn.request("POST", "/sms/3/messages", payload, headers)

        res = conn.getresponse()
        data = res.read()

        if res.status >= 400:
            raise Exception(data.decode("utf-8"))

        print(data.decode("utf-8"))

        conn.close()


# SLACK SENDER

class SlackSender(NotificationChannel):

    def send(self, recipient, message, **kwargs):

        url = "https://slack.com/api/chat.postMessage"
        token = os.getenv("SLACK_BOT_TOKEN")

        if not token:
            raise ValueError("Slack token is missing")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "channel": recipient,
            "text": message
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data.get("ok"):
            print("Slack message sent successfully!")
        else:
            print(f"Failed to send Slack message: {data.get('error')}")


# WHATSAPP SENDER

class WhatsAppSender(NotificationChannel):

    def send(self, recipient, message, **kwargs):

        hour = kwargs.get("hour")
        minute = kwargs.get("minute")

        if hour is None or minute is None:
            raise ValueError("Hour and minute are required")

        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Invalid time")

        print("Sending WhatsApp message...")

        kit.sendwhatmsg(recipient, message, hour, minute)

        print("Message sent!")


# NOTIFICATION SERVICE MANAGER

class NotificationService:

    def __init__(self, channel):

        if not isinstance(channel, NotificationChannel):
            raise ValueError("Invalid notification channel")

        self.channel = channel

    def notify(self, recipient, message, **kwargs):

        if not isinstance(recipient, str) or not recipient.strip():
            raise ValueError("Invalid recipient")

        if not isinstance(message, str) or not message.strip():
            raise ValueError("Message cannot be empty")

        self.channel.send(recipient, message, **kwargs)


# TESTING THE SYSTEM

if __name__ == "__main__":

    email = EmailSender()
    sms = SMSSender()
    slack = SlackSender()
    whatsapp = WhatsAppSender()

    email_service = NotificationService(email)
    sms_service = NotificationService(sms)
    slack_service = NotificationService(slack)
    whatsapp_service = NotificationService(whatsapp)

    # EMAIL
    # email_service.notify(
    #     "kehlaouiayman@gmail.com",
    #     "Hello Datheon!",
    #     sender="kehlaouiayman@gmail.com",
    #     subject="Testing Python Script"
    # )

    # SMS
    # sms_service.notify("+212694142908", "Hello Datheon!")

    # SLACK
    # slack_service.notify("projet-de-synthèse-", "Hello Datheon!")

    # WHATSAPP
    # whatsapp_service.notify(
    #     "+212694142908",
    #     "Hello Datheon!",
    #     hour=19,
    #     minute=55
    # )
