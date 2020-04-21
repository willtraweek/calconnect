from twilio.rest import Client

# Used for testing
data = {
    "number": "4259996002"
}

def send_confirmation_text(data):
    account_sid="AC671d8184b17090a0c010137f796b09f7" 
    auth_token="c453469f432e1ad45229c4ebd256b6d6"

    client = Client(account_sid, auth_token)

    client.messages.create(
        to="+1" + data["number"],
        from_="+12058325507",
        body="Congratulations! Your CalConnect Meeting has been Schedule"
    )

#send_confirmation_text(test)   