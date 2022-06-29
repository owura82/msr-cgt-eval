const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();

body = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>HTML 5 Boilerplate</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
	<script src="index.js"></script>
    <h1>Test heading here!!</h1>
    <h2 id='holder'></h2>
    <button type="button" id="next-button">Click here for next line</button>
  </body>
</html>`

// your code goes here!
app.get('/', function(req, res){
    // res.send(body)
   
    const resp  = fs.readFileSync('temp.txt', 'utf-8');
    console.log(typeof resp)

    res.send(resp)

});

// app.get('/books', function(req, res){


// });

// app.get('/books-new', function(req, res){
   
// });

// app.post('/books-new', function(req, res){
   

// });


app.listen(3000);