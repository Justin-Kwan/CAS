from flask import Flask, render_template, request, redirect, url_for, jsonify
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
from SignUpHandler      import SignUpHandler
from LoginHandler       import LoginHandler
from IndexReturnDecider import IndexReturnDecider

app = Flask(__name__)

'''
    signup routes
'''

@app.route("/signUpSuccess")
def signUpSuccess():
    return render_template('SignUpPages/SignUpSuccess.html')

@app.route("/signUpError=existingUsername")
def signUpExistingUsername():
    return render_template('SignUpPages/SignUpErrorExistingUsername.html')

@app.route("/signUpError=invalidUsernameCharacters")
def signUpInvalidUsernameCharacters():
    return render_template('SignUpPages/SignUpErrorInvalidUsernameCharacters.html')

@app.route("/signUpError=usernameOutOfRange")
def signUpUsernameOutOfRange():
    return render_template('SignUpPages/SignUpErrorUsernameOutOfRange.html')

@app.route("/signUpError=passwordOutOfRange")
def signUpPasswordOutOfRange():
    return render_template('SignUpPages/SignUpErrorPasswordOutOfRange.html')

@app.route("/signUpError=emptyFields")
def signUpEmptyFields():
    return render_template('SignUpPages/SignUpErrorEmptyFields.html')

@app.route("/signUp", methods=['GET'])
def signUp():
    return render_template('SignUpPages/SignUp.html')


@app.route("/signUpSubmit", methods=['POST'])
def signUpSubmit():
    if request.method == 'POST':
        signUpHandler = SignUpHandler()
        IRD = IndexReturnDecider()

        username = request.form['username']
        password = request.form['password']

        resultCode = signUpHandler.handleUserSignUp(username, password)
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

        username = request.form['username']
        password = request.form['password']

        # list of token and result code returned if successful
        resultPackage = loginHandler.handleUserLogin(username, password)
        isTokenReturned = IRD.checkIfTokenReturned(resultPackage[1])

        if isTokenReturned:
            securityToken = resultPackage[0]
            # return a json web security token
            return jsonify({
                'success': 'true',
                'token': securityToken
            })
        else:
            # determine redirect page using result code
            redirectPage = IRD.determineLoginRedirectPage(resultPackage[1])
            return redirect(url_for(redirectPage))
