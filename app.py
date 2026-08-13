# app.py
# Entry point for the Mini SOC Dashboard web application

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Mini SOC Dashboard - Coming soon"


if __name__ == "__main__":
    app.run(debug=True)