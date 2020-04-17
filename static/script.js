let invitees = [];

function addEmail() {
  let email = document.getElementById('input-invitee').value;
  
  if (invitees.indexOf(email) >= 0) {
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
    invitees.map(invitee => {
      let badge =  `<span class="invitee-email badge badge-info ml-2"
                          onclick=removeEmail('${invitee}')>
                       ${invitee}
                       <span class="ml-1">
                          X
                       </span>
                    </span>`
      list.innerHTML += badge;
    })
  }
}


// Sign-in success callback
function onLoginSuccess(googleUser) {
  // Retrieve the Google account data
  console.log(googleUser)
  gapi.client.load('oauth2', 'v2', function () {
    var request = gapi.client.oauth2.userinfo.get({
        'userId': 'me'
    });
    request.execute(function (resp) {
      // console.log(resp);
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
      'scope': 'profile email',
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
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    document.getElementById("user-welcome").style.display = "none";  
    document.getElementById("gSignIn").style.display = "block";
  });
  
  auth2.disconnect();
}



document.addEventListener("DOMContentLoaded", function(event) { 
  showEmails();
  document.getElementById("user-welcome").style.display = "none";
});