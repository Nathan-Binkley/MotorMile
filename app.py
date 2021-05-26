import flask
from flask import request, render_template, redirect
import json
import data_get

app = flask.Flask(__name__)

@app.route("/")
def main():

    return render_template("index.html", audi=data_get.get_audi_local())

app.run(debug=True)