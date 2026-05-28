from app import app
from flask import render_template


@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/create")
def create():
    return "create"

@app.route("/update")
def update():
    return "update"

@app.route("/delete")
def delete():
    return "delete"