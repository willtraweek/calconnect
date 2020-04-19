# function that gets attendees who are not subscribed

`pip install`<br/>
  `oauth2client`<br/>
  `--upgrade httplib2`<br/>
  `--upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`<br/>
  `pendulum`<br/>


from `not_subscribed.py`, import the function on line 78, `get_unsubscribed_users(jsonFileName)`

function's **input**: json file (ex: `scheduledMeeting.json`)

function's **output**: python list of invitees whom the host has not subscribed to

to get credentials: `python get_credentials.py`

to run: `python not_subscribed.py`

file structure (just like Mitchell's):<br>
`├── calconnect`                 <br>
`│   ├── credentials.py`         <br>
`│   ├── get_credentials.py`     <br>
`│   ├── not_subscribed.py`      <br>
`│   └── scheduledMeeting.json`  <br>
`└── google_credentials`         <br>
&nbsp;&nbsp;&nbsp;    `├── client_secret.json`     <br>
&nbsp;&nbsp;&nbsp;    `└── credentials.json `
