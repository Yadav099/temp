import app
from app import APP
from flask import request


# api to get the data of newly registered users
@app.route('/signup', methods=['POST'])
def signup_create_user():
    """this block is for the post request
            arguments: registration data
            return: status code"""
    try:
        response_code = signup_add_user(request.json)
        return response_code
    except Exception as err:
        print(f'Other error occurred: {err}')
        return 404


# api to validate the user
@app.route('/signup', methods=['GET'])
def login_check_user():
    """this block is for the post request
            arguments: user name, email and company name
            return: status code"""
    try:
        response_code = login_get_user(request.json)
        return response_code
    except Exception as err:
        print(f'Other error occurred: {err}')
        return 400
