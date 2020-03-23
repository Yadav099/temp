from app import APP, MIGRATE, DB, METADATA, models
from flask import request
from flask_migrate import migrate, upgrade
from app.models import Employee
from sqlalchemy.sql import text

import os
import json


from sqlalchemy.ext.automap import automap_base

Base = automap_base()

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

    print("YEYEY")
    return models.add_employee(employee, company)

def create_dynamic_employee_table():
    print(os.environ['COMPANY'])
    table_name = '{}_employee'.format(os.environ['COMPANY'])
    table_string = "CREATE TABLE {} (id SERIAL PRIMARY KEY, emp_name varchar(50), emp_pass varchar(150), emp_email varchar(120));".format(table_name)
    print(table_string)
    DB.session.execute(text(table_string))
    DB.session.commit()
