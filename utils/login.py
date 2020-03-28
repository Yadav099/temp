from app import APP ,bcrypt, DB
from flask import request, Response
import os
import json

from app.models import Company, Base


def login_get_user(user_data):

    try:
        login_data = {
            "company_name": user_data['companyName'],
<<<<<<< HEAD
            "emp_email": user_data['userName'],
            "emp_pass": user_data['password'],
=======
            "emp_email": user_data['user_email'],
            "emp_pass": user_data['pass'],
>>>>>>> 8340faaab433f73d1db6049982ff0c215ced6cc7
        }

# connecting to employee and company database
        name = '{}_employee'.format(login_data['company_name'])
        employee_table = Base.classes.get(name)
        employee = DB.session.query(employee_table).filter_by(emp_email=login_data['emp_email']).first()
        company = Company.query.filter_by(company_name=login_data["company_name"]).first()

# condition statement to check the password with stored hashed password
        if employee  and company and bcrypt.check_password_hash(employee.emp_pass, login_data["emp_pass"]):
            return "Success"
<<<<<<< HEAD
        else:
            return "Unsuccesful"
=======
>>>>>>> 8340faaab433f73d1db6049982ff0c215ced6cc7

    except Exception as e:
        print(str(e))

