from flask import Flask
from flask import render_template
from flask import request
from flask import request, redirect, render_template, url_for
import json
from dashboard import *
from mail import email_content
from log_load import verify
from extra import write_log
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        if request.form['loginuser'] != 'admin' or request.form['loginPassword'] != 'admin':
            write_log('\n$Invalid Credentials by: '+request.form['loginuser'])
            error="Invalid Credentials"
            return render_template('new_index.html',error=error)
        else:
            write_log('\nUsername: '+request.form['loginuser'])
            verify()
            return redirect("/dash")
    return render_template('new_index.html',error=error)# Login.html is used


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('new_index.html',error="Please contact your admin")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect("/")

# while merging change this to 
# @app.route('/dash', methods=['GET', 'POST']) 
@app.route('/dash', methods=['GET', 'POST'])
def dash():
    table_data = json.loads(get_all_details())
    return render_template("dash_board.html",table_data=table_data,label=1)

@app.route('/incoming', methods=['GET', 'POST'])
def incoming():
    graph_data = json.loads(graph_dashboard())
    return render_template("dash_board.html",graph_data=graph_data,label=2)

@app.route('/team_manag', methods=['GET', 'POST'])
def team_manag():
    table_data = json.loads(get_all_details())
    return render_template("dash_board.html",table_data=table_data,label=3)

@app.route('/hiring', methods=['GET', 'POST'])
def hiring():
    table_data = json.loads(get_all_details())
    return render_template("dash_board.html",report="",table_data=table_data,label=4)


@app.route('/hiring_result', methods=['GET', 'POST'])
def hiring_result():
    table_data = json.loads(get_all_details())
    if request.method == 'POST':
        report = json.loads(get_user_details(str(request.form['cand_id'])))
    return render_template("dash_board.html",report=report,table_data=table_data,label=4)

@app.route('/user_manag', methods=['GET', 'POST'])
def user_manag():
    return render_template("dash_board.html",label=5)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    data = "Post a job"
    return render_template("dash_board.html",data=data,label=6)

@app.route('/about', methods=['GET', 'POST'])
def about():
    data = "About us"
    return render_template("dash_board.html",data=data,label=7)

if __name__ == '__main__':
    global candidate_id
    app.run(host='127.0.0.1', port=8080, debug=True)
