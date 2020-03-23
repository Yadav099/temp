from app import DB, bcrypt, METADATA
from flask import Response
from sqlalchemy.ext.automap import automap_base
import os
import sys
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
        except Exception as e:
            print(str(e))


class Customer(DB.Model):
    __tablename__ = 'customer'
    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    customer_name = DB.Column(DB.String(50), nullable=False)
    customer_email = DB.Column(DB.String(120), nullable=False)
    customer_pno = DB.Column(DB.Integer, nullable=False)
    customer_gender = DB.Column(DB.String(8), nullable=False)
    customer_age = DB.Column(DB.Integer, nullable=False)
    customer_like = DB.Column(DB.String(20), nullable=False)
    company_name = DB.Column(DB.ForeignKey("company.company_name"))


for tables in Base.classes.keys():
    if "_employee" in tables:
        table_args = {'autoload':True, 'autoload_with': DB.engine}
        args = {'__tablename__': tables, '__module__': 'app.models','__table_args__': table_args}
        table = type(tables, (DB.Model,), args)


def add_employee(employee, company_val):
    Base.prepare(DB.engine, reflect=True)
    name = '{}_employee'.format(os.environ['COMPANY'])
    employee_table = Base.classes.get(name)
    employees = employee_table()

    employees.emp_name = employee['emp_name']
    employees.emp_email = employee['emp_email']
    employees.emp_pass = bcrypt.generate_password_hash(employee['emp_pass']).decode("utf-8")
    employees.isAdmin = employee['isAdmin']
    employees.company_name = employee['company_name']

    company = Company()
    company.add_company(company_val)
    try:
        DB.session.add(employees)
        DB.session.commit()
        resp = json.dumps({'message': "Company Added"})
        return Response(resp, 200)
    except Exception as e:
        print(str(e))

