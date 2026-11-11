import pywhatkit as kit
import http.client
import json
import smtplib
from email.message import EmailMessage
from abc import ABC, abstractmethod


# NOTIFICATION ABSTRACTION

class NotificationChannel(ABC):

    @abstractmethod
    def send(self, recipient, message):
        pass


# EMAIL  SENDER

class EmailSender(NotificationChannel):

    def send(self,sender, recipient, message):
        msg = EmailMessage()
        msg["Subject"] = "Hello from Python"
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("kehlaouiayman@gmail.com", "vcwe jvpy gaoo lrqn")

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

        print("Sending Slack message...")
        print("Channel:", recipient)
        print("Message:", message)


# 5. WHATSAPP SENDER

class WhatsAppSender(NotificationChannel):

    def send(self, recipient, message,hour,minute):
        print("Sending WhatsApp message...")
        kit.sendwhatmsg(recipient,message, hour,minute)
        print("Message sent.")
        


# 6. NOTIFICATION SERVICE

class NotificationService:

    def __init__(self, channel):

        if not isinstance(channel, NotificationChannel):
            raise TypeError("Invalid notification channel")

        self.__channel = channel

    def notify(self, recipient, message):

        if not isinstance(recipient, str) or recipient.strip() == "":
            raise ValueError("Invalid recipient")

        if not isinstance(message, str) or message.strip() == "":
            raise ValueError("Message cannot be empty")

        self.__channel.send(recipient, message)


# 7. TESTING THE SYSTEM

# Create notification channels

email = EmailSender()
sms = SMSSender()
slack = SlackSender()
whatsapp = WhatsAppSender()


# Inject channels into the service

email_service = NotificationService(email)
sms_service = NotificationService(sms)
slack_service = NotificationService(slack)
whatsapp_service = NotificationService(whatsapp)


# Send notifications


#whatsapp.send(
#    "+212664503097",
#    "salam khadija",
#    19,
#    55
#)


#sms.send(+212694142908,"ayman's python code is working.")


#email.send('kehlaouiayman@gmail.com','kehlaouiayman@gmail.com','hello your code is working.')


