from flask import Flask

application = Flask(__name__)
app = application

@app.route("/")
def index():
    return("Welcome to my first Flask app!")

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()