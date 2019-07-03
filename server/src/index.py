from flask import Flask, render_template, request, redirect, url_for, jsonify
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/controllers')
from SignUpController import SignUpController
from LoginController  import LoginController

app = Flask(__name__)

'''
    signup routes
'''

@app.route("/success")
def success():
    return render_template('Success.html')

@app.route("/error=existingUsername")
def existingUsername():
    return render_template('ErrorExistingUsernameSignUp.html')

@app.route("/error=invalidUsernameCharacters")
def invalidUsernameCharacters():
    return render_template('ErrorInvalidUsernameCharacters.html')

@app.route("/error=usernameOutOfRange")
def usernameOutOfRange():
    return render_template('ErrorUsernameOutOfRange.html')

@app.route("/error=passwordOutOfRange")
def passwordOutOfRange():
    return render_template('ErrorPasswordOutOfRange.html')

@app.route("/signUp", methods=['GET'])
def signUp():
    return render_template('SignUp.html')

@app.route("/error=emptySignUpFields")
def emptySignUpFields():
    return render_template('ErrorEmptyFieldsSignUp.html')


@app.route("/signUpSubmit", methods=['POST'])
def signUpSubmit():
    if(request.method == 'POST'):
        signUpController = SignUpController()
        processResult = signUpController.handleUserSignUp(request.form['username'], request.form['password'])
        redirectPage = determineSignUpRedirectPage(processResult)
        return redirect(url_for(redirectPage))

'''
    login routes
'''

@app.route("/login", methods=['GET'])
def login():
    return render_template('Login.html')

@app.route("/error=emptyLoginFields")
def emptyLoginFields():
    return render_template('ErrorEmptyFieldsLogin.html')

@app.route("/error=invalidUsernameOrPassword")
def invalidUsernameOrPasswordLogin():
    return render_template('ErrorInvalidUsernamePassword.html')

@app.route("/loginSubmit",  methods=['POST'])
def loginSubmit():
    if(request.method == 'POST'):

        print("POST DATA!!!")

        loginController = LoginController()
        processResult = loginController.handleUserLogin(request.form['username'], request.form['password'])

        if(processResult == 'EMPTY_USERNAME' or processResult == 'EMPTY_PASSWORD' or processResult == 'EMPTY_FIELDS'):
            return redirect(url_for('emptyLoginFields'))
        elif(processResult == 'INVALID_USERNAME_OR_PASSWORD'):
            return redirect(url_for('invalidUsernameOrPasswordLogin'))

        # return a json web security token
        return jsonify({
            'success' : 'true',
            'token' : processResult
        })

def determineSignUpRedirectPage(processResult):
    if(processResult == 'SUCCESS'):
        return 'success'
    elif(processResult == 'DUPLICATE_USERNAME'):
        return 'existingUsername'
    elif(processResult == 'INVALID_USERNAME_CHARS'):
        return 'invalidUsernameCharacters'
    elif(processResult == 'INVALID_USERNAME_LENGTH'):
        return 'usernameOutOfRange'
    elif(processResult == 'INVALID_PASSWORD_LENGTH'):
        return 'passwordOutOfRange'
    else:
        return 'emptySignUpFields'
