from flask import Flask, render_template, request, redirect, url_for
from InputHandler import InputHandler

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

@app.route("/signUp", methods=['POST'])
def signUp():
    if(request.method == 'POST'):
        inputHandler = InputHandler()
        processResult = inputHandler.handleUserInput(request.form['username'], request.form['password'])
        redirectPage = determineRedirectPage(processResult)
        return redirect(url_for(redirectPage))

def determineRedirectPage(processResult):
    if(processResult == 'SUCCESS'):
        return 'success'
    elif(processResult == 'DUPLICATE_USERNAME'):
        return 'existingUsername'
    elif(processResult == 'INVALID_USERNAME_CHARS'):
        return 'invalidUsernameCharacters'
    else:
        return 'emptyFields'

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
