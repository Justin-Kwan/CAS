from flask import Flask, render_template, request, redirect, url_for
from InputHandler import InputHandler

app = Flask(__name__)

@app.route("/success")
def success():
    return render_template('Success.html')

@app.route("/emptyFields")
def emptyFields():
    return render_template('ErrorEmptyFieldsSignUp.html')

@app.route("/existingUsername")
def existingUsername():
    return render_template('ErrorExistingUsernameSignUp.html')

@app.route("/signUp", methods=['POST'])
def signUp():
    if(request.method == 'POST'):

        print(request.form['username'], request.form['password'])

        inputHandler = InputHandler()
        processResult = inputHandler.handleUserInput(request.form['username'], request.form['password'])

        redirectPage = None
        
        if(processResult == 'SUCCESS'):
            redirectPage = 'success'
        elif(processResult == 'DUPLICATE_USERNAME'):
            redirectPage = 'existingUsername'
        else:
            redirectPage = 'emptyFields'
        return redirect(url_for(redirectPage))

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
