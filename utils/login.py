
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
        print(employee.emp_pass)
        print("aaaa")
        print(bcrypt.generate_password_hash(login_data["emp_pass"]))

        # function to check  whether email and company name are vlid or not
        if company.company_name == login_data["company_name"]:
            if employee.emp_email == login_data["emp_email"]:

# condition statement to check the password with stored hashed password
              if employee and bcrypt.check_password_hash(employee.emp_pass, login_data["emp_pass"]):
                return "Successful"
              else:
                return "3"
            else:
                return "2"
        else:
              return "1"


    except Exception as e:
        print(str(e))

