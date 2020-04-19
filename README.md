# Node, Express, React Implementation of Cal Connect

For backup.

To run, you need to include your client_id and client_secret from google OAuth2 and paste them into `Home.jsx` in `calconnect/frontend/src/components`, which you can obtain from the google cloud console.

### Instructions
`cd` into `frontend` and run `npm install`<br/>
`cd` into `backend` and run `npm install`<br/>
while still in `backend`, run `npm start`<br/>

got to `http://localhost:3000`

### Completed
- frontend submits form data to backend, backend uses this data to schedule an event on host's and attendee's google calendars

### Incomplete
- there should be an alert box from the browser after the user submits the event from
- determining who's not subscribed
- coming up with first-fit time that is available on everyone's calendar
