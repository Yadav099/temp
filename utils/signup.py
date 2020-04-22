from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError
from app import APP, MIGRATE, DB, METADATA, models,f
from flask import request, Response
from flask_migrate import migrate, upgrade
from sqlalchemy.sql import text

import os
import json
import os, random, string

from simplecrypt import encrypt, decrypt
from app.models import add_new_employee, add_new_employee_auth
from utils.mail import send_confirmation_email


def signup_add_new_user_auth(user_data):
    employee = {
        "emp_email": user_data['employeeMail'],
        "company_name": os.environ['COMPANY'].lower(),
        "isAdmin": user_data['admin']

    }
    response = add_new_employee_auth(employee)
    if response == "Successful":
        send_confirmation_email(employee["emp_email"], employee['company_name'])

        return response
    else:
        return response


def signup_add_new_user(user_data):
    data=user_data['token']
    print(type(data['data'].encode("utf-8")))

    plaintext=f.decrypt(data['data'].encode("utf-8"))
    print(plaintext.decode("utf-8"))
    plaintext=plaintext.split()
    print(plaintext[0].decode("utf-8"))
    employee = {
        "emp_name": user_data['employeeName'],

        "emp_id": user_data['employeeId'],
        "emp_pass": user_data['employeePass'],
        "company": plaintext[1].decode("utf-8").lower(),
        "emp_email": plaintext[0].decode("utf-8"),
        "auth":True
    }
    print(user_data)
    response = add_new_employee(employee)
    if response == "Successful":

        return response
    else:
        return response


def signup_add_user(user_data):
    length = 13
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    password = ''.join(random.choice(chars) for i in range(length))

    employee = {
        "emp_name": user_data['employeeName'],
        "emp_email": user_data['employeeMail'],
        "company_name": user_data['companyName'].lower(),
        "isAdmin": True
    }
    company = {
        "company_name": user_data["companyName"].lower(),
        "company_email": user_data["companyMail"],
    }

    os.environ['COMPANY'] = user_data['companyName'].lower()
    create_dynamic_employee_table()
    response = models.add_employee(employee, company)
    print(response)
    if response == "Successful":
        send_confirmation_email(employee["emp_email"], company['company_name'])

        return response
    else:
        return response


def create_dynamic_employee_table():
    try:
        table_name1 = '{}_employee'.format(os.environ['COMPANY'])
        table_string1 = "CREATE TABLE {} (id SERIAL PRIMARY KEY,emp_id varchar(50) UNIQUE, emp_name varchar(50) UNIQUE, emp_pass varchar(150) , " \
                        "emp_email varchar(120) UNIQUE, company_name varchar(50), FOREIGN KEY (company_name) " \
                        "REFERENCES company (company_name),admin boolean, auth boolean DEFAULT false);".format(
            table_name1)

        table_name = '{}_mail'.format(os.environ['COMPANY'])
        table_string = "CREATE TABLE {} (id SERIAL PRIMARY KEY,sender varchar(50) ,date TIMESTAMP DEFAULT now() ,reciever text[][]);".format(
            table_name)
        DB.session.execute(text(table_string))

        DB.session.execute(text(table_string1))
        DB.session.commit()

    # except IntegrityError as e:
    # Tried this exception but its not working
    except DBAPIError as e:

        # Raised when the execution of a database operation fails. If the error-raising operation occured in the
        # execution of a SQL statement, that statement and its parameters will be available on the exception  object
        # in the statement and params attributes. The wrapped exception object is available in the orig attribute.
        # Its type and properties are DB-API implementation specific.
        print(str(e))
        return Response("Company details already exist", 400)
