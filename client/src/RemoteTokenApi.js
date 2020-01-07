'use strict';

const fetch = require('node-fetch');

class RemoteTokenApi {

  fetchAuthCheck(authToken) {
    const requestJson = JSON.stringify({
      "crypto_cost_session": authToken
    });

    var promise = new Promise(function(resolve, reject) {
      fetch('http://localhost:5000/authorizeUser', {
          method: 'POST',
          body: requestJson,
          headers: {
            'Content-Type': 'application/json'
          },
        })
        .then(function(serverResponse) {
          return serverResponse.json();
        })
        .then(function(serverResponseJson) {
          resolve(serverResponseJson['is user authorized']);
        })
        .catch(err => console.log(err));
    });
    return promise;
  }

}

module.exports = RemoteTokenApi;
