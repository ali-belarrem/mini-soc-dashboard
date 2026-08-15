# app.py
# Entry point for the Mini SOC Dashboard web application

from flask import Flask, render_template
from scanner import scan

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan")
def run_scan():
    devices = scan("192.168.1.0/24")
    return render_template("index.html", devices=devices)


if __name__ == "__main__":
    app.run(debug=True)