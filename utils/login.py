
from app import APP ,bcrypt
from flask import request, Response
import json

from app.models import Employee, Company


def login_get_user(user_data):

    try:
        login_data = {
            "company_name": user_data['companyName'],
            "emp_email": user_data['userName'],
            "emp_pass": user_data['password'],
        }

# connecting to employee and company database
        employee = Employee.query.filter_by(emp_email=login_data["emp_email"]).first()
        company = Company.query.filter_by(company_name=login_data["company_name"]).first()

# condition statement to check the password with stored hashed password
        if employee  and company and bcrypt.check_password_hash(employee.emp_pass, login_data["emp_pass"]):
            return "Success"
        else:
            return "Unsuccesful"

    except Exception as e:
        print(str(e))

