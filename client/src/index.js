/**
 *  router for serving static signup and login pages
 */
 
'use strict';

const express    = require('express');
const app        = express();
const cors       = require('cors')
const path       = require('path');

const LOCAL_HOST = '127.0.0.1';
const PORT       = 5001;

/**
 * folder paths
 */
const assetsFolderPath = express.static(path.join(__dirname, './assets'));

/**
 * file paths
 */
 const loginPage = path.join(__dirname, './pages/login.html');
 const signupPage = path.join(__dirname, './pages/signup.html');

app.use(cors())
app.use(assetsFolderPath);

app.get('/login', function (req, res) {
  res.sendFile(loginPage);
})

app.get('/signup', function (req, res) {
  res.sendFile(signupPage);
})

app.listen(PORT, function() {
  console.log('Frontend server started at ' + LOCAL_HOST + ':' + PORT + '...');
});
