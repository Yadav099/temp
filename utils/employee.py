from app import DB, bcrypt, METADATA, APP
from flask import Response, jsonify
from sqlalchemy.ext.automap import automap_base
import os
import sys
import json
from app.models import Company, Base

from app.models import changePasswordInDb, changeEmployeeEmailInDb
from utils.mail import mailVerifyToken

Base = automap_base()
METADATA.reflect(DB.engine)

Base.prepare(DB.engine, reflect=True)


def employeeList():
    try:
        name = '{}_employee'.format(os.environ['COMPANY'].lower())
        employee_table = Base.classes.get(name)
        employee = DB.session.query(employee_table).all()
        response = []
        for user in employee:
            if user.auth:
                response.append({"name": user.emp_name, "mail": user.emp_email,"id":user.emp_id, "admin": user.admin})

        result = {"data": response, "employeeEmail": os.environ['EMAIL']}
        return result

    except Exception as e:
        print(str(e))
        result = jsonify({"error": "NO Data"})
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
        os.environ['COMPANY'] = data['emp_company'].lower()
        os.environ['EMAIL'] = data['emp_email']

        employee_table = Base.classes.get(name)
        employee = DB.session.query(employee_table).filter_by(emp_email=data['emp_email']).first()
        company = Company.query.filter_by(company_name=login_data["company_name"]).first()

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
        name = '{}_employee'.format(os.environ['COMPANY'].lower())
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


def userDetails():
    try:
        Base.prepare(DB.engine, reflect=True)
        name = '{}_employee'.format(os.environ['COMPANY'].lower())
        employee_table = Base.classes.get(name)
        userEmail = os.environ['EMAIL']
        company = Company.query.filter_by(company_name=os.environ['COMPANY']).first()

        user = DB.session.query(employee_table).filter_by(emp_email=userEmail).first()
        if user and company:
            data = {"name": user.emp_name, "email": user.emp_email, "admin": user.admin,
                    "companyEmail": company.company_email,
                    "company": company.company_name,"id":user.emp_id}
            return data
        else:
            return {"Error": "Failed"}


    except Exception as e:
        print(str(e))
        return {"Error": "No connection"}
    return data


def emailAuthentication(data):
    try:

        # connecting to employee and company database
        name = '{}_employee'.format(data['company'])
        employee_table = Base.classes.get(name)
        employee = DB.session.query(employee_table).filter_by(emp_email=data['email']).first()
        # condition statement to check the password with stored hashed password
        if employee :
            employee.auth = False
            DB.session.add(employee)
            DB.session.commit()
    except Exception as e:
        return str(e)


