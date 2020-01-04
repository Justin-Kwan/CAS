/**
 *  router for serving static signup and login pages
 */

'use strict';

const express    = require('express');
const app        = express();
const cors       = require('cors');
const path       = require('path');
var cookieParser = require('cookie-parser');

const LOCAL_HOST = '127.0.0.1';
const PORT       = 5001;

/**
 * folder paths
 */
const cssFolderPath = express.static(path.join(__dirname, './assets/css'));
const pagesFolderPath = express.static(path.join(__dirname, './pages'));
const vendorFolderPath = express.static(path.join(__dirname, './vendor'));
const fontsFolderPath = express.static(path.join(__dirname, './assets/pulp-display-font'));
const imagesFolderPath = express.static(path.join(__dirname, './assets/images'));

/**
 * file paths
 */
const loginPage = path.join(__dirname, './pages/login.html');
const signupPage = path.join(__dirname, './pages/signup.html');

app.use(cors())
app.use(cookieParser());
app.use(cssFolderPath);
app.use(pagesFolderPath);
app.use(vendorFolderPath);
app.use(fontsFolderPath);
app.use(imagesFolderPath);

app.get('/login', function (req, res) {
  if (req.cookies['crypto_cost_session'] != undefined)
    res.redirect("http://127.0.0.1:8000/getPortfolio");
  else
    res.sendFile(loginPage);
})

app.get('/signup', function (req, res) {
  if(req.cookies['crypto_cost_session'] != undefined)
    res.redirect("http://127.0.0.1:8000/getPortfolio");
  else
    res.sendFile(signupPage);
});

app.listen(PORT, function() {
  console.log('User auth frontend server started at ' + LOCAL_HOST + ':' + PORT + '...');
});
