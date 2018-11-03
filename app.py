import os
from flask import Flask,render_template ,request, redirect
import secrets
import sqlite3
from flask import g
from flask import session

# Create database

# Initialize the application
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(20)

@app.before_request
def before_request():
    g.db = sqlite3.connect("db/data.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html',added = "")

@app.route('/add', methods = ['GET'])
def add_():
    return render_template("add.html")

@app.route('/add_language',methods = ["POST"])
def add_language():
    language = request.form['Language']
    comment = request.form['Comment']
    good = True
    params=[]
    if not language:
        params["error_langauge"] = "Langauge name is required"
        good = False
    if not comment:
        params["error_comment"] = "Comment is required"
        good = False

    if good:
        g.db.execute("INSERT INTO languages (CSLanguage,comment) values (?,?)",[language,comment])
        g.db.commit()
        return render_template("index.html",added = "Language added successfully!!")
    else:
        return render_template("add.html",**params)

@app.route('/read', methods = ['GET'])
def read_language():
    langauges = g.db.cursor().execute("SELECT * FROM languages")
    return str(langauges.fetchall())
    #return render_template("read.html")



if __name__ == "__main__":
    app.run(debug=True)