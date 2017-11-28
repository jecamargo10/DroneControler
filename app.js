"use strict";


var express = require('express');
var bebop = require('node-bebop');
var fs = require("fs");


var output = fs.createWriteStream("./video.h264"),
    drone = bebop.createClient(),
    video = drone.getVideoStream();
    video.pipe(output);


var  cantidad= 1;
var app = express();
app.get('/', function (req, res) {
  res.send('Hello World!');
});

app.post('/subscription', function(req, res){
    res.setHeader('Content-Type', 'application/json');

  console.log("MESSAGE ARRIVED")
  console.log(cantidad)
  cantidad = cantidad + 1;

if (cantidad === 3)
{
    console.log("dron Time")

    drone.connect(function() {
      drone.MediaStreaming.videoEnable(1);
      drone.takeOff();

      setTimeout(function() {
        drone.stop();
      }, 5000);

      setTimeout(function() {
        drone.up(20);
      }, 7000);

      setTimeout(function() {
        drone.stop();
      }, 12000);

      setTimeout(function() {
        drone.forward(30);
      }, 14000);

      setTimeout(function() {
        drone.stop();
      }, 17000);

      setTimeout(function() {
        drone.clockwise(30);
      }, 20000);

      setTimeout(function() {
        drone.stop();
      }, 22000);

      setTimeout(function() {
        drone.forward(30);
      }, 23000);

      setTimeout(function() {
        drone.stop();
      }, 30000);

      setTimeout(function() {
        drone.clockwise(30);
      }, 37000);

      setTimeout(function() {
        drone.stop();
      }, 41000);

      setTimeout(function() {
        drone.forward(30);
      }, 42000);

      setTimeout(function() {
        drone.stop();
      }, 48000);

      setTimeout(function() {
        drone.counterClockwise(30);
      }, 50000);

      setTimeout(function() {
        drone.stop();
      }, 52500);

      setTimeout(function() {
        drone.forward(30);
      }, 54000);

      setTimeout(function() {
        drone.stop();
      }, 59000);

      setTimeout(function() {
        drone.land();
      }, 61000);

    });





}
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});
