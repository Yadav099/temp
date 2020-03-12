from app import DB
from flask import request
import json
import csv
import io
from app.models import Employee, Customer


def column_no_finder(row, test):
    position = -1
    if test in row:
        for item in row:
            position += 1
            if item == test:
                return position
    else:
        return -1


def add_customer_list(file_reader):
    line_count = 0
    customer = Customer()
    for row in file_reader:
        if line_count == 0:
            name_index = column_no_finder(row, "name")
            email_index = column_no_finder(row, "email")
            gender_index = column_no_finder(row, "gender")
            age_index = column_no_finder(row, "age")
            pno_index = column_no_finder(row, "p_,no")
            like_index = column_no_finder(row, "like")
            company_name_index = column_no_finder(row, "company_name")

        elif line_count > 1:
            customer.add_customer({
                'customer_name': row[name_index],
                'customer_age': row[age_index],
                'customer_email': row[email_index],
                'customer_gender': row[gender_index],
                'customer_pno': row[pno_index],
                'customer_like': row[like_index],
                'company_name': row[company_name_index]
            })
        line_count += 1
    return "customer data added"
