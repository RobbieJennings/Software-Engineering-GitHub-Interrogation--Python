var express = require('express');
var app = express();
var fs = require('fs');
const { spawn } = require("child_process");
var MongoClient = require('mongodb').MongoClient;

function getCollection(collection) {
    MongoClient.connect("mongodb://localhost:27017/github_database",
        { useNewUrlParser: true }, function (err, db) {
         if(err) throw err;
         var collection = db.collection(collection);
         return collection.find().toArray()
    });
}

app.get('/', function (req, res) {
    const pythonInitDB = spawn("python3",["initdb.py"]);
    pythonInitDB.stdout.on('data', (data) => {
        console.log(data.toString());
        fs.readFile('home.html', function(err, data){
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data);
            return res.end();
        })
    })
})

app.get('/adduser', function (req, res) {
    var username = req.query.username;
    console.log(username)
    var pythonAddUser = spawn("python3",["adduser.py", username]);
    pythonAddUser.stdout.on('data', (data) => {
        console.log(data.toString());
        fs.readFile('stats.html', function(err, data){
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data);
            return res.end();
        })
    })
})

app.get('/removeuser', function (req, res) {
    var username = req.query.username;
    console.log(username)
    const pythonRemoveUser = spawn("python3",["removeuser.py", username]);
    pythonRemoveUser.stdout.on('data', (data) => {
        console.log(data.toString());
        fs.readFile('stats.html', function(err, data){
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data);
            return res.end();
        })
    })
})

var server = app.listen(8080, function () {
   var host = server.address().address
   var port = server.address().port
   console.log("Sweng project listening at http://%s:%s", host, port)
})
