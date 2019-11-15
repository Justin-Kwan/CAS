
class HtmlResultBars():

    signupEmptyFields       = '<div id="sign_up_result_bar" class="d-inline-flex alert alert-danger"><strong>Username or password is empty</strong></div>'
    usernameOutOfRange      = '<div id="sign_up_result_bar" class="d-inline-flex alert alert-danger"><strong>Sorry, your username must be 6 to 35 characters long!</strong></div>'
    passwordOutOfRange      = '<div id="sign_up_result_bar" class="d-inline-flex alert alert-danger"><strong>Sorry, your password must Be 8 to 65 characters long!</strong></div>'
    invalidUsernameChars    = '<div id="sign_up_result_bar" class="d-inline-flex alert alert-danger"><strong>Sorry, your username can only contain letters and numbers!</strong></div>'
    existingUsername        = '<div id="sign_up_result_bar" class="d-inline-flex alert alert-info"><strong>Sorry, that username already exists!</strong></div>'
    signUpSuccess           = '<div id="form_and_button" class="row"><div class="col-6"><div class="img"><img src="../static/images/signup-img.png" style="width:100%; height:100%;"></div></div><div class="col-6"><br></br><br></br><br></br><br></br><br></br><div class="d-inline-flex alert alert-success"><h2>Thanks for signing up</h2></div><br></br><a href="http://127.0.0.1:5000/login"><button class="btn btn-primary">Login</button></a></div></div>'
    invalidUsernamePassword = '<div id="login_result_bar" class="d-inline-flex alert alert-danger"><strong>Sorry, invalid username or password</strong></div>'
    loginEmptyFields        = '<div id="login_result_bar" class="d-inline-flex alert alert-danger"><strong>Username or password is empty</strong></div>'
