from app import DB, bcrypt
from flask import Response
import json


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


class Employee(DB.Model):
    __tablename__ = 'employee'
    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    emp_name = DB.Column(DB.String(50), nullable=False)
    emp_pass = DB.Column(DB.String(150), nullable=False)
    emp_email = DB.Column(DB.String(120), nullable=False)
    isAdmin = DB.Column(DB.Boolean, default=False)
    company_name = DB.Column(DB.ForeignKey("company.company_name"))

    def add_employee(self, employee, company_val):
        self.emp_name = employee['emp_name']
        self.emp_email = employee['emp_email']
        self.emp_pass = str(bcrypt.generate_password_hash(employee['emp_pass']).decode("utf-8"))
        self.isAdmin = employee['isAdmin']
        self.company_name = employee['company_name']

        company = Company()
        company.add_company(company_val)
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
