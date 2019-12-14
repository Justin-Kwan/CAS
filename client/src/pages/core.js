const HTML_BAR = 0;
const RESULT_CODE = 1;

$(document).ready(function() {

  $('#submit_button').click(function() {
    console.log("CLICKED!");
    $("#login_form").submit();
  });

  $("#login_form").submit(function(event) {

    event.preventDefault(); //prevent default action
    let postUrl = 'http://127.0.0.1:5000/loginSubmit'
    let formData = $(this).serialize(); //Encode form elements for submission

    $.post(postUrl, formData, function(userAuthServerResponse) {
      console.log('SERVER RESPONSE: ' + userAuthServerResponse);
      $('#login_result_bar').replaceWith(userAuthServerResponse[HTML_BAR]);
    });

  });

});

doesTokenExist = (callback) => {

}

const getTokenCookie = (name) => {
  var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return v ? v[2] : null;
}

const makePostRequest = (url, formData, callback) => {
  $.post(postUrl, formData, callback);
}

const replaceComponent = (componentTag, newComponent) => {
  $(componentTag).replaceWith(newComponent);
}

const signupEmptyFields = `<div id="sign_up_result_bar" class="d-inline-flex alert alert-danger">
                            <strong>
                              Username or password is empty
                            </strong>
                           </div>`

const loginFieldsEmpty  = `<div id="login_result_bar" class="d-inline-flex alert alert-danger">
                            <strong>
                              Username or password is empty
                            </strong>
                           </div>`

const usernameBadLength = `<div id="sign_up_result_bar" class="d-inline-flex alert alert-danger">
                            <strong>
                              Sorry, your username must be 6 to 35 characters long!
                            </strong>
                           </div>`

const passwordBadLength = `<div id="sign_up_result_bar" class="d-inline-flex alert alert-danger">
                            <strong>
                              Sorry, your password must Be 8 to 65 characters long!
                            </strong>
                           </div>`

const usernameBadChars  = `<div id="sign_up_result_bar" class="d-inline-flex alert alert-danger">
                            <strong>
                              Sorry, your username can only contain letters and numbers!
                            </strong>
                           </div>`

const usernameExists    = `<div id="sign_up_result_bar" class="d-inline-flex alert alert-info">
                            <strong>
                              Sorry, that username already exists!
                            </strong>
                           </div>`

const badUsernamePassword = `<div id="login_result_bar" class="d-inline-flex alert alert-danger">
                                <strong>
                                  Sorry, invalid username or password
                                </strong>
                             </div>`

const successfulSignup    = `<div id="form_and_button" class="row">
                                <div class="col-6">
                                  <div class="img">
                                    <img src="../static/images/signup-img.png" style="width:100%; height:100%;">
                                  </div>
                                </div>
                                <div class="col-6">
                                    <br></br><br></br><br></br><br></br><br></br>
                                    <div class="d-inline-flex alert alert-success">
                                        <h2>Thanks for signing up</h2>
                                    </div>
                                    <br></br>
                                    <a href="http://127.0.0.1:5000/login">
                                      <button class="btn btn-primary">Login</button>
                                    </a>
                                </div>
                             </div>`
