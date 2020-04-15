import datetime
import os

import pyotp

import app
from app import APP, mail
from flask import request, Response
import json
from flask_mail import Message

from app.models import Company, Customer, mailLogging


def mail_customer(data):
    """to send dynamic mail to all the users
                             arguments: template name
                            sends mail to all users with there name in it
                            return: string saying send """

    customers = filter_customer({'age_lower': data['age_lower'],
                                 'age_upper': data['age_upper'],
                                 'gender': data['gender']})
    recievers=[]
    for customer in customers:
        recievers.append(customer.customer_email)
        company = Company.query.filter_by(company_name=customer.company_name).first()
        message = data['body']
        subject = data['event']
        msg = Message(sender=company.company_email,
                      recipients=[customer.customer_email],
                      body=message,
                      subject=subject)
        # mail.send(msg)
        log={"sender":  os.environ['EMAIL'],
             "reciever":recievers,
             "company_name":os.environ['COMPANY']
             }
        mailLogging(log)
    return "Sent"


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
