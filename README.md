# get attendees who are not subscribed

from `not_subscribed.py`, import the function on line 78, `get_not_subscribed_users(jsonFileName)`

function's **input**: json file (ex: `scheduledMeeting.json`)

function's **output**: python list of invitees whom the host has not subscribed to

to run: `python not_subscribed.py`

file structure (just like Mitchell's)

├── calconnect
│   ├── credentials.py
│   ├── get_credentials.py
│   ├── not_subscribed.py
│   └── scheduledMeeting.json
├── contacts.txt
└── google_credentials
    ├── client_secret.json
    └── credentials.json
