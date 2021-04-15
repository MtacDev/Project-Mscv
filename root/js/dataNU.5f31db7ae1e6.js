// se recive los datos de los usuarios desde la Api de Cyclos

var userData = [];

window.addEventListener('load',  function () {
  
  const url = "https://cors-anywhere.herokuapp.com/https://communities.cyclos.org/valpos/api/users?groups=nodoValpos&includeGroup=true&includeGroupSet=true&orderBy=alphabeticallyAsc&roles=member&statuses=active&pageSize=5000";
  getData(url)
  .then( data => {
    data.json().then(response =>{ 
           
        for (let i = 0; i < response.length; i++) {              
            document.getElementById("textarea").innerHTML += '<option selected value="'+ response[i]["shortDisplay"]+'-'+
            response[i]["display"] +'">'+ response[i]["display"] +'</option>' ;          
        }  
        userData = response;    
      });
      
    })  
})

async function getData(url = '') {
 
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'GET', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'default', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit   
    headers: {
      // 'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',    
      'Authorization': 'Basic ' + btoa(authCred.userCred() + ':' + authCred.passCred()),       
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url|
  });
  return response; // parses JSON response into native JavaScript objects
}

