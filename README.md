# Central-Authorization-Service
A generic central authentication service (CAS) that supports user sign-up and login &amp; and request validation, built with Python Flask and JWT

## Available API Routes

  Here are the current routes, as I'll be adding more features in the future!

### localhost:5000/signupSubmit

        HTTP Request Type: POST
        Accepts (JSON): { 'email': {email string}, 'password': {password string} }
        Returns (JSON): { 'response': {string}, 'status': {integer} }

### localhost:5000/loginSubmit

        HTTP Request Type: POST
        Accepts (JSON): { 'email': {email string}, 'password': {password string} }
        Returns (JSON): { 'token': {string}, 'status': {integer} }

### localhost:5000/resetPassword

        HTTP Request Type: PATCH
        Accepts (JSON): { 'crypto_cost_session': {token string}, 'new password': {password string} }
        Returns (JSON): { 'response string': {string}, 'response code': {integer} }

### localhost:5000/authorizeUser

        HTTP Request Type: POST
        Accepts (JSON): { 'token': {string} }
        Returns (JSON): { 'is_user_authorized': {boolean}, 'user_id': {string}, 'response code:' {integer} }

## JSON Web Token Implementation

Issued JSON web token payloads are of the form:

        {
          'email': {email string},
          'user id': {id string},
          'exp': {expiry date integer}
        }
