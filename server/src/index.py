
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_cors import CORS
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
from SignUpHandler import SignUpHandler
from LoginHandler  import LoginHandler
from TokenCheckHandler import TokenCheckHandler

app = Flask(__name__)
CORS(app)

# accepts: json { 'email': {email}, 'password': {password} }
# returns: json { 'response string': {Str}, 'response code': {Int} }
@app.route("/signupSubmit", methods=['POST'])
def signUpSubmit():
    if request.method == 'POST':
        signUpHandler = SignUpHandler()

        loginFormJson = request.get_json()
        email = str(loginFormJson['email'])
        password = str(loginFormJson['password'])

        response = signUpHandler.handleUserSignUp(email, password)
        return jsonify(response)

# accepts: json { 'email': {email}, 'password': {password} }
# returns: json { 'response string': {Str/token}, 'response code': {Int} }
@app.route("/loginSubmit",  methods=['POST'])
def loginSubmit():
    if request.method == 'POST':
        loginHandler = LoginHandler()

        signupFormJson = request.get_json()
        email = str(signupFormJson['email'])
        password = str(signupFormJson['password'])

        resultPackage = loginHandler.handleUserLogin(email, password)
        return jsonify(resultPackage)


# accepts: { 'crypto_cost_session': {token}, 'new password:' {password} }
# returns: { 'response string:' {Str}, 'response code:' {Int} }
@app.route("/resetPassword",  methods=['PATCH'])
def loginSubmit():
    if request.method == 'PATCH':




# accepts: json { 'crypto_cost_session': {token} }
# returns: json {'is user authorized': {Bool}, 'user id': {id}, 'response code:' {Int} }
@app.route("/authorizeUser",  methods=['POST'])
def authorizeUser():
    if request.method == 'POST':
        tokenCheckHandler = TokenCheckHandler()

        authTokenJson = request.get_json()
        authToken = str(authTokenJson['crypto_cost_session'])

        response = tokenCheckHandler.handleTokenCheck(authToken)
        return jsonify(response)
