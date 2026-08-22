# app.py
# Entry point for the Mini SOC Dashboard web application

from flask import Flask, render_template
from scanner import scan
from auditor import run_all_checks
from analyzer import run_analysis

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan")
def run_scan():
    devices = scan("192.168.1.0/24")
    return render_template("index.html", devices=devices)


@app.route("/audit")
def run_audit():
    devices = []
    results = run_all_checks()
    return render_template("index.html", devices=devices, results=results)


@app.route("/analyze")
def run_log_analysis():
    devices = []
    results = []
    suspicious_ips = run_analysis()
    return render_template("index.html", devices=devices, results=results, suspicious_ips=suspicious_ips)


if __name__ == "__main__":
    app.run(debug=True)