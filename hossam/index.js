

function myfunct(){
    console.log("new log message");

    const folder_request = new XMLHttpRequest();

    folder_request.onreadystatechange = function (){
      if (this.readyState == 4 && this.status == 200) {
        console.log(this.responseText);

        //add images to page
        top_left = document.getElementById('tl-image');
        top_right = document.getElementById('tr-image');
        bottom = document.getElementById('bottom-image');

        top_left.src = 'assets/img/evals/'+this.responseText+'/coders/A.png'
        top_right.src = 'assets/img/evals/'+this.responseText+'/coders/B.png'
        bottom.src = 'assets/img/evals/'+this.responseText+'/coders/C.png'
        
      }
    }

    folder_request.open('GET', 'https://cgt-coder-app.herokuapp.com/current?coder=hossam');
    folder_request.send();
    
}

// function next_button_click(){
//     
// }

// next_button = getElementById('next-button');

// next_button.addEventListener("click", next_button_click)

document.addEventListener("DOMContentLoaded", myfunct);