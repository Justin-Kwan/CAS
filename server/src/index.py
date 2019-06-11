from flask import Flask, render_template, request, redirect, url_for
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/controllers')
from SignUpController import SignUpController

app = Flask(__name__)

@app.route("/success")
def success():
    return render_template('Success.html')

@app.route("/error=emptyFields")
def emptyFields():
    return render_template('ErrorEmptyFieldsSignUp.html')

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

@app.route("/signUpSubmit", methods=['POST'])
def signUpSubmit():
    if(request.method == 'POST'):
        signUpController = SignUpController()
        processResult = signUpController.handleUserSignUp(request.form['username'], request.form['password'])
        redirectPage = determineSignUpRedirectPage(processResult)
        return redirect(url_for(redirectPage))

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
        return 'emptyFields'
