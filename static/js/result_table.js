// include("./capture_parameter.js");
var dataset=undefined;
var topicdataset=undefined;

function initialise(x, x1){
    dataset= x;
    topicdataset= x1;
}
function displayQuestionResult(){
    alert("Inside function");
    alert(answers[0]);
    qtable= document.getElementById("qtable-body");
    for(var i=1;i<=15;i++){
        qtable.innerHTML="<tr><td>"+i+"</td><td>"+dataset[i-1][1]+"</td><td>"+elapsedtime[i-1]+"</td><td>"+optionchanges[i-1]+"</td><td>"+totalTimeTaken+"</td><td>"+row[questions[i]-1][10]+"</td><td>"+row[questions[i]-1][9]+"</td></tr>";
    }
}

/* <th>Question No</th>
<th>Correctness</th>    answers
<th>Time Taken</th> elapsedTime  
<th>Option Changes</th> optionchanges
<th>Time Taken per test</th>    totalTimeTaken
<th>Topic</th>
<th>Level</th> */