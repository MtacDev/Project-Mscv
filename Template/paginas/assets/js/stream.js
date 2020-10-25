// se recive los datos del login

function sendForm() {
    var output = document.getElementById("output");
    var username = document.getElementById("user").value;
    var pass = document.getElementById("pass");


        postData('https://communities.cyclos.org/valpos/api/sessions', data = {
          user:"test2",
          password:"123456",
          remoteAddress:"string",
          channel:"main",
          sessionTimeout:{
            amount:0,
            field:"days"},
        })
      .then(data => {
        console.log(data); // JSON data parsed by `data.json()` call
      });
    /*$.ajax({

      type: "POST",
      url: "https://communities.cyclos.org/valpos/api/sessions",
      // The key needs to match your method's input parameter (case-sensitive).
      data: JSON.stringify(dato),
      crossDomain: true,
      contentType: "application/json; charset=utf-8",
      dataType: "json'",
      beforeSend : function(xhr){
        xhr.setRequestHeader("Authorization", "kM33fdeUoSr2wJEKmTMYZgPzsmFf4xpr");
      },
      success: function(data){alert(data);},
      failure: function(errMsg) {
          alert(errMsg);
        }
      });*/
        
    }

    async function postData(url = '', data ) {
      // Default options are marked with *
      const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {

          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          // 'Content-Type': 'application/x-www-form-urlencoded',
          'Session-Token': 'rcoGAgfm34KnCFWZQDDDEWn6nstHmoUH',       

        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
      });
      return response; // parses JSON response into native JavaScript objects
    }