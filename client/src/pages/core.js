'use strict';

const THREE_HRS = 0.125

/**
 * submit button listeners
 */
$(document).ready(function() {
  $('#login_submit_button').click(function() {
    onLoginSubmit();
  });

  $('#signup_submit_button').click(function() {
    onSignupSubmit();
  });
});

async function onLoginSubmit() {
  document.getElementById("login_submit_button").disabled = true;
  console.log("login button clicked");
  const serverResponse = await makePostRequest('http://127.0.0.1:5000/loginSubmit', "#login_form");
  determineActionOnResponse(serverResponse['response code'], serverResponse['response string']);

  if(serverResponse['response code'] != 202) {
    document.getElementById("login_submit_button").disabled = false;
  }
}

async function onSignupSubmit() {
  document.getElementById("signup_submit_button").disabled = true;
  console.log("submit button clicked");
  const serverResponse = await makePostRequest('http://127.0.0.1:5000/signupSubmit', "#signup_form");
  determineActionOnResponse(serverResponse['response code'], serverResponse['response string']);
  document.getElementById("signup_submit_button").disabled = false;
}

function makePostRequest(url, formTag) {
  const formJson = JSON.stringify($(formTag).serializeJSON());

  $.ajaxSetup({
    contentType: "application/json; charset=utf-8"
  });

  var promise = new Promise(function(resolve, reject) {
    $.post(url, formJson, function(serverResponse) {
      resolve(serverResponse);
    });
  });

  return promise;
}

function determineActionOnResponse(responseCode, responseString) {
  console.log(responseCode);

  switch (responseCode) {
    case 400:
      if (responseString === "email empty") {
        replaceComponent("#signup_result_bar", signupEmailEmpty);
        replaceComponent("#login_result_bar", loginEmailEmpty);
      } else {
        replaceComponent("#signup_result_bar", signupPasswordEmpty);
        replaceComponent("#login_result_bar", loginPasswordEmpty);
      }
      break;
    case 401: // bad login credentials
      replaceComponent("#login_result_bar", emailPasswordWrong);
      break;
    case 402: // bad signup email/password length
      if (responseString === "email length bad")
        replaceComponent("#signup_result_bar", emailInvalid);
      else
        replaceComponent("#signup_result_bar", passwordBadLength);
      break;
    case 403: // bad signup email characters
      replaceComponent("#signup_result_bar", emailInvalid);
      break;
    case 404:
      replaceComponent("#signup_result_bar", emailExists);
      break;
    case 201:
      replaceComponent("#form_and_button", successfulSignup);
      break;
    default: // (case 202)
      setTokenCookie(responseString);
      redirectToApi("http://127.0.0.1:8000/getPortfolio");
      break;
  }
}

function setTokenCookie(authToken) {
  var expires = "";
  const date = new Date();
  date.setTime(date.getTime() + (THREE_HRS * 24 * 60 * 60 * 1000));
  expires = "; expires=" + date.toUTCString();
  document.cookie = "crypto_cost_session" + "=" + (authToken || "") + expires + "; path=/";
}

function redirectToApi(url) {
  window.location.href = url;
}

function replaceComponent(componentTag, newComponent) {
  $(componentTag).replaceWith(newComponent);
}

const signupEmailEmpty = `<div id="signup_result_bar" class="col-3 container text-center alert alert-danger">
                          <strong>Sorry, your email is empty!</strong></div>`;

const loginEmailEmpty = `<div id="login_result_bar" class="col-3 container text-center alert alert-danger">
                         <strong>Sorry, your email is empty!</strong></div>`;

const signupPasswordEmpty = `<div id="signup_result_bar" class="col-3 container text-center alert alert-danger">
                             <strong>Sorry, your password is empty!</strong></div>`;

const loginPasswordEmpty = `<div id="login_result_bar" class="col-3 container text-center alert alert-danger">
                            <strong>Sorry, your password is empty!</strong></div>`;

const passwordBadLength = `<div id="signup_result_bar" class="col-3 container text-center alert alert-danger">
                           <strong>Sorry, your password must Be 8 to 65 characters long!</strong>
                           </div>`;

const emailInvalid = `<div id="signup_result_bar" class="col-3 container text-center alert alert-danger">
                      <strong>Sorry, invalid email!</strong></div>`;

const emailExists = `<div id="signup_result_bar" class="col-3 container text-center alert alert-info">
                     <strong>Sorry, that email already exists!</strong></div>`;

const emailPasswordWrong = `<div id="login_result_bar" class="col-3 container text-center alert alert-danger">
                            <strong>Sorry, incorrect email or password</strong></div>`;

const successfulSignup = `<div id="form_and_button" class="row"><h2 class="col-3 container text-center">
                          Thanks for signing up</h2></div><br></br><a href="http://127.0.0.1:5001/login">
                          <div class="container text-center"><button class="btn btn-primary">Login</button>
                          </div></a></div></div>`;
