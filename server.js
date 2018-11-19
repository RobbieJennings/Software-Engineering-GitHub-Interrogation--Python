var express = require('express');
var app = express();
const { spawn } = require("child_process");
var MongoClient = require('mongodb').MongoClient;

// Connect to the db
MongoClient.connect("mongodb://localhost:27017/github_database",
    { useNewUrlParser: true }, function (err, db) {

     if(err) throw err;

     //Write databse Insert/Update/Query code here..

});

var username = "RobbieJennings"
const pythonInitDB = spawn("python3",["initdb.py", username]);
pythonInitDB.stdout.on('data', (data) => {
    console.log(data.toString());
    const pythonAddUser = spawn("python3",["adduser.py", username]);
    pythonAddUser.stdout.on('data', (data) => {
        console.log(data.toString());
        const pythonRemoveUser = spawn("python3",["removeuser.py", username]);
        pythonRemoveUser.stdout.on('data', (data) => {
            console.log(data.toString());
            console.log("done")
        });
    });
});

app.get('/', function (req, res) {
    res.send('Hello World');
})

var server = app.listen(8080, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Sweng project listening at http://%s:%s", host, port)
})
