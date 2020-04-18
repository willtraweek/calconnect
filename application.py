from flask import Flask, render_template, request

application = Flask(__name__)
app = application


@app.route("/submit", methods=['POST'])
def submit():
    data = request.get_json()
    # print(form)
    result = {
    }
    if (len(data['emails']) == 1):
        result["result"] = "ALONE"
    else:
        result["result"] = "Thanks"
    return result


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
