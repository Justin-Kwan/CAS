'use strict';


class HttpRequestMaker {

  async requestSignUp(formData, callback) {

      const response = await fetch('http://127.0.0.1:5000/signUpSubmit', {
        method: 'post',
        body: formData
      });

      const newComponentHtml = await response.text();
      const responseStatusCode = await response.status;

      console.log('server status code: ' + responseStatusCode);

      if(callback) {
        callback(newComponentHtml, responseStatusCode);
      }

  }


}
