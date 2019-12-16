var questions=new Array(15); // Array of Random Question numbers
var answers=new Array(15);  //Array of Whether Answers marked are coorect(1) or not(0)
var elapsedtime = new Array(15);    //Array to store time taken in each question

var Default_val=0;
elapsedtime.fill(Default_val);

var timeTaken=30;
var timerFun;
var row=undefined;

window.onload= timer();
var startTime=undefined;
var finishTime=undefined;

// Function which ensures correct question is selected

//row refers to the data sent by flask, in our case it is the entire question table

function initialise(x){
    row=x;
    var last_question_no=40;
    for(var i=0;i<15;){
        var temp = Math.floor(Math.random()*(last_question_no-1+1)+1);      //question number between 1 to last_question_no
        if(!questions.includes(temp)){
            questions[i]=temp;  //To find integral random between a range, max not included, 
                            //Math.floor(Math.random()*(max-min)+min) 
            i++;
        }
        else{
            continue;
        }
    }
    alert(questions);
    alert(elapsedtime);
}

//Display the question the dynamically and get cookie to mark previously marked answer
function renderQuestion(a) {
    // alert(x);
    ques = document.getElementById("question-data");
    var x=questions[a-1];     //get the ath random question number
    //var row = {{ value }} ;

    // this data is sent in flask using render template, data is sent as comma separated all values
    // however, index 0 refers to values of all cols separated by comma, alert(row[x-1]); 
    // So row[x-1][1], refers to the (x-1)th row and 1st indexed column
    ques.innerHTML = "<h5 class='card-title' id='question-num'>Question No. " + a + "</h5>";
    ques.innerHTML += "<p class='card-text' id='question-content'>" + row[x - 1][1] + "</p>";
    ques.innerHTML += "<input id='option1' type='radio' name='option' value='1'>" + row[x - 1][4] + "<br><br>";
    ques.innerHTML += "<input id='option2'type='radio' name='option' value='2'>" + row[x - 1][5] + "<br><br>";
    ques.innerHTML += "<input id='option3'type='radio' name='option' value='3'>" + row[x - 1][6] + "<br><br>";
    ques.innerHTML += "<input id='option4'type='radio' name='option' value='4'>" + row[x - 1][7] + "<br><br>";
    
    var prev_ans=getCookie("Answer"+a);
    //alert("prev ans "+ prev_ans);
    if(prev_ans){
        document.getElementById('option'+prev_ans).checked=true;
    }
    
    startTime=Date.now()/1000; 
    //document.getElementById("question-num").addEventListener("load", qtimer);
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(' ');
    //alert("Cookie is "+ca);

    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function setCookie(name, value, minutes) {
    if (minutes) {
        var date = new Date();
        date.setTime(date.getTime() + (minutes * 60 * 1000));
        var expires = " expires=" + date.toGMTString();
    } else var expires = "";
    document.cookie = name + "=" + value + expires + " path=/";
}
 

//Function which stores answer for each question every time the answer is saved and sets the cookie
function storeAnswer(){

    //var row = {{ value }};
    var qno=document.getElementById('question-num');
    //Question No. 12
    var qnum_cur=parseInt(qno.innerText.substring(13));
    var qnum = questions[qnum_cur-1]; //Substring "12" converted to 12; 
    //substring(13) as from 'Question No. 3' we want from 13th char onwards
    //then find the corresponding random question number as, questions[...the whole code to find the corresponding question...]

    //alert("Question No. rn is "+qnum);
    //alert(row);
    var ans= row[qnum-1][8].charCodeAt()-96; //a=1,b=2.....
    //alert("Answer is "+ans);
    var ele = document.getElementsByName('option');
    var ansValue; 
    for(i = 0; i < ele.length; i++) { 
        if(ele[i].checked){
            ansValue = ele[i].value;
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

    finishTime=Date.now()/1000;
    elapsedtime[qnum_cur-1] += Math.floor(finishTime-startTime);
    startTime=finishTime;
    alert(answers);
    alert(elapsedtime);
    setCookie("Answer"+qnum_cur,ansValue,30);
}

function deleteAllCookies(){
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++)
      deleteCookie(cookies[i].split("=")[0]);
}

function deleteCookie(name){
    setCookie(name,"",-1);
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
    deleteAllCookies();
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