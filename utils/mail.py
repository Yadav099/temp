import datetime
import os

import pyotp

import app
from app import APP, mail
from flask import request, Response, url_for, render_template
import json
from flask_mail import Message

from textmagic.rest import TextmagicRestClient

from app.models import Company, mailLogging, Customer
from app import f
from utils.Filters import mainFilter


def mail_customer(data):
    """to send dynamic mail to all the users
                             arguments: template name
                            sends mail to all users with there name in it
                            return: string saying send """

    try:
        print(type(data))
        msg = Message(sender=APP.config['MAIL_DEFAULT_SENDER'],
                      recipients=['yadirockz@gmail.com'],
                      html=data,
                      )
        mail.send(msg)
        # username = "your_textmagic_username"
        # token = "your_apiv2_key"
        # client = TextmagicRestClient(username, token)
        # message = client.messages.create(phones="0620098510", text="Hello TextMagic")
        # print(message)
        return "Done"

    except Exception as e:
        # print(str(e))
        # log = {"sender": os.environ['EMAIL'],
        #        "reciever": recievers,
        #        "company_name": os.environ['COMPANY']
        #        }
        # # mailLogging(log)

        return "error"


def filter_customer(customer_data):
    return Customer.query \
        .filter_by(customer_gender=customer_data['gender']) \
        .filter(Customer.customer_age < customer_data['age_upper']) \
        .filter(Customer.customer_age > customer_data['age_lower']) \
        .all()


def mailVerifyToken(data):
    totp = pyotp.TOTP('base32secret3232', interval=120)

    #
    # # OTP verified for current time
    # totp.verify('492039')  # => True
    # time.sleep(30)
    # totp.verify('492039')  # => False
    APP.config['otp'] = totp
    message = "verrification token is {}".format(totp.now())
    try:
        msg = Message(sender=APP.config['MAIL_USERNAME'],
                      recipients=[os.environ['EMAIL']],
                      body=message,
                      subject="Reset your password")
        mail.send(msg)
        return "Success"
    except Exception as e:
        print(str(e))
        return "Failed"


def send_confirmation_email(user_email, user_company):
    try:
        # data = json.dumps({"email": user_email, "company": user_company})
        data = "{} {}".format(user_email, user_company)
        encrypt_value = f.encrypt(data.encode("utf-8"))

        token = app.confirm_serializer.dumps(json.dumps({"data": encrypt_value.decode("utf-8")}),
                                             salt='email-confirm')

        msg = Message('confirm Email', sender=APP.config['MAIL_DEFAULT_SENDER'],
                      recipients=[user_email],
                      )

        link = url_for('confirm_email', token=token, _external=True)
        msg.body = "your link is {}".format(link)
        print(link)
        mail.send(msg)
        return "Success"
    except Exception as e:
        print(str(e))
        return "Failed"
