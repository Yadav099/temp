import csv
import io

from flask_jwt import jwt_required

from app import APP, jwt
from flask import request, Response, make_response, jsonify
from functools import wraps

#  from app.models import Employee
from utils import signup, customers
from utils.customers import add_customer_list, add_customer
from utils.employee import employeeList, deleteEmpployeeByname, forgotEmployeePassword, verrifyEmployeeToken, \
    changeEmployeePassword, changeEmployeeEmail, changeEmployeeProfilePassword
from utils.login import login_get_user, verifyJWTToken
from utils.mail import mail_customer

# api to get the data of newly registered users
from utils.signup import signup_add_new_nonadmin_user


@APP.route('/signup', methods=['POST'])
def signup_create_user():
    """this block is for the post request
            arguments: registration data
            return: status code"""
    try:

        signup.signup_add_user(request.json)
        return Response("", 200)
    except Exception as err:
        return Response("", 400)


# api to validate the user
@APP.route('/login', methods=['POST'])
def login_check_user():
    """this block is for the post request
             arguments: user name, email and company name
             return: status code"""

    if request.authorization and request.authorization.username and request.authorization.password:
        data = request.json
        return ((login_get_user({
            "companyName": data["companyName"],
            "user_email": request.authorization.username,
            "pass": request.authorization.password
        })))


# api to send mails to the targeted users
@APP.route("/mail", methods=['POST'])
def dynamic_mail_users():
    try:
        """to send dynamic mail to all the users
                                arguments: template name
                                sends mail to all users with there name in it
                                return: string saying send """
        data = request.json
        return mail_customer(data)
    except Exception as e:
        return e


# api to insert customer data from a CSV file to the database
@APP.route("/customer/add/CSV", methods=['POST'])
def customer():
    file = request.files['csv']
    if not file:
        return "No file"
    file_contents = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    file_reader = csv.reader(file_contents)
    return add_customer_list(file_reader)


#  api to insert a row of customer data to the database
@APP.route("/customer/addemployee", methods=['POST'])
def employee():
    # print(request.json['token'])
    return signup_add_new_nonadmin_user(request.json)


#

@APP.route("/customer/viewemployee", methods=['GET'])
def viewEmpployee():
    return employeeList();


@APP.route("/customer/deleteEmployee", methods=['DELETE'])
def deleteEmpployee():
    data = request.json

    return deleteEmpployeeByname(data);


@APP.route('/ForgotPassword', methods=['POST'])
def forgotPassword():
    data = request.json
    return forgotEmployeePassword(data)


@APP.route('/VerrifyToken', methods=['POST'])
def verifyToken():
    data = request.json
    return verrifyEmployeeToken(data)


@APP.route("/ChangePassword", methods=['PUT'])
def changePassword():
    data = request.json
    return changeEmployeePassword(data)


@APP.route("/verify", methods=['POST'])
def verifyUser():
    data = request.json
    return verifyJWTToken(data)




@APP.route("/logout", methods=['POST'])
def logout():
    data = request.json['token']

@APP.route("/ChangeEmail", methods=['POST'])
def ChangeEmail():
    data = request.json
    return changeEmployeeEmail(data)

@APP.route("/ChangeProfilePassword", methods=['PUT'])
def changeProfilePassword():
    data = request.json
    return changeEmployeeProfilePassword(data)