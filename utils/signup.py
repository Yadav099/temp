import app
from app import APP
from flask import request
import json


def signup_add_user(user_data):
    employee = {
        "emp_name" : user_data['employeeName'],
        "emp_email" : user_data['employeeMail'],
        "emp_password" : user_data['employeeID'],
    }
    company = {
        "company_name" : user_data["companyName"],
        "company_email" : user_data["companyMail"],
    }

    employees = Employee() 
    employees.add_employee(employee, company)
