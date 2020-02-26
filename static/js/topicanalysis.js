// include("./capture_parameter.js");
var dataset=undefined;
var topicdataset=undefined;

function initialise(x1, x2){
    topicdataset=x1;
    testId= x2;
    // alert(typeof(dataset));
    
    displayTopicResult();
}
function displayTopicResult(){
    // alert("Dataset is: ");
    // alert(dataset);
    // alert("Topic Dataset is: ");
    alert(topicdataset);
    console.log(topicdataset);
    console.table(topicdataset);
    qtable= document.getElementById("qtable-body");
    for(var i=1;i<=4;i++){
        qtable.innerHTML +="<tr><td>"+i+"</td><td>"+topicdataset[i-1][2]+"</td><td>"+topicdataset[i-1][3]+"</td><td>"+topicdataset[i-1][4]+"</td><td>"+topicdataset[i-1][5]+"</td><td>"+topicdataset[i-1][6]+"</td><td>"+topicdataset[i-1][7]+"</td></tr>";
    }
}