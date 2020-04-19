const { google } = require('googleapis')
const { OAuth2 } = google.auth

function schedule(data) {
    // create instance of oAuth w/ our client id, client secret, and user's refresh token
  const oAuth2Client = new OAuth2(data.client_id, data.client_secret)
  oAuth2Client.setCredentials({access_token: data.access_token})

  // crete authorized calendar instance
  const calendar = google.calendar({version:'v3', auth:oAuth2Client})

  // set up event
  const delay = 1

  const earliest = data.earliest // 2020-04-27
  const latest = data.latest     // 2020-04-30

  const start = new Date()          // current date & time 2020-04-18T04:35:46.096Z
  //start.setDate(start.getDay() + delay) // set an event for tomorrow

  const end = new Date()
  console.log(end)
  end.setHours(end.getHours() + parseInt(data.hours))
  console.log(end)
  end.setMinutes(end.getMinutes() + parseInt(data.minutes))
  console.log(end)

  //console.log((end-start)/3600000) // delay in hours
  
  const emails = data.emails

  const tz = 'America/Chicago'

  const invitees = []
  data.emails.forEach(email => {
    let obj = {}
    obj['email'] = email
    invitees.push(obj)
  })

  const event = {
    summary: data.event_name,
    location: data.location,
    description: data.description,
    start: {dateTime: start, timeZone: tz},
    end: {dateTime: end, timeZone: tz},
    attendees: invitees
  }

  console.log(event)

  // insert event into calendar
  calendar.freebusy.query(  
    {
      resource: {
        timeMin: start,
        timeMax: end,
        timeZone: tz,
        items: [{id:'primary'}]
      }
    },
    (err, res) => {
      if(err) return console.error('Free busy query error:', err)
      //console.log(res)
      if(res.data.calendars.primary.busy.length===0) // user is not busy at that time
        return calendar.events.insert(
          {calendarId:'primary', resource:event},
          err => {
            //if(erro) return console.error('Error creating calendar event:', err)
            return console.log('Event successfully created')
          }
        )
      return console.log('Someone is busy at that time')
    }
  )
}

module.exports = schedule