
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_cors import CORS
import os
import sys
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/domain-layer/handlers')
from SignUpHandler import SignUpHandler
from LoginHandler  import LoginHandler
from TokenCheckHandler import TokenCheckHandler
from PasswordResetHandler import PasswordResetHandler

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["40 per minute"]
)

# accepts: json { 'email': {email}, 'password': {password} }
# returns: json { 'response string': {Str}, 'response code': {Int} }
@app.route("/signupSubmit", methods=['POST'])
@limiter.limit("40 per minute")
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
@limiter.limit("40 per minute")
def loginSubmit():
    if request.method == 'POST':
        loginHandler = LoginHandler()

        signupFormJson = request.get_json()
        email = str(signupFormJson['email'])
        password = str(signupFormJson['password'])

        resultPackage = loginHandler.handleUserLogin(email, password)
        return jsonify(resultPackage)


# accepts: { 'crypto_cost_session': {token}, 'new password': {password} }
# returns: { 'response string:' {Str}, 'response code:' {Int} }
@app.route("/resetPassword",  methods=['PATCH'])
@limiter.limit("40 per minute")
def resetPassword():
    if request.method == 'PATCH':
        PRH = PasswordResetHandler()

        passwordResetJson = request.get_json()
        authToken = str(passwordResetJson['crypto_cost_session'])
        newTextPassword = str(passwordResetJson['new password'])

        response = PRH.handlePasswordReset(authToken, newTextPassword)
        return jsonify(response)


# accepts: json { 'crypto_cost_session': {token} }
# returns: json {'is user authorized': {Bool}, 'user id': {id}, 'response code:' {Int} }
@app.route("/authorizeUser",  methods=['POST'])
@limiter.limit("40 per minute")
def authorizeUser():
    if request.method == 'POST':
        tokenCheckHandler = TokenCheckHandler()
        authTokenJson = request.get_json(force=True)
        authToken = str(authTokenJson['crypto_cost_session'])
        response = tokenCheckHandler.handleTokenCheck(authToken)
        return jsonify(response)
