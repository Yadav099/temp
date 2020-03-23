import csv
import io
from app import APP
from flask import request, Response, make_response
from functools import wraps

from app.models import Employee
from utils import signup
from utils.customers import add_customer_list, add_customer
from utils.login import login_get_user
from utils.mail import mail_customer


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        employee = Employee.query.filter_by(emp_pass=request.authorization.password,
                                            emp_email=request.authorization.username)
        if employee.id:
            return f(*args, **kwargs)
        return make_response('could not verify your login!', 401,
                             {'WWW-Authentication': 'Basic realm="Login Required"'})

    return decorated


# api to get the data of newly registered users
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
        return (login_get_user({
            "companyName": data["companyName"],
            "user_email": request.authorization.username,
            "pass": request.authorization.password
        }))


# api to send mails to the targeted users
@APP.route("/mail", methods=['GET'])
def dynamic_mail_users():
    """to send dynamic mail to all the users
                            arguments: template name
                            sends mail to all users with there name in it
                            return: string saying send """
    data = request.json
    return mail_customer(data)


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
#  @APP.route("/customer/add/CSV", methods=['POST'])
#  def customer():
    #  return customers.add_customer(request.json)
#

