import json
import random
import os
import time
from flask import Flask, render_template, redirect, request, url_for

# GLOBALS
db = "./urls/url.json"
app = Flask(__name__)

# BACKEND 5050
def get_data():
    with open(db, "r") as json_file:
        data = json.load(json_file)

    return data

def get_url(url):
    choice = ["url_1", "url_2"]
    data = get_data()
    for entry in data:
        if entry["base"] == url:
            u = random.choice(choice)
            return entry[u]


def write_url(base, url_1, url_2):
    item_data = {}
    data = get_data()

    item_data["base"] = base
    item_data["url_1"] = url_1
    item_data["url_2"] = url_2
    data.append(item_data)

    with open(db, "w") as f:
        json.dump(data, f, indent=4)


# BACKEND WEBSITE
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<int:base>')
def get_base(base):
    try:
        url = get_url(base)
        return redirect(url)
    except:
        return ""

@app.route('/create', methods = ['POST', 'GET'])
def create():
    if request.method == "POST":
        link = "http://127.0.0.1:5000/"
        base = int(time.time())
        url_1 = request.form['url_1']
        url_2 = request.form['url_2']
        write_url(base, url_1, url_2)
        link += str(base)
        #print(link)
        return render_template("create.html", url_1=url_1, url_2=url_2, content="Your 5050 Url:", link=link)
    else:
        return render_template("create.html", link="", url_1="", url_2="")

if __name__ == "__main__":
    app.run(debug=True)
