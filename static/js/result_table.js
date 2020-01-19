// include("./capture_parameter.js");

function displayQuestionResult(){
    alert("Inside function");
    alert(answers[0]);
    qtable= document.getElementById("qtable-body");
    for(var i=1;i<=15;i++){
        qtable.innerHTML="<tr><td>"+i+"</td><td>"+answers[i-1]+"</td><td>"+elapsedtime[i-1]+"</td><td>"+optionchanges[i-1]+"</td><td>"+totalTimeTaken+"</td><td>"+row[questions[i]-1][10]+"</td><td>"+row[questions[i]-1][9]+"</td></tr>";
    }
}
function include(file) { 
    var script  = document.createElement('script'); 
    script.src  = file; 
    script.type = 'text/javascript'; 
    script.defer = true; 
    document.getElementsByTagName('head').item(0).appendChild(script); 
} 

/* <th>Question No</th>
<th>Correctness</th>    answers
<th>Time Taken</th> elapsedTime  
<th>Option Changes</th> optionchanges
<th>Time Taken per test</th>    totalTimeTaken
<th>Topic</th>
<th>Level</th> */