import sendgrid
import os
from sendgrid.helpers.mail import *

# Used for testing purposes can be deleted
test = {
    'host': 'whatever',
    'emails': ['ryanmadlener@hotmail.com', 'ryanmadlener@hotmail.com'],
    'duration': 60,
    'description': 'test event',
    'start_date': '2020-04-22',
    'event_name': 'test'
}


def send_confirmation_email(data):

    # Sending an email for every email in the dictionary
    for email in data['emails']:
        sg = sendgrid.SendGridAPIClient(api_key='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')
        from_email = Email("info@calconnect.com")
        to_email = To(email)
        subject = "Your CalConnect Meeting Has Been Successfully Scheduled!"
        content = "Thank you for using CalConnect!\n\n The appointment booked by account "\
                + data['host'] + " was added to your calendar. Make sure you are not missing it."\
                + "\n\nWords from host:\n"\
                + "    \"" + data['description'] + "\""\
                + "\n\n Sincerely,\n CalConnect Team"

        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)


# send_confirmation_email(test)