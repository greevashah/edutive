var testdataset= undefined;
var len=undefined;
// var document= undefined;
var countDownDate = new Date("Nov 29, 2020 ").getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
    
  // Find the distance between now and the count down date
  var distance = countDownDate - now;
    
  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
//   var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
//   var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
//   var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
  // Output the result in an element with id="demo"
  document.getElementById("demo").innerHTML = days ;
    
  // If the count down is over, write some text 
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("demo").innerHTML = "EXPIRED";
  }
}, 1000);


$(document).ready(function () {
    $('#dtBasicExample').DataTable();
    $('.dataTables_length').addClass('bs-select');
  });


window.onload = function () {
    var linechart = new CanvasJS.Chart("linechartContainer", {
        animationEnabled: true,
        exportEnabled: true,
        theme: "light2",
        title:{
            text: "Test Score"
        },
        axisY:{
            includeZero: false
        },
        data: [{        
            type: "line",       
            dataPoints: [
                { y: null},
                { y: null},
                { y: null},
                { y: null},
                { y: null},
                { y: null }
            ]
        }]
    });

    for(var i=0 ; i < len;i++){
        linechart.options.data[0].dataPoints[i].y = testdataset[len-i-1][4];
    }
    // indexLabel: "Latest",markerColor: "red", markerType: "triangle"
    linechart.options.data[0].dataPoints[len-1].indexLabel = "Latest";
    linechart.options.data[0].dataPoints[len-1].markerColor = "red";
    linechart.options.data[0].dataPoints[len-1].markerType = "triangle";
    linechart.render();
}

function initialise(x){
    testdataset=x; 
    len= testdataset.length;
    if(len > 6)
        len = 6;
}