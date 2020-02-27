var donutchart=undefined;
var dataset=undefined;
var topicdataset=undefined;
var testdataset= undefined;

window.onload = function () {
    var linechart = new CanvasJS.Chart("linechartContainer", {
        animationEnabled: true,
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
                { label: "TSD",  y: 0  },
                { label: "TW", y: 0  },
                { label: "SI", y: 0  },
                { label: "PPL",  y: 0  },
            ]
        },
         {
            // Change type to "bar", "area", "spline", "pie",etc.
            type: "column",
               name: "Incorrect",
               showInLegend: true,
               color: "#b52b27",
            dataPoints: [
                { label: "TSD",  y: 0  },
                { label: "TW", y: 0  },
                { label: "SI", y: 0  },
                { label: "PPL",  y: 0  },
            ]
        }
        ]
    });
    for(var i=0;i<4;i++){
        barchart.options.data[0].dataPoints[i].y=topicdataset[i][7];
        barchart.options.data[1].dataPoints[i].y=topicdataset[i][8];
    }
    barchart.render();

    var donutchart = new CanvasJS.Chart("donutchartContainer", {
        exportEnabled: true,
        animationEnabled: true,
        title:{
            text: "Time of Entire Test"
        },
        legend:{
            cursor: "pointer",
            itemclick: explodePie
        },
        data: [{
            type: "pie",
            showInLegend: true,
            toolTipContent: "{name}: <strong>{y}secs</strong>",
            indexLabel: "{name} - {y}secs",
            dataPoints: [
                { y:0 , name: "TSD", exploded: true },
                { y:0 , name: "TW" },
                { y:0 , name: "SI" },
                { y:0, name: "PPL" }
            ]
        }]
    });
    for(var i=0;i<4;i++){
        donutchart.options.data[0].dataPoints[i].y=topicdataset[i][6];
    }
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

function initialise(x, x1, x2, x3){
    dataset= x;
    topicdataset=x1;
    testdataset=x2;     //testdataset
    testId= x3;
    // alert(typeof(dataset));
    alert(testdataset)
    displayQuestionResult();
    displayTopicResult();
    displayStatistics();
}

function displayQuestionResult(){
    // alert("Dataset is: ",dataset);
    // alert(dataset[0]);
    // alert(dataset[0][2]);
    qtable= document.getElementById("qtable-body");
    for(var i=1;i<=15;i++){
        qtable.innerHTML +="<tr><td>"+i+"</td><td>"+dataset[i-1][3]+"</td><td>"+dataset[i-1][4]+"</td><td>"+dataset[i-1][5]+"</td><td>"+dataset[i-1][6]+"</td><td>"+dataset[i-1][8]+"</td><td>"+dataset[i-1][9]+"</td></tr>";
    }
}
/* 
<th>Question No</th>
<th>Correctness</th>    answers
<th>Time Taken</th> elapsedTime  
<th>Option Changes</th> optionchanges
<th>Time Taken per topic</th>    totalTimeTaken
<th>Topic</th>
<th>Level</th> */

function displayTopicResult(){
    ttable= document.getElementById("ttable-body");
    // alert(topicdataset[1][2]);
    for(var i=1;i<=4;i++){
        ttable.innerHTML +="<tr><td>"+i+"</td><td>"+topicdataset[i-1][2]+"</td><td>"+topicdataset[i-1][3]+"</td><td>"+topicdataset[i-1][4]+"</td><td>"+topicdataset[i-1][5]+"</td><td>"+topicdataset[i-1][6]+"</td><td>"+topicdataset[i-1][7]+"</td><td>"+topicdataset[i-1][8]+"</td><td>"+topicdataset[i-1][9]+"</td><td>"+topicdataset[i-1][10]+"</td></tr>";
    }
}
/*
<th>Id</th>
<th>Topic</th>    
<th>Correctness</th>   
<th>Time Taken per Question</th>
<th>Option Changes</th>
<th>Time Taken per Topic</th>
<th>Correct Questions</th>
<th>Incorrect Questions</th>
<th>Topic Score</th>
<th>Time Taken per Test</th> 
*/

function displayStatistics(){
    // alert("In display stats");
    // alert(testdataset);
    // alert(typeof(testdataset[0][2])); OP-> Number
    // alert(testdataset[2]); OP-> Undefined
    l=testdataset.length;
    var tc= document.getElementById("totalcorrect");
    tc.innerHTML = testdataset[0][2];
    var tic= document.getElementById("totalincorrect");
    tic.innerHTML = testdataset[0][3];
    var ua= document.getElementById("unattempted");
    ua.innerHTML = 15 - (testdataset[0][2] + testdataset[0][3]);
    // alert(tc);
    // alert(tic);
}