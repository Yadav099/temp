import app
from app import APP
from flask import request, Response, make_response
from functools import wraps

from app.models import Employee
from utils import signup
from utils.login import login_get_user


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        employee = Employee.query.filter_by(emp_pass=request.authorization.password,
                                            emp_email=request.authorization.username)
        if employee.id:
            return f(*args, **kwargs)
        return make_response('could not verify your login!', 401, {'WWW-Authentication': 'Basic realm="Login Required"'})
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
@APP.route('/login', methods=['GET'])
def login_check_user():
    """this block is for the post request
             arguments: user name, email and company name
             return: status code"""
    if request.authorization and request.authorization.username and request.authorization.password:
        data = request.json
        return (login_get_user({
            "companyName": data["companyName"],
            "userName": request.authorization.username,
            "password": request.authorization.password
        }))

@APP.route("/")
def hello():
    return "Hello World!"
