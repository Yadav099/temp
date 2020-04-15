from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError
from app import APP, MIGRATE, DB, METADATA, models
from flask import request,Response
from flask_migrate import migrate, upgrade
from sqlalchemy.sql import text

import os
import json

from app.models import add_new_employee


def signup_add_new_user(user_data):
    employee = {
        "emp_name": user_data['employeeName'],
        "emp_email": user_data['employeeMail'],
        "emp_pass": user_data['employeeId'],
        "company_name": os.environ['COMPANY'],
        "admin": user_data['admin']
    }
    print(user_data)
    return add_new_employee(employee)


def signup_add_user(user_data):
    employee = {
        "emp_name": user_data['employeeName'],
        "emp_email": user_data['employeeMail'],
        "emp_pass": user_data['employeeID'],
        "company_name": user_data['companyName'],
        "isAdmin": True
    }
    company = {
        "company_name": user_data["companyName"],
        "company_email": user_data["companyMail"],
    }

    os.environ['COMPANY'] = user_data['companyName'].lower()
    create_dynamic_employee_table()

    return models.add_employee(employee, company)


def create_dynamic_employee_table():
    try:
        table_name1 = '{}_employee'.format(os.environ['COMPANY'])
        table_string1 = "CREATE TABLE {} (id SERIAL PRIMARY KEY, emp_name varchar(50) UNIQUE, emp_pass varchar(150) , " \
                       "emp_email varchar(120) UNIQUE, company_name varchar(50), FOREIGN KEY (company_name) " \
                       "REFERENCES company (company_name),admin boolean);".format(
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

