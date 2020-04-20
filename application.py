from flask import Flask, render_template, request
from not_subscribed import get_unsubscribed_users
from process_data import process_data
from send_emails import send_confirmation_email

application = Flask(__name__)
app = application

# create credentials.json based on template
def create_credentials(access_token):
    PATH_TEMPLATE = 'json/template.json'
    PATH_CREDENTIALS = 'json/credentials.json'
    
    content = ""
    with open(PATH_TEMPLATE, 'r') as f:
        content = f.read()

    content = content.replace('{access_token}', access_token)

    with open(PATH_CREDENTIALS, 'w') as f:
        f.write(content)


def book_appointments(data_front_end):
    data = {
        'host': data_front_end['emails'][0],
        'emails': data_front_end['emails'],
        'duration': data_front_end['duration'],
        'description': data_front_end['event'],
        'start_date': data_front_end['date']
    }
    process_data(data)


def send_follow_emails(data_front_end):
    data = {
        'host': data_front_end['emails'][0],
        'emails': data_front_end['emails'],
        'duration': data_front_end['duration'],
        'event_name': data_front_end['event'],
        'start_date': data_front_end['date'],
        'description': data_front_end['description'],
    }
    send_confirmation_email(data)


@app.route("/submit", methods=['POST'])
def submit():
    response = {
        'unsubscribedEmails': [],
    }

    data = request.get_json()
    access_token = data['accessToken']
    print(data)
    create_credentials(access_token)

    # get unsubscribed users
    response['unsubscribedEmails'] = get_unsubscribed_users(data['emails'][1:])

    if (len(response['unsubscribedEmails']) == 0): # good sign, let's book
        book_appointments(data)  
        send_follow_emails(data)

    return response
        


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
