'use strict';

class HtmlUpdateHandler {

  constructor() {
    this.SUCCESS_USER_SIGN_UP  = 201;
    this.ERROR_USER_SIGN_UP    = 202;
  }

  // returns id tag of html component to update
  determineComponentToUpdate(responseStatusCode, requestType) {

    if(requestType == 'SIGN_UP_REQUEST') {

      if(responseStatusCode == this.SUCCESS_USER_SIGN_UP) {
        return 'sign-up-page-body'
      }
      else if(responseStatusCode == this.ERROR_USER_SIGN_UP) {
        return 'sign-up-page-info-bar'
      }

    }
    // else if(requestType == 'LOGIN') {
    // }
  }

  updateComponent(componentToUpdate, newComponentHtml) {

    document.getElementById(componentToUpdate).innerHTML = newComponentHtml;

  }



}
