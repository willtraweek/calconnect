# get attendees who are not subscribed

from `not_subscribed.py`, import the function on line 78, `get_not_subscribed_users(jsonFileName)`

function's **input**: json file (ex: `scheduledMeeting.json`)

function's **output**: python list of invitees whom the host has not subscribed to

to get credentials: `python get_credentials.py`

to run: `python not_subscribed.py`

file structure (just like Mitchell's)

├── calconnect                  <br>
│   ├── credentials.py          <br>
│   ├── get_credentials.py      <br>
│   ├── not_subscribed.py       <br>
│   └── scheduledMeeting.json   <br>
├── contacts.txt                <br>
└── google_credentials          <br>
    ├── client_secret.json      <br>
    └── credentials.json 
