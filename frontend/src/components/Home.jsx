import React from 'react'
import axios from 'axios'
import { Button, Form, Container, Row, Col } from 'react-bootstrap'
import { GoogleLogin, GoogleLogout } from 'react-google-login'

const APIURL        = 'http://localhost:8080'
const CLIENT_ID     = '<PASTE YOUR CLIENT ID HERE>'
const CLIENT_SECRET = '<PASTE YOUR CLIENT SECRET HERE>'
const SCOPE         = 'profile email https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/admin.directory.resource.calendar.readonly'

class Home extends React.Component {
  state = {
    client_id       : CLIENT_ID,
    client_secret   : CLIENT_SECRET,
    access_token    : '',
    logged_in       : false,
    host_name       : '',
    host_first_name : '',
    event_name      : '',
    location        : '',
    earliest        : '',
    latest          : '',
    hours           : 0 ,
    minutes         : 0 ,
    temp_email      : '',
    emails          : [],
    description     : ''
  }

  renderLogin = () =>       
    <div style={{textAlign:'center', itemsAlign:'center'}}>
      <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
      <h4>Welcome to CalConnect.</h4><br/>
      <GoogleLogin
        clientId={CLIENT_ID}
        buttonText='Log in to book an event'
        scope={SCOPE}
        onSuccess={(res) => this.handleLoginSuccess(res)}
        onFailure={(res) => console.log(res)}
        cookiePolicy={'single_host_origin'}
      />
    </div>

  handleLoginSuccess = (res) => {
    //console.log(res)
    this.setState({access_token  : res.tokenObj.access_token})
    this.setState({host_first_name : res.profileObj.givenName})
    this.setState({host_name      : res.profileObj.name})
    this.setState({logged_in      : true})
  }

  renderForm = () =>
    <Container><br/>
      <Form>
        <div style={{float:'right'}}>
          <GoogleLogout
            type='button'
            clientId={CLIENT_ID}
            buttonText='Logout'
            onLogoutSuccess={()=>this.setState({logged_in:false})}
          />
        </div>
        <h4>Welcome {this.state.host_first_name}. Let's schedule an event.</h4>
          <Form.Label>Event Name</Form.Label><Form.Control type='text' onChange={(e)=>this.setState({event_name:e.target.value})}/>
          <Form.Label>Event Location</Form.Label><Form.Control type='text' onChange={(e)=>this.setState({location:e.target.value})}/>
          <Row>
            <Col><Form.Label>Earliest Date</Form.Label><Form.Control type='date' onChange={(e)=>this.setState({earliest:e.target.value})}/></Col>
            <Col><Form.Label>Latest Date</Form.Label><Form.Control type='date' onChange={(e)=>this.setState({latest:e.target.value})}/></Col>
          </Row>
          <Form.Label>Duration</Form.Label>
          <Row>
            <Col><Form.Control type='text' placeholder='Hours' onChange={(e)=>this.setState({hours:e.target.value})}/></Col>
            <Col><Form.Control type='text' placeholder='Minutes' onChange={(e)=>this.setState({minutes:e.target.value})}/></Col>
          </Row>
          <Form.Label>Invitee's Emails</Form.Label>
          <Row>
            <Col><Form.Control type='email' placeholder='johndoe@gmail.com' value={this.state.temp_email} onChange={(e)=>this.setState({temp_email:e.target.value})} onKeyPress={target=>{if(target.charCode===13) this.addEmail()}}/></Col>
            <Col><Button type='button' onClick={this.addEmail}>Add</Button></Col>
          </Row>
          <Container>{this.renderEmails()}</Container>
          <Form.Label>Description</Form.Label><Form.Control as='textarea' rows='3' onChange={(e)=>this.setState({description:e.target.value})}/><br/>
          <Button type='button' onClick={(e)=>this.handleSubmit(e)} variant='success' size='lg' style={{width:'100%'}}>Book Appointment</Button>
      </Form>
      <br/>
    </Container>

  addEmail = () => {
    let emails = this.state.emails
    emails.push(this.state.temp_email)
    this.setState({emails})
    this.setState({temp_email:''})
  }

  deleteEmail = (index) => {
    let emails = this.state.emails
    emails.splice(index,1)
    this.setState({emails})
  }

  renderEmails = () => 
    this.state.emails.map(
      (email,index)=>
        <Row key={index} style={{margin:'5px 0'}}>
          <Col>
            {email}
          </Col>
          <Col>
            <Button 
              size='sm'
              type='button'
              variant='danger'
              onClick={index => this.deleteEmail(index)}
            >
              Delete
            </Button>
          </Col>
        </Row>
    )

  handleSubmit = (e) => {
    e.preventDefault()
    const { client_id, client_secret, access_token, host_name, event_name, location, 
            earliest, latest, hours, minutes, emails, description } = this.state
    const formData = { client_id, client_secret, access_token, host_name, event_name, 
                       location, earliest, latest, hours, minutes, emails, description }
    //console.log(formData)
    axios.post(APIURL + '/api/receive', formData) // send data to backend
    .then(res => console.log(res.data.msg))       // print response
  }

  render =() => 
    <div>
      {!this.state.logged_in && this.renderLogin()}
      {this.state.logged_in && this.renderForm()}
    </div>
}

export default Home