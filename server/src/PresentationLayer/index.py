# @author: Justin Kwan

from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from HtmlResultBars     import HtmlResultBars
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

resultCodes    = ResultCodes()
htmlResultBars = HtmlResultBars()

app = Flask(__name__)

'''
    signup routes
'''

@app.route("/signUpSuccess")
def signUpSuccess():
    print("SUCCESS", resultCodes.SUCCESS_USER_SIGN_UP)
    return jsonify([htmlResultBars.signUpSuccess, resultCodes.SUCCESS_USER_SIGN_UP])

@app.route("/signUpError=existingUsername")
def signUpExistingUsername():
    return jsonify([htmlResultBars.existingUsername, resultCodes.ERROR_USER_SIGN_UP])

@app.route("/signUpError=invalidUsernameCharacters")
def signUpInvalidUsernameCharacters():
    return jsonify([htmlResultBars.invalidUsernameChars, resultCodes.ERROR_USER_SIGN_UP])

@app.route("/signUpError=usernameOutOfRange")
def signUpUsernameOutOfRange():
    return jsonify([htmlResultBars.usernameOutOfRange, resultCodes.ERROR_USER_SIGN_UP])

@app.route("/signUpError=passwordOutOfRange")
def signUpPasswordOutOfRange():
    return jsonify([htmlResultBars.passwordOutOfRange, resultCodes.ERROR_USER_SIGN_UP])

@app.route("/signUpError=emptyFields")
def signUpEmptyFields():
    return jsonify([htmlResultBars.signupEmptyFields, resultCodes.ERROR_USER_SIGN_UP])

@app.route("/signUp", methods=['GET'])
def signUp():
    return render_template('SignUp.html'), resultCodes.HTTP_200_OK

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
    # if already a token in user's browser when requesting login, redirect to
    # crud service
    if 'auth_token' in request.cookies:
        response = make_response(redirect('http://127.0.0.1:8000/getPortfolio'))
        return response
    else:
        return render_template('Login.html')

@app.route("/loginError=emptyFields")
def loginEmptyFields():
    return jsonify([htmlResultBars.loginEmptyFields, resultCodes.ERROR_USER_SIGN_UP])

@app.route("/loginError=invalidUsernameOrPassword")
def loginInvalidUsernameOrPassword():
    return jsonify([htmlResultBars.invalidUsernamePassword, resultCodes.ERROR_USER_SIGN_UP])

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
            authToken = resultPackage[AUTH_TOKEN]
            # redirect to other service url
            response = make_response(redirect('http://127.0.0.1:8000/getPortfolio'))
            response.set_cookie('auth_token', authToken, max_age = THREE_HOURS)
            return response
        else:
            redirectPage = IRD.determineLoginRedirectPage(resultPackage[RESULT_CODE])
            return redirect(url_for(redirectPage))
