# @author: Justin Kwan

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from SignUpHandler      import SignUpHandler
from LoginHandler       import LoginHandler
from IndexReturnDecider import IndexReturnDecider
from HtmlInfoBars       import HtmlInfoBars
from ResultCodes        import ResultCodes

RESULT_CODE = 1
SECURITY_TOKEN = 0

htmlInfoBars = HtmlInfoBars()
resultCodes  = ResultCodes()

app = Flask(__name__)

'''
    signup routes
'''

@app.route("/signUpSuccess")
def signUpSuccess():
    return htmlInfoBars.SUCCESS, resultCodes.HTTP_201_CREATED

@app.route("/signUpError=existingUsername")
def signUpExistingUsername():
    return htmlInfoBars.ERROR_DUPLICATE_USERNAME, resultCodes.HTTP_203_NON_AUTHORITATIVE_INFORMATION

@app.route("/signUpError=invalidUsernameCharacters")
def signUpInvalidUsernameCharacters():
    return htmlInfoBars.ERROR_INVALID_USERNAME_CHARS, resultCodes.HTTP_203_NON_AUTHORITATIVE_INFORMATION

@app.route("/signUpError=usernameOutOfRange")
def signUpUsernameOutOfRange():
    return htmlInfoBars.ERROR_USERNAME_LENGTH_INVALID, resultCodes.HTTP_203_NON_AUTHORITATIVE_INFORMATION

@app.route("/signUpError=passwordOutOfRange")
def signUpPasswordOutOfRange():
    return htmlInfoBars.ERROR_PASSWORD_LENGTH_INVALID, resultCodes.HTTP_203_NON_AUTHORITATIVE_INFORMATION

@app.route("/signUpError=emptyFields")
def signUpEmptyFields():
    return htmlInfoBars.ERROR_EMPTY_FIELDS, resultCodes.HTTP_203_NON_AUTHORITATIVE_INFORMATION

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

            # return a json web security token
            return jsonify({
                'success': 'true',
                'token': securityToken
            })
        else:
            redirectPage = IRD.determineLoginRedirectPage(resultPackage[RESULT_CODE])
            return redirect(url_for(redirectPage))
