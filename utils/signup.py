from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError
from app import APP, MIGRATE, DB, METADATA, models
from flask import request
from flask_migrate import migrate, upgrade
from sqlalchemy.sql import text

import os
import json


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

    os.environ['COMPANY'] = user_data['companyName']
    create_dynamic_employee_table()

    return models.add_employee(employee, company)


def create_dynamic_employee_table():
    try:
        table_name = '{}_employee'.format(os.environ['COMPANY'])
        table_string = "CREATE TABLE {} (id SERIAL PRIMARY KEY, emp_name varchar(50), emp_pass varchar(150), emp_email varchar(120), company_name varchar(50), FOREIGN KEY (company_name) REFERENCES company (company_name));".format(
            table_name)
        DB.session.execute(text(table_string))
        DB.session.commit()

    # except IntegrityError as e:
    # Tried this exception but its not working
    except DBAPIError as e:

        # Raised when the execution of a database operation fails. If the error-raising operation occured in the
        # execution of a SQL statement, that statement and its parameters will be available on the exception  object
        # in the statement and params attributes. The wrapped exception object is available in the orig attribute.
        # Its type and properties are DB-API implementation specific.

        print("Company already exist")
        exit(0)
