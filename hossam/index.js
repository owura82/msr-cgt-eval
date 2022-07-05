const coder = "hossam";

function setSampleNumber(sample_number){
  document.getElementById('sample-num-container').textContent = 'Sample '+sample_number;
  document.getElementById('sample-number').textContent = sample_number;
}

function setImages(sample_folder, order){
  // const rand = Math.floor(Math.random() * 10);

  document.getElementById('bottom-image').src = '../assets/img/evals/'+sample_folder+'/coders/C.png'
  if (order === 'N'){
    //N = normal, I= inverted (doesnt really matter)
    document.getElementById('tl-image').src = '../assets/img/evals/'+sample_folder+'/coders/A.png';
    document.getElementById('tr-image').src = '../assets/img/evals/'+sample_folder+'/coders/B.png';
  } else {
    document.getElementById('tl-image').src = '../assets/img/evals/'+sample_folder+'/coders/B.png';
    document.getElementById('tr-image').src = '../assets/img/evals/'+sample_folder+'/coders/A.png';
  }
  document.getElementById('sample-folder').textContent = sample_folder;
  document.getElementById('coder-input').reset();
}

function getSelection(response){
  if (response === 'tl-button') {
    return document.getElementById('tl-image').src.endsWith('A.png') ? "A":"B";
  } else if (response === 'tr-button') {
    return document.getElementById('tr-image').src.endsWith('A.png') ? "A":"B";
  } else {
    return 'C';
  }
  
}

function handleFormSubmit(e){
  const form = document.getElementById('coder-input');
  const formData = new FormData(form);
  
  const response = formData.get('response');
 
  if (!response){
    alert('One of the options must be selected');
  } else {
    const selection = getSelection(response);
    const sample_number = document.getElementById('sample-number').textContent;
    const sample_folder = document.getElementById('sample-folder').textContent;

    const send_selection = new XMLHttpRequest();

    send_selection.onreadystatechange = function (){
      if (this.readyState == 4 && this.status == 200) {

        const resp = JSON.parse(this.responseText);

        if (resp['all_done'] === 'yes'){
          showAllDoneMessage();
        }
        console.log('response folder --> ', resp['sample_folder']);
        setImages(resp['sample_folder'], resp['top_order'])
        setSampleNumber(resp['sample_number']);
      }
    }
    const req_body = {
      coder: coder,
      sample_folder: sample_folder,
      sample_number: sample_number,
      result: selection
    };

    console.log(JSON.stringify(req_body))

    send_selection.open('POST', 'https://cgt-coder-app.herokuapp.com/store-response');
    send_selection.setRequestHeader('Content-Type', 'application/json');
    send_selection.send(JSON.stringify(req_body));
  }
  e.preventDefault();
}


function handlePreviousButtonClick() {
  const sample_number = document.getElementById('sample-number').textContent;

  if (parseInt(sample_number) <= 1) {
    return;
  }
  const getPrevious = new XMLHttpRequest();

  getPrevious.onreadystatechange = function (){
    if (this.readyState == 4 && this.status == 200) {
      if (this.responseText === 'no-previous-sample') {
        return;
      }
      const resp = JSON.parse(this.responseText);

      if (resp['all_done'] === 'yes'){
        showAllDoneMessage();
      }

      setImages(resp['sample_folder'], resp['top_order'])
      setSampleNumber(resp['sample_number']);
    }
  }
  console.log('here, previous')
  const req_body = {
    coder: coder,
    sample_number: sample_number
  };

  console.log(JSON.stringify(req_body))

  getPrevious.open('POST', 'https://cgt-coder-app.herokuapp.com/previous');
  getPrevious.setRequestHeader('Content-Type', 'application/json');
  getPrevious.send(JSON.stringify(req_body));
}


function handleGetNextButtonClick() {

  const sample_number = document.getElementById('sample-number').textContent;

  if (parseInt(sample_number) < 1) {
    return;
  }

  const getNext = new XMLHttpRequest();

  getNext.onreadystatechange = function (){
    if (this.readyState == 4 && this.status == 200) {
      if (this.responseText === 'no-previous-sample') {
        return;
      }
      const resp = JSON.parse(this.responseText);

      if (resp['all_done'] === 'yes'){
        showAllDoneMessage();
      }

      setImages(resp['sample_folder'], resp['top_order'])
      setSampleNumber(resp['sample_number']);
    }
  }
  console.log('here, previous')
  const req_body = {
    coder: coder,
    sample_number: sample_number
  };

  console.log(JSON.stringify(req_body))

  getNext.open('POST', 'https://cgt-coder-app.herokuapp.com/next');
  getNext.setRequestHeader('Content-Type', 'application/json');
  getNext.send(JSON.stringify(req_body));


}

function handleGetSample(e){
  const entered_value = document.getElementById('to-retrieve').value;

  if (isNaN(entered_value) || entered_value===''){
    alert("Must enter a number");
    return
  }

  if ((parseInt(entered_value) < 1 || parseInt(entered_value) > 87)){
    alert("Number must be between 1 and 87 (inclusive)");
    return
  }

  //make request for sample and update page
  const sample_request = new XMLHttpRequest();

  sample_request.onreadystatechange = function (){
    if (this.readyState == 4 && this.status == 200) {

      const resp = JSON.parse(this.responseText);

      if (resp['all_done'] === 'yes'){
        showAllDoneMessage();
      }
      setImages(resp['sample_folder'], resp['top_order'])
      setSampleNumber(resp['sample_number']);
    }
  }
  sample_request.open('GET', 'https://cgt-coder-app.herokuapp.com/get-sample?num='+entered_value+'&coder='+coder);
  sample_request.send();
  e.preventDefault();
}

function showAllDoneMessage(){
  document.getElementById('all-done-container').style.display = 'initial';
  document.getElementById('next-button').style.display = 'initial';
}


function loadInitialPictures(){
    const folder_request = new XMLHttpRequest();

    folder_request.onreadystatechange = function (){
      if (this.readyState == 4 && this.status == 200) {

        const resp = JSON.parse(this.responseText);

        if (resp['all_done'] === 'yes'){
          showAllDoneMessage();
        }
        setImages(resp['sample_folder'], resp['top_order'])
        setSampleNumber(resp['sample_number']);
      }
    }
    folder_request.open('GET', 'https://cgt-coder-app.herokuapp.com/current?coder='+coder);
    folder_request.send();

    //add event listeners to form
    const form = document.getElementById('coder-input');

    const back_button = document.getElementById('back-button');

    const retrieve_form = document.getElementById('get-sample-form');

    const next_button = document.getElementById('next-button');
    
    form.addEventListener('submit', handleFormSubmit);

    back_button.addEventListener('click', handlePreviousButtonClick);

    retrieve_form.addEventListener('submit', handleGetSample);

    next_button.addEventListener('click', handleGetNextButtonClick);
    
}

document.addEventListener("DOMContentLoaded", loadInitialPictures);