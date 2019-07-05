'use strict';

const httpRequestMaker  = new HttpRequestMaker();
const htmlUpdateHandler = new HtmlUpdateHandler();

class FormSubmitHandler {

  listenForSignUp() {

    const signUpPageForm = document.getElementById('sign-up-page-form');

    signUpPageForm.addEventListener('submit', function(event) {

      event.preventDefault();
      const formData = new FormData(this);

      httpRequestMaker.requestSignUp(formData, function(newComponentHtml, responseStatusCode) {
        const componentToUpdate = htmlUpdateHandler.determineComponentToUpdate(responseStatusCode, 'SIGN_UP_REQUEST');
        document.getElementById('sign-up-page-form').reset();
        htmlUpdateHandler.updateComponent(componentToUpdate, newComponentHtml);
      });

    });

  }

}

const formSubmitHandler = new FormSubmitHandler();

formSubmitHandler.listenForSignUp();
