// import
const express    = require('express')      // express framework
const bodyParser = require('body-parser')  // http post req handler
const cors       = require('cors')         // frontend backend api calling

// instantiate app
const app = express()

// enable
app.use(bodyParser.urlencoded({extended: true})) // url-encoded body parsing
app.use(bodyParser.json())             // body parsing
app.use(express.json())                // json parsing
app.use(cors())                        // cross origin resource sharing

// start server
const port = 8080
app.listen(port, () => console.log(`backend running on http://localhost:${port}`)) // port

//--------------------------- SCHEDULE EVENT ---------------------------

const schedule   = require('./schedule')  // import schedule event function

app.post('/receive', (req, res) => {      // receive event data from the frontend
  //console.log(req.body)
  schedule(req.body)                      // schedules event
  res.status(200).json({msg:'form data received'})
})
