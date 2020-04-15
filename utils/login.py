from app import APP, bcrypt, DB
import jwt;
from flask import request, Response, jsonify
import os
import json
from datetime import datetime, timedelta

from app.models import Company, Base


def login_get_user(user_data):
    try:
        login_data = {
            "company_name": user_data['companyName'],

            "emp_email": user_data['user_email'],
            "emp_pass": user_data['pass'],
        }

        # connecting to employee and company database
        name = '{}_employee'.format(login_data['company_name'].lower())
        employee_table = Base.classes.get(name)
        employee = DB.session.query(employee_table).filter_by(emp_email=login_data['emp_email']).first()
        company = Company.query.filter_by(company_name=login_data["company_name"]).first()
        admin=employee.admin
        # condition statement to check the password with stored hashed password
        if employee and company and bcrypt.check_password_hash(employee.emp_pass, login_data["emp_pass"]):
            os.environ['COMPANY'] = user_data['companyName']
            print(
            os.environ['COMPANY']

            )
            os.environ['EMAIL'] = login_data['emp_email']
            encoded = jwt.encode({'exp': datetime.utcnow() + timedelta(seconds=1800), 'a': 't'}, 'secret',
                                 algorithm='HS256').decode(
                "utf-8")

            return jsonify({"access_token": {"token": str(encoded), "admin":admin}})


        else:
            result = jsonify({"error": "Invalid user"})
            return result

    except Exception as e:
        print(str(e))
        result = jsonify({"error": "Invalid user"})
        return result


def verifyJWTToken(data):
    try:

        encode = jwt.decode(data['Authorization'], 'secret', algorithms=['HS256'])

        if encode:
            return jsonify({"isLoggedIn": "true"})
        else:
            return jsonify({"isLoggedIn": "false"})
    except Exception as e:
        print(str(e))
        return jsonify({"error": True})
