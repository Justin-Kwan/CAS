# @author: Justin Kwan

from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from SignUpHandler      import SignUpHandler
from LoginHandler       import LoginHandler
from IndexReturnDecider import IndexReturnDecider
from ResultCodes        import ResultCodes

RESULT_CODE = 1
AUTH_TOKEN  = 0
THREE_HOURS = 10800  # 3hrs in secs

resultCodes = ResultCodes()

app = Flask(__name__)

'''
    signup routes
'''

@app.route("/signUpSuccess")
def signUpSuccess():
    return render_template('SignUpPages/SignUpSuccess.html'), resultCodes.SUCCESS_USER_SIGN_UP

@app.route("/signUpError=existingUsername")
def signUpExistingUsername():
    return render_template('SignUpPages/SignUpErrorExistingUsername.html'), resultCodes.ERROR_USER_SIGN_UP

@app.route("/signUpError=invalidUsernameCharacters")
def signUpInvalidUsernameCharacters():
    return render_template('SignUpPages/SignUpErrorInvalidUsernameCharacters.html'), resultCodes.ERROR_USER_SIGN_UP

@app.route("/signUpError=usernameOutOfRange")
def signUpUsernameOutOfRange():
    return render_template('SignUpPages/SignUpErrorUsernameOutOfRange.html'), resultCodes.ERROR_USER_SIGN_UP

@app.route("/signUpError=passwordOutOfRange")
def signUpPasswordOutOfRange():
    return render_template('SignUpPages/SignUpErrorPasswordOutOfRange.html'), resultCodes.ERROR_USER_SIGN_UP

@app.route("/signUpError=emptyFields")
def signUpEmptyFields():
    return render_template('SignUpPages/SignUpErrorEmptyFields.html'), resultCodes.ERROR_USER_SIGN_UP

@app.route("/signUp", methods=['GET'])
def signUp():
    return render_template('SignUpPages/SignUp.html'), resultCodes.HTTP_200_OK

@app.route("/signUpSubmit", methods=['POST'])
def signUpSubmit():

    if request.method == 'POST':
        signUpHandler = SignUpHandler()
        IRD = IndexReturnDecider()

        enteredUsername = request.form['username']
        enteredPassword = request.form['password']

        resultCode = signUpHandler.handleUserSignUp(enteredUsername, enteredPassword)
        redirectPage = IRD.determineSignUpRedirectPage(resultCode)
        return redirect(url_for(redirectPage))

'''
    login routes
'''

@app.route("/login", methods=['GET'])
def login():
    return render_template('LoginPages/Login.html')

@app.route("/loginError=emptyFields")
def loginEmptyFields():
    return render_template('LoginPages/LoginErrorEmptyFields.html')

@app.route("/loginError=invalidUsernameOrPassword")
def loginInvalidUsernameOrPassword():
    return render_template('LoginPages/LoginErrorInvalidUsernamePassword.html')

@app.route("/loginSubmit",  methods=['POST'])
def loginSubmit():
    if request.method == 'POST':
        loginHandler = LoginHandler()
        IRD = IndexReturnDecider()

        enteredUsername = request.form['username']
        enteredPassword = request.form['password']

        # list of token and result code is returned if successful
        resultPackage = loginHandler.handleUserLogin(enteredUsername, enteredPassword)
        isTokenReturned = IRD.checkIfTokenReturned(resultPackage[RESULT_CODE])

        if isTokenReturned:
            securityToken = resultPackage[SECURITY_TOKEN]

            '''redirect to other service url'''
            response = make_response(redirect('http://127.0.0.1:8000/createPortfolio'))
            response.set_cookie('security_token', securityToken, max_age = THREE_HOURS)
            return response
        else:
            redirectPage = IRD.determineLoginRedirectPage(resultPackage[RESULT_CODE])
            return redirect(url_for(redirectPage))
