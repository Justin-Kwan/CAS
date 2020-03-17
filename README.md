# Central-Authorization-Service
A generic central authentication service (CAS) that supports user sign-up and login &amp; and request validation, built with Python Flask and JWT

## Available API Routes

  Here are the current routes, as I'll be adding more features in the future!

### localhost:5000/signupSubmit

        HTTP Request Type: POST
        Accepts (JSON): { 'email': {email string}, 'password': {password string} }
        Returns (JSON): { 'response string': {response string}, 'response code': {integer} }

### localhost:5000/loginSubmit

        HTTP Request Type: POST
        Accepts (JSON): { 'email': {email string}, 'password': {password string} }
        Returns (JSON): { 'response string': {response string (on error) or token (on success)}, 'response code': {integer} }

### localhost:5000/resetPassword

        HTTP Request Type: PATCH
        Accepts (JSON): { 'crypto_cost_session': {token string}, 'new password': {password string} }
        Returns (JSON): { 'response string': {response string}, 'response code': {integer} }

### localhost:5000/authorizeUser

        HTTP Request Type: POST
        Accepts (JSON): { 'crypto_cost_session': {token string} }
        Returns (JSON): { 'is user authorized': {boolean}, 'user id': {id string}, 'response code:' {integer} }

## JSON Web Token Implementation

Issued JSON web token payloads are of the form:

        {
          'email': {email string},
          'user id': {id string},
          'exp': {expiry date integer}
        }
