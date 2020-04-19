// import
const express    = require('express')      // express framework
const bodyParser = require('body-parser')  // http post req handler
const cors       = require('cors')         // frontend backend api calling
const schedule   = require('./schedule')   // schedule event

// instantiate app
const app = express()

// enable
app.use(bodyParser.urlencoded({extended: true})) // url-encoded body parsing
app.use(bodyParser.json())             // json parsing
app.use(express.json())                // enable json parsing???
app.use(cors())                        // cross origin resource sharing

const { google } = require('googleapis')
const { OAuth2 } = google.auth

// create instance of oAuth w/ our client id & client secret
const oAuth2Client         = new OAuth2(CLIENTID, CLIENTSECRET)
// NEED TO GET USER'S REFRESH TOKEN
oAuth2Client.setCredentials({refresh_token: REFRESHTOKEN})

// create authorized calendar instance
const calendar = google.calendar({version:'v3', auth:oAuth2Client})

// start server
const port = 8080
app.listen(port, () => console.log(`backend running on http://localhost:${port}`)) // port

// receive data from the backend
app.post('/api/receive', (req, res) => {
  //console.log(req.body)
  schedule(req.body)      // schedules the event
  res.status(200).json({msg:'form data received'})
})
