var testdataset= undefined;
var len=undefined;

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