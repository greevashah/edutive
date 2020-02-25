window.onload = function () {
    var linechart = new CanvasJS.Chart("linechartContainer", {
        animationEnabled: true,
        theme: "light2",
        title:{
            text: "Simple Line Chart"
        },
        axisY:{
            includeZero: false
        },
        data: [{        
            type: "line",       
            dataPoints: [
                { y: 450 },
                { y: 414},
                { y: 520, indexLabel: "highest",markerColor: "red", markerType: "triangle" },
                { y: 460 },
                { y: 450 },
                { y: 500 },
                { y: 480 },
                { y: 480 },
                { y: 410 , indexLabel: "lowest",markerColor: "DarkSlateGrey", markerType: "cross" },
                { y: 500 },
                { y: 480 },
                { y: 510 }
            ]
        }]
    });
    linechart.render();
    
    var barchart = new CanvasJS.Chart("barchartContainer", {
        theme: "light1", // "light2", "dark1", "dark2"
        animationEnabled: true, // change to true		
        title:{
            text: "Correctness"
        },
          axisX: {
            title: "Topics"
        },
          axisY: {
            title: "Number of Questions"
        },
      toolTip:{
        shared: true
      },
        data: [
        {
            // Change type to "bar", "area", "spline", "pie",etc.
            type: "column",
              name: "Correct",
              showInLegend: true,
              color: "#3d8b3d",
            dataPoints: [
                { label: "TSD",  y: 10  },
                { label: "TW", y: 15  },
                { label: "SI", y: 25  },
                { label: "PPL",  y: 30  },
            ]
        },
         {
            // Change type to "bar", "area", "spline", "pie",etc.
            type: "column",
               name: "Incorrect",
               showInLegend: true,
               color: "#b52b27",
            dataPoints: [
                { label: "TSD",  y: 4  },
                { label: "TW", y: 10  },
                { label: "SI", y: 25  },
                { label: "PPL",  y: 30  },
            ]
        }
        ]
    });
    barchart.render();
    var donutchart = new CanvasJS.Chart("donutchartContainer", {
        exportEnabled: true,
        animationEnabled: true,
        title:{
            text: "State Operating Funds"
        },
        legend:{
            cursor: "pointer",
            itemclick: explodePie
        },
        data: [{
            type: "pie",
            showInLegend: true,
            toolTipContent: "{name}: <strong>{y}%</strong>",
            indexLabel: "{name} - {y}%",
            dataPoints: [
                { y: 26, name: "School Aid", exploded: true },
                { y: 20, name: "Medical Aid" },
                { y: 5, name: "Debt/Capital" },
                { y: 3, name: "Elected Officials" },
                { y: 7, name: "University" },
                { y: 17, name: "Executive" },
                { y: 22, name: "Other Local Assistance"}
            ]
        }]
    });
    donutchart.render();
}

function explodePie (e) {
	if(typeof (e.dataSeries.dataPoints[e.dataPointIndex].exploded) === "undefined" || !e.dataSeries.dataPoints[e.dataPointIndex].exploded) {
		e.dataSeries.dataPoints[e.dataPointIndex].exploded = true;
	} else {
		e.dataSeries.dataPoints[e.dataPointIndex].exploded = false;
	}
	e.donutchart.render();
}

var dataset=undefined;
var topicdataset=undefined;

function initialise(x, x1, x2){
    dataset= x;
    topicdataset=x1;
    testId= x2;
    // alert(typeof(dataset));
    // alert(ds)
    displayQuestionResult()
    displayTopicResult();
}

function displayQuestionResult(){
    // alert("Dataset is: ",dataset);
    // alert(dataset[0]);
    // alert(dataset[0][7]);
    qtable= document.getElementById("qtable-body");
    for(var i=1;i<=15;i++){
        qtable.innerHTML +="<tr><td>"+i+"</td><td>"+dataset[i-1][3]+"</td><td>"+dataset[i-1][4]+"</td><td>"+dataset[i-1][5]+"</td><td>"+dataset[i-1][6]+"</td><td>"+dataset[i-1][8]+"</td><td>"+dataset[i-1][9]+"</td></tr>";
    }
}
/* <th>Question No</th>
<th>Correctness</th>    answers
<th>Time Taken</th> elapsedTime  
<th>Option Changes</th> optionchanges
<th>Time Taken per topic</th>    totalTimeTaken
<th>Topic</th>
<th>Level</th> */

function displayTopicResult(){
    ttable= document.getElementById("ttable-body");
    for(var i=1;i<=15;i++){
        ttable.innerHTML +="<tr><td>"+i+"</td><td>"+topicdataset[i-1][2]+"</td><td>"+topicdataset[i-1][3]+"</td><td>"+topicdataset[i-1][4]+"</td><td>"+topicdataset[i-1][5]+"</td><td>"+topicdataset[i-1][6]+"</td><td>"+topicdataset[i-1][7]+"</td></tr>";
    }
}