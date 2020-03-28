import app
from app import APP, mail
from flask import request, Response
import json
from flask_mail import Message

from app.models import Company, Customer


def mail_customer(data):
    """to send dynamic mail to all the users
                            arguments: template name
                            sends mail to all users with there name in it
                            return: string saying send """

    customers = filter_customer({'age_lower': data['age_lower'],
                                 'age_upper': data['age_upper'],
                                 'gender': data['gender']})
    for customer in customers:
        company = Company.query.filter_by(company_name=customer.company_name).first()
        message = data['body']
        subject = data['event']
        msg = Message(sender=company.company_email,
                      recipients=[customer.customer_email],
                      body=message,
                      subject=subject)
        mail.send(msg)
    return "Sent"


def filter_customer(customer_data):
    return Customer.query \
        .filter_by(customer_gender=customer_data['gender']) \
        .filter(Customer.customer_age < customer_data['age_upper']) \
        .filter(Customer.customer_age > customer_data['age_lower']) \
        .all()
