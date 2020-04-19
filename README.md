# Node, Express, React Implementation of CalConnect

For backup.

To run, you need to include your own `client_secret.json` file obtained from google cloud console and paste or replace it in `calconnect/frontend/src`

### Instructions
`cd` into `frontend` and run `npm install`<br/>
`cd` into `backend` and run `npm install`<br/>
in `backend`, run `npm start`<br/>

go to `http://localhost:3000`

### Completed
- frontend submits form data to backend, backend uses this event data to schedule an event on host's and attendees' google calendars

### Incomplete
- there should be an alert box from the browser after the user submits the event from
- determining who's not subscribed
- coming up with first time that is available on everyone's calendar
