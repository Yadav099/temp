from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError
from app import DB, bcrypt, METADATA
from flask import Response
from sqlalchemy.ext.automap import automap_base
import os
import json


Base = automap_base()
METADATA.reflect(DB.engine)

Base.prepare(DB.engine, reflect=True)


class Company(DB.Model):
    __tablename__ = 'company'
    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    company_name = DB.Column(DB.String(30), nullable=False, unique=True)
    company_email = DB.Column(DB.String(120), nullable=False, unique=True)

    def add_company(self, company):
        self.company_name = company['company_name']
        self.company_email = company['company_email']
        try:
            DB.session.add(self)
            DB.session.commit()
            resp = json.dumps({'message': "Company Added"})
            return Response(resp, 200)
        except SQLAlchemyError as e:
            print("Company data repeated")
            return e


class Customer(DB.Model):
    __tablename__ = 'customer'
    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    customer_name = DB.Column(DB.String(50), nullable=False)
    customer_email = DB.Column(DB.String(120), nullable=False)
    customer_pno = DB.Column(DB.Integer, nullable=False)
    customer_gender = DB.Column(DB.String(8), nullable=False)
    customer_age = DB.Column(DB.Integer, nullable=False)
    customer_like = DB.Column(DB.String(20), nullable=False)
    date=DB.Column(DB.TIMESTAMP)

    company_name = DB.Column(DB.ForeignKey("company.company_name"))


for tables in Base.classes.keys():
    if "_employee" in tables:
        table_args = {'autoload': True, 'autoload_with': DB.engine}
        args = {'__tablename__': tables, '__module__': 'app.models', '__table_args__': table_args}
        table = type(tables, (DB.Model,), args)


def add_employee(employee, company_val):
    try:
        Base.prepare(DB.engine, reflect=True)
        name = '{}_employee'.format(os.environ['COMPANY'])
        employee_table = Base.classes.get(name)
        employees = employee_table()

        employees.emp_name = employee['emp_name']
        employees.emp_email = employee['emp_email']
        employees.admin = employee['isAdmin']
        employees.company_name = employee['company_name']

        company = Company()
        company.add_company(company_val)

        DB.session.add(employees)
        DB.session.commit()

        os.environ['COMPANY']=company_val['company_name']
        os.environ['EMAIL']=employee['emp_email']
        return "Successful"
    except SQLAlchemyError as e:
        print(e)
        return "Company details already exist"

def add_new_employee_auth(employee):
      try:
            Base.prepare(DB.engine, reflect=True)
            name = '{}_employee'.format(os.environ['COMPANY']).lower()
            employee_table = Base.classes.get(name)
            employees = employee_table()

            employees.emp_email = employee['emp_email']
            employees.admin = employee['isAdmin']
            employees.company_name = employee['company_name']

            DB.session.add(employees)
            DB.session.commit()

            return "Successful"

      except SQLAlchemyError as e:
        print(e)
        return "Company details already exist"


def add_new_employee(employee):
    Base.prepare(DB.engine, reflect=True)
    name = '{}_employee'.format(employee['company'].lower())
    employee_table = Base.classes.get(name)

    employees = DB.session.query(employee_table).filter_by(emp_email=employee['emp_email']).first()
    employees.emp_name = employee['emp_name']
    employees.emp_id=employee['emp_id']
    employees.emp_pass = bcrypt.generate_password_hash(employee['emp_pass']).decode("utf-8")
    employees.auth=employee['auth']
    try:
        DB.session.add(employees)
        DB.session.commit()
        return "Successful"
    except SQLAlchemyError as e:
        print("Data repeated")
        return "Data repeated"


def changePasswordInDb(data):
    try:
        if data['emp_pass'] is not None:
            Base.prepare(DB.engine, reflect=True)
            name = '{}_employee'.format(os.environ['COMPANY'])
            employee_table = Base.classes.get(name)
            userEmail = os.environ['EMAIL']
            user = DB.session.query(employee_table).filter_by(emp_email=userEmail).first()
            if user is not None:
                user.emp_pass = bcrypt.generate_password_hash(data['emp_pass']).decode("utf-8")
                DB.session.commit()
                return 'updated pass'
            else:
                return "No Changes"
        else:
            return "No Changes"

        return "Done"
    except Exception as e:
        print(str(e))
        return "Failure"


def changeEmployeeEmailInDb(data):
    try:
        Base.prepare(DB.engine, reflect=True)
        name = '{}_employee'.format(os.environ['COMPANY'])
        employee_table = Base.classes.get(name)
        userEmail = os.environ['EMAIL']
        print(data['emp_email'])
        print(userEmail)
        user = DB.session.query(employee_table).filter_by(emp_email=userEmail).first()
        if user and bcrypt.check_password_hash(user.emp_pass, data["emp_password"]):
            user.emp_email = data['emp_email']
            DB.session.commit()
            os.environ['EMAIL'] = data['emp_email']
            return "success"
        else:
            return "fail"


    except Exception as e:
        print(str(e))
        return "Failure"


def mailLogging(log):
    try:
        Base.prepare(DB.engine, reflect=True)
        name = '{}_mail'.format(os.environ['COMPANY'])
        mail_table = Base.classes.get(name)
        mail = mail_table()
        mail.sender=log['sender']
        mail.reciever=log['reciever']
        mail.company_name=log['company_name']

        DB.session.add(mail)
        DB.session.commit()
        print("done")
    except Exception as e:
        print(str(e))

