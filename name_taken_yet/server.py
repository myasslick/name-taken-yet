import subprocess

import flask
from flask import render_template
from flask import request

from name_taken_yet.check_youtube import youtube_search
from name_taken_yet.check_gmail import check_account_exists

import sys

import logging
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.ERROR) # only log errors and above

app = flask.Flask(__name__)
app.logger.addHandler(handler)  # attach the handler to the app's logger


"""
@app.route("/")
def home_search(method="GET"):
    return render_template("search.html")

@app.route("/search")
def do_search():
    query = request.args["search_term"]
    gmail = check_account_exists(query)
    youtube = youtube_search(query)

    return render_template("search.html",
        gmail=gmail,
        youtube=youtube)
"""

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        query = request.form["term"]
        args = ["python", "demo.py", query]
        #args = ["python", "demo.py", '"{q}"'.format(q=query)]
        #p = subprocess.Popen(args,
        #        stdout=subprocess.PIPE,
        #        stderr=subprocess.PIPE
        #    )
        search_results = subprocess.check_output(args)
        #search_results = p.stdout
        print(search_results)
        return render_template("search.html",
            search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
