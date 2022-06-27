let fs = require('fs')

function myfunct(){
    console.log("this is a function in javascript")
    
    fs.readFileSync('temp.txt', function(err, data){
        console.log(typeof data)
        console.log(data)
    })
}

// function next_button_click(){
//     // fs.readFile('temp.txt', function(err, data){
//     //     console.log(typeof data)
//     //     console.log(data)

//     // })
// }

// next_button = getElementById('next-button');

// next_button.addEventListener("click", next_button_click)

document.addEventListener("DOMContentLoaded", myfunct);