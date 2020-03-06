import app
from app import APP
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
        employee = Employee.query.filter_by(emp_pass=login_data["emp_pass"], emp_email=login_data["emp_email"]).first()
        company = Company.query.filter_by(company_name=login_data["company_name"]).first()
        if employee.id and company.id:
            return Response("", 200)
    except Exception as e:
        return Response("", 400)
