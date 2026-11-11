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
    def send(self, recipient, message):
        pass


# EMAIL SENDER

class EmailSender(NotificationChannel):

    def send(self,sender, recipient,subject, message):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, "vcwe jvpy gaoo lrqn")
            server.send_message(msg)

        print("Email sent successfully!")


# SMS SENDER

class SMSSender(NotificationChannel):

    def send(self, recipient, message):
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
            'Authorization': 'App cd8bbe61537d22681297f7c427816c4c-d005ae5d-dfb3-4ca4-a9f6-795e56b3fc64',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/sms/3/messages", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))


# SLACK SENDER

class SlackSender(NotificationChannel):

    def send(self, recipient, message):
        url = "https://slack.com/api/chat.postMessage"
        token = os.getenv("SLACK_BOT_TOKEN")
        
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

    def send(self, recipient, message, hour=None, minute=None):
        print("Sending WhatsApp message...")
        kit.sendwhatmsg(recipient, message, hour, minute)
        print("Message sent.")


# NOTIFICATION SERVICE MANAGER

class NotificationService:

    def __init__(self, channel):
        if not isinstance(channel, NotificationChannel):
            raise ValueError("Invalid notification channel")
        self.channel = channel

    def notify(self, recipient, message, **kwargs):
        if not isinstance(recipient, str):
            raise ValueError("Invalid recipient")

        if not isinstance(message, str):
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

    # email_service.notify("kehlaouiayman@gmail.com",'kehlaouiayman@gmail.com','testing python script...', "Hello Datheon!")
    # sms_service.notify("+212694142908", "Hello Datheon")
    # whatsapp_service.notify("+212694142908", "Hello Datheon", hour=19, minute=55)
    #slack_service.notify('projet-de-synthèse-','hello')
