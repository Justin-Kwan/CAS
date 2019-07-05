

let responseStatusCode;
let signUpForm = document.getElementById('signUpForm')

signUpForm.addEventListener('submit', function(event) {

  event.preventDefault();

  let formData = new FormData(this);

  fetch('http://127.0.0.1:5000/signUpSubmit', {
    method: 'post',
    body: formData
  })
    .then(function(response) {

      responseStatusCode = response.status;
      return response.text();


    }).then(function(text) {

        console.log('server status code: ' + responseStatusCode)

        if(responseStatusCode == 201) {
          document.getElementById("sign-up-body").innerHTML = text;
        }
        else if(responseStatusCode == 203) {
          document.getElementById("sign-up-info-bar").innerHTML = text;
        }

    }).catch(function(error) {
      console.error(error);
    })

});
