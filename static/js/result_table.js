// include("./capture_parameter.js");
var dataset=undefined;
var topicdataset=undefined;

function initialise(x, x1, x2){
    dataset= x;
    topicdataset=x1;
    testId= x2;
    // alert(typeof(dataset));
    // alert(ds)
    displayQuestionResult();
}
function displayQuestionResult(){
    // alert("Dataset is: ", dataset);
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