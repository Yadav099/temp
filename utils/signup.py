import app
from app import APP
from flask import request
import json

from app.models import Employee


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

    employees = Employee()
    return employees.add_employee(employee, company)
