var questions=new Array(15); // Array of Random Question number
var answers=new Array(15);  //Array of Answers
var timeTaken=30;
var timerFun;
var row=undefined;
window.onload= timer();
// Function which ensures correct question is selected

//row refers to the data sent by flask, in our case it is the entire question table

function initialise(x){
    row=x;
}

function renderQuestion(x) {
    // alert(x);
    ques = document.getElementById("question-data");
    //var row = {{ value }} ;
    // this data is sent in flask using render template, data is sent as comma separated all values
    // however, index 0 refers to values of all cols separated by comma, alert(row[x-1]);
    // So row[x-1][1], refers to the (x-1)th row and 1st indexed column
    ques.innerHTML = "<h5 class='card-title' id='question-num'>Question No. " + x + "</h5>";
    ques.innerHTML += "<p class='card-text' id='question-content'>" + row[x - 1][1] + "</p>";
    ques.innerHTML += "<input type='radio' name='option' value='1'>" + row[x - 1][4] + "<br><br>";
    ques.innerHTML += "<input type='radio' name='option' value='2'>" + row[x - 1][5] + "<br><br>";
    ques.innerHTML += "<input type='radio' name='option' value='3'>" + row[x - 1][6] + "<br><br>";
    ques.innerHTML += "<input type='radio' name='option' value='4'>" + row[x - 1][7] + "<br><br>";
    
    //document.getElementById("question-num").addEventListener("load", qtimer);
}

//Function which stores answer for each question every time the answer is saved
function storeAnswer(){
    //var row = {{ value }};
    var qno=document.getElementById('question-num');
    //Question No. 12
    var qnum = parseInt(qno.innerText.substring(13)); //Substring "12" converted to 12; 
    //substring(13) as from 'Question No. 3' we want from 13th char onwards

    //alert("Question No. rn is "+qnum);
    //alert(row);
    var ans= row[qnum-1][8].charCodeAt()-96; //a=1,b=2....
    //alert("Answer is "+ans);
    var ele = document.getElementsByName('option'); 
    for(i = 0; i < ele.length; i++) { 
    if(ele[i].checked){
        if(ele[i].value == ans){
        //alert("Correct Answer");
        answers[qnum-1]=1;
        }
        else{
        //alert("Wrong Answer");
        answers[qnum-1]=0;
        }
    } 
    }
}

//Function which checks the total number of correct answers at the end of the test
function checkAnswers(){
    var count=0;
    var total=0;
    //alert("ans array is "+ answers);
    for(var i=0;i<answers.length;i++){
    if(answers[i] == 1){
        count++;
        total++;
    }
    else if(answers[i] == 0){
        total++;
    }  
    }
    alert("Congratulations, Test Complete!\nNumber of correct answers are "+count+"\nTotal number of questions "+total);
    clearInterval(timerFun);
    var tim=document.getElementById('test-timer');
    var a= (tim.innerText).split(':');
    //alert("a is "+ a);
    var seconds=(+a[0])*60*60 + (+a[1])*60 + (+a[2]);
    var diff=(30*60)-seconds;

    alert("Time Taken by you is "+ toTimeString(diff));
}

function toTimeString(seconds){
    //alert("seconds is "+seconds);
    return (new Date(seconds * 1000)).toUTCString().match(/(\d\d:\d\d:\d\d)/)[0];
}

function timer(){
    var tim=document.getElementById('test-timer');
    //alert("tim is "+ tim);
    var a= (tim.innerText).split(':');
    //alert("a is "+ a);
    var seconds=(+a[0])*60*60 + (+a[1])*60 + (+a[2]);

    timerFun= setInterval(function(){
    seconds--;
    if(seconds>=0){
        tim.innerHTML=toTimeString(seconds);
    }
    
    if (seconds === 0) {
        alert('Time Over! Test Complete');
        clearInterval(timerFun);
        timeTaken=30;
    }
    },1000);
}
