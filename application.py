from flask import Flask, render_template, request
from not_subscribed import get_unsubscribed_users

application = Flask(__name__)
app = application

# create credentials.json based on template
def createCredentials(access_token):
    PATH_TEMPLATE = 'json/template.json'
    PATH_CREDENTIALS = 'json/credentials.json'
    
    content = ""
    with open(PATH_TEMPLATE, 'r') as f:
        content = f.read()

    content = content.replace('{access_token}', access_token)

    with open(PATH_CREDENTIALS, 'w') as f:
        f.write(content)


@app.route("/submit", methods=['POST'])
def submit():
    response = {
        'unsubscribedEmails': [],
    }

    data = request.get_json()
    access_token = data['accessToken']
    print(data)
    createCredentials(access_token)

    # get unsubscribed users
    response['unsubscribedEmails'] = get_unsubscribed_users(data['emails'])

    # if (len(unsubscribed_users) == 0): # good sign
    print(response)
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
