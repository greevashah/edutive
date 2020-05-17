var testdataset= undefined;
window.onload = function () {
    console.log('hello from profile side :P');
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
                { y: 450 },
                { y: 414},
                { y: 520},
                { y: 460 },
                { y: 450 },
                { y: 410 , indexLabel: "Latest",markerColor: "red", markerType: "triangle" },
            ]
        }]
    });
    for(var i=0;i<6;i++){
        linechart.options.data[0].dataPoints[i].y=testdataset[6-i-1][4];
    }
    linechart.render();

}

function initialise(x){
    testdataset=x; 

       
}