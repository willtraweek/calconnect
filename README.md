# React, Node, Express Implementation of Cal Connect

For backup.

To run, you need to include your client_id and client_secret from google OAuth2, which you can obtain from the google cloud console

### Instructions
cd into frontend and run `npm install`
cd into backend and run `npm install`
while in backend, run `npm start`

got to `http://localhost:3000`

completed
- frontend submits form data to backend, backend uses this data to schedule an event on host's and attendee's google calendars

incomplete
- there should be an alert box from the browser after the user submits the event from
- determining who's not subscribed
- coming up with first-fit time that is available on everyone's calendar
