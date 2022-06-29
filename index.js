

function myfunct(){
    console.log("new log message")
    
    var txt = '';
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
      if(xmlhttp.status == 200 && xmlhttp.readyState == 4){
        txt = xmlhttp.responseText;
        console.log(txt)
      }
    };
    xmlhttp.open("GET","temp.txt",true);
    xmlhttp.send();
    
}

// function next_button_click(){
//     
// }

// next_button = getElementById('next-button');

// next_button.addEventListener("click", next_button_click)

document.addEventListener("DOMContentLoaded", myfunct);