from app import DB, bcrypt, METADATA, APP
from flask import Response
from sqlalchemy.ext.automap import automap_base
import os
import sys
import json

from app.models import changePasswordInDb, changeEmployeeEmailInDb
from utils.mail import mailVerifyToken

Base = automap_base()
METADATA.reflect(DB.engine)

Base.prepare(DB.engine, reflect=True)


def employeeList():
    name = '{}_employee'.format(os.environ['COMPANY'])
    employee_table = Base.classes.get(name)
    employee = DB.session.query(employee_table).all()
    response = []
    for user in employee:
        response.append({"name": user.emp_name, "mail": user.emp_email})

    result = {"data": response, "employeeEmail": os.environ['EMAIL']}
    return result


def deleteEmpployeeByname(userdata):
    name = '{}_employee'.format(os.environ['COMPANY'])
    employee_table = Base.classes.get(name)
    employee = DB.session.query(employee_table).filter_by(emp_email=userdata['emp_email']
                                                          , emp_name=userdata['emp_name']).first()
    if employee:
        try:
            DB.session.delete(employee)
            DB.session.commit()
            return "deleted"

        except Exception as e:
            return str(e)
    else:
        return "failure"


def forgotEmployeePassword(data):
    try:
        name = '{}_employee'.format(data['emp_company'])
        os.environ['COMPANY'] = data['emp_company']
        os.environ['EMAIL'] = data['emp_email']

        employee_table = Base.classes.get(name)
        employee = DB.session.query(employee_table).filter_by(emp_email=data['emp_email']).first()

        # condition statement to check the password with stored hashed password
        if employee:
            return mailVerifyToken(data)

    except Exception as e:
        return "Failure"


def verrifyEmployeeToken(data):
    try:
        if APP.config['otp'].verify(data['token']):
            return "Success"
        else:
            return "Failure"
    except Exception as e:
        return "Failure"


def changeEmployeePassword(data):
    return changePasswordInDb(data);


def changeEmployeeEmail(data):
    return changeEmployeeEmailInDb(data);


def changeEmployeeProfilePassword(data):
    try:
        Base.prepare(DB.engine, reflect=True)
        name = '{}_employee'.format(os.environ['COMPANY'])
        employee_table = Base.classes.get(name)
        userEmail = os.environ['EMAIL']

        user = DB.session.query(employee_table).filter_by(emp_email=userEmail).first()
        if user and bcrypt.check_password_hash(user.emp_pass, data["emp_password"]):
            user.emp_pass = bcrypt.generate_password_hash(data['new_password']).decode("utf-8")
            DB.session.commit()

            return "success"
        else:
            return "fail"


    except Exception as e:
        print(str(e))
        return "Failure"
