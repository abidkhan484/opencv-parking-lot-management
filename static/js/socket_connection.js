$(document).ready(function () {
  var socket = io.connect(
    "http://" + document.domain + ":" + location.port + "/availability"
  );

  //receive details from server
  socket.on("availability", function (msg) {
    // console.log("Received Occupied " + msg.occupied);
    // console.log("Received Available " + msg.available);
    $("#occupied").text(msg.occupied ?? msg.occupied);
    $("#available").text(msg.available ?? msg.occupied);
  });
});
