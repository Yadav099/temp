from app import APP, bcrypt, DB, client
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
        name = '{}_employee'.format(login_data['company_name'])
        employee_table = Base.classes.get(name)
        employee = DB.session.query(employee_table).filter_by(emp_email=login_data['emp_email']).first()
        company = Company.query.filter_by(company_name=login_data["company_name"]).first()

        # condition statement to check the password with stored hashed password
        if employee and company and bcrypt.check_password_hash(employee.emp_pass, login_data["emp_pass"]):
            os.environ['COMPANY'] = user_data['companyName']
            os.environ['EMAIL']=login_data['emp_email']
            encoded = jwt.encode({'exp': datetime.utcnow() + timedelta(seconds=1800), 'a': 't'}, 'secret',
                                 algorithm='HS256').decode(
                "utf-8")

            number = "9620098510"
            message = "Hello human"
            # response=client.send_message({
            #     'from': 'Smart comm',
            #     'to': '919620098510',
            #     'text': 'Hello from Vonage',
            # })
            # print(response)
            # response=response['message'][0]
            # if response['status']=='0':
            #     print(response['message-id'])
            # else:
            #     print(response['error-text'])
            return jsonify({"access_token": {"token": str(encoded), "loggedIn": 'True'}})


        else:
            result = jsonify({"error": "Invalid user"})
            return result

    except Exception as e:
        print(str(e))
        return "failure"


def verifyJWTToken(data):
    try:

        encode = jwt.decode(data['Authorization'], 'secret', algorithms=['HS256'])

        if encode:
            return jsonify({"isLoggedIn": "true"})
        else:
            return jsonify({"isLoggedIn": "false"})
    except Exception as e:
        print(str(e))
        return jsonify({"Error": True})
