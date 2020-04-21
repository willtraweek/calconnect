let invitees = [];
let hostName = "";
let accessToken = "";

function addEmail() {
  let email = document.getElementById('input-invitee').value;
  
  if (invitees.indexOf(email) == 0) {
    alert("You cannot invite yourself");
    return;
  }

  if (invitees.indexOf(email) >= 1) {
    alert("You already invite this person");
    return;
  }

  let regex = /^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$/;
  if (!regex.test(email)) {
    alert("Invalid email");
    return;
  }
  invitees.push(email);
  showEmails();
  document.getElementById('input-invitee').value = ""
}

function removeEmail(email) {
  let index = invitees.indexOf(email);
  invitees.splice(index, 1);
  showEmails();
}

function showEmails() {
  let list = document.getElementById("invitee-list")
  if (invitees.length === 0) {
    list.innerHTML = `<span style="color:gray"> No invitee`;
  }
  else {
    list.innerHTML = "Invitees: ";
    invitees.map((invitee, id) => {
      if (id > 0) {
        let badge =  `<span class="invitee-email badge badge-info ml-2"
                            onclick=removeEmail('${invitee}')>
                         ${invitee}
                         <span class="ml-1">
                            X
                         </span>
                      </span>`
        list.innerHTML += badge;
      }
    })
  }
}

// Sign-in success callback
function onLoginSuccess(googleUser) {
  // console.log(googleUser);
  accessToken = googleUser.tc.access_token;

  // Retrieve the Google account data
  gapi.client.load('oauth2', 'v2', function () {
    var request = gapi.client.oauth2.userinfo.get({
         'userId': 'me'
    });
    request.execute(function (resp) {
      invitees.push(resp.email);
      hostName = resp.name;
      document.getElementById("gSignIn").style.display = "none";
      document.getElementById("user-name").innerHTML = resp.given_name;
      document.getElementById("user-welcome").style.display = "block";
    });
  });
}

// Sign-in failure callback
function onLoginFailure(error) {
  console.log("Error when logging in " + error)
}

// Render Google Sign-in button
function renderButton() {
  gapi.signin2.render('gSignIn', {
      'scope': 'profile email https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/admin.directory.resource.calendar.readonly',
      'width': 240,
      'height': 50,
      'longtitle': true,
      'theme': 'dark',
      'onsuccess': onLoginSuccess,
      'onfailure': onLoginFailure
  });
}


// Sign out the user
function signOut() {
  invitees = [];
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    document.getElementById("user-welcome").style.display = "none";  
    document.getElementById("gSignIn").style.display = "block";
  });
  
  auth2.disconnect();
}


// return a message to user
function handleResponse(resp) {
  if (resp['unsubscribedEmails'].length > 0){
    message = "We are not able to book the appointment. You need to subscribe these user(s):\n"
    message += "<ul>\n";
    resp['unsubscribedEmails'].map(email => {
      message += `<li>${email}</li>\n`;
    });
    message += "</ul>"
    $("#modal-body").html(message);
    $("#modal-title").html("Sorry :(");
    // change modal button green -> red
    $("#modal-button").removeClass("btn-success");
    $("#modal-button").addClass("btn-danger");
  }
  else {
    let message = "We booked your appointment! Thank you for using our website!";
    $("#modal-body").html(message);
    $("#modal-title").html("Thank you <3");
    $("#modal-button").addClass("btn-success");
    $("#modal-button").removeClass("btn-danger");
    document.getElementById("modal-button").onclick = 
      function() {
        location.reload();
      }
  }
}

function formSubmit() {
  if (invitees.length == 0) {
    alert("You have to login to book");
    return;
  }
  // disable button
  $("#book-button").attr("disabled", true);

  data = {
    host: hostName,
    emails: invitees,
    event: $("#input-event").val(),
    date: $("#input-start-date").val(),
    duration: $("#input-duration").val(),
    description: $("#input-description").val(),
    accessToken: accessToken,
  }

  $.ajax({
    type: "POST",
    url: "/submit",
    contentType: 'application/json',
    dataType : 'json',
    data : JSON.stringify(data),
    success: function(result, status) {
      handleResponse(result);
      $("#launch-modal").click();
      $('#book-button').removeAttr("disabled");
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log(jqXHR, textStatus, errorThrown);
    }
  })
}


// load all contents
document.addEventListener("DOMContentLoaded", function(event) { 
  showEmails();
  
  document.getElementById("user-welcome").style.display = "none";

  document.getElementById("form").onsubmit = function(e) {
    e.preventDefault();
    formSubmit();
  }
});
