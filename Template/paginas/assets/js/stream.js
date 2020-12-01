// se recive los datos del login

function sendForm() {
  var output = document.getElementById("output");
  var username = document.getElementById("user").value;
  var pass = document.getElementById("pass").value;

postData('https://cors-anywhere.herokuapp.com/https://communities.cyclos.org/valpos/api/sessions', 
              data = {
                user: username,
                password: pass,
                remoteAddress:"string",
                channel:"main",
                sessionTimeout:{
                  amount:0,
                  field:"days"},
              })
    .then(data => {
      data.json().then(post =>{
        console.log(post)
      } ) // JSON data parsed by `data.json()` call  
    });
}



async function postData(url = '', data= {} ) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'default', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',       
        "Authorization": "Basic " + btoa("mtapia" + ":" + "m741852963"),       
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response; // parses JSON response into native JavaScript objects
}