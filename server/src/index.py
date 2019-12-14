
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
from SignUpHandler import SignUpHandler
from LoginHandler  import LoginHandler

RESPONSE_CODE   = 1
RESPONSE_STRING = 0

app = Flask(__name__)

@app.route("/signUpSubmit", methods=['POST'])
def signUpSubmit():

    if request.method == 'POST':
        signUpHandler = SignUpHandler()

        username = request.form['username']
        password = request.form['password']

        resultPackage = signUpHandler.handleUserSignUp(username, password)
        print("Response String: ", resultPackage[RESPONSE_STRING])
        print("Response Code: ", resultPackage[RESPONSE_CODE])
        return resultPackage[RESPONSE_STRING], resultPackage[RESPONSE_CODE]

@app.route("/loginSubmit",  methods=['POST'])
def loginSubmit():

    if request.method == 'POST':
        loginHandler = LoginHandler()

        username = request.form['username']
        password = request.form['password']

        resultPackage = loginHandler.handleUserLogin(username, password)
        print("Response String: ", resultPackage[RESPONSE_STRING])
        print("Response Code: ", resultPackage[RESPONSE_CODE])
        return resultPackage[RESPONSE_STRING], resultPackage[RESPONSE_CODE]
