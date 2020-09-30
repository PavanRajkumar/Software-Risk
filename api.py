from flask import Flask, request, jsonify, render_template
import Predictor.Predictor as Predictor
import pandas as pd
import os
import time

app = Flask(__name__, template_folder='templates')
app.config["DEBUG"] = True
LOG_FILE = "./Git_logs/Call_logs.txt"

@app.route("/predict/", methods=["POST"])
def post_json():

    # For sending data as a file
    #
    # if "/" in filename:
    #     # Return 400 BAD REQUEST
    #     os.abort(400, "no subdirectories directories allowed")
    # res = Predictor.get_latest_commit_details()
    # res = req_data.split(",")
    # res.append(len(res[1]))
    # res = Predictor.reshape_np(res)

    # Sending data as a json


    req_data = request.get_json()
    req_data = req_data["latest_commit"]

    res = Predictor.extract_info(req_data)
    if type(res) == type("Cannot analyse, no files changed"):
        return res

    df = pd.DataFrame(res, columns=list(
        "author,comment,changed files,lines added,lines deleted,msg_len".split(",")))

    Predictor.process_df(df)

    with open(os.path.join(LOG_FILE), "a") as fp:
        fp.write("[ " + str(time.strftime('%a %H:%M:%S')) + " ] " + str(res) + "\n")

    return "\nCommit has an estimated bug risk of :" + str(round(Predictor.predict(df, model)[0, 1] * 100, 4)) + "%"


@app.route('/', methods=["GET"])
def home():
    return '''<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<div id="output"></div>
<h3>Latest Commits</h3>
<a href="./Git_logs/Call_logs.txt">Link to file</a><script type= "text/javascript"> print("hello");w = window.open("./Git_logs/Call_logs.txt");w.print();\script>'''


@app.route('/predict', methods=["GET"])
def predict():
    return render_template("upload.html")

@app.route('/Git_logs/Call_logs.txt', methods=["GET"])
def print_log():
    with open(os.path.join(LOG_FILE), "r") as fp:
        data = fp.read()

    return render_template("upload.html", data=data)


if __name__ == '__main__':
    model_filename = "./Training/rf_model_del.pkl"
    model = Predictor.load_model(model_filename)

    app.run(port=5000, debug=True, host='127.0.0.1')
