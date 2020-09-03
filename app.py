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
    error = None
    if request.method == 'POST':
        if request.form['loginuser'] != 'admin' or request.form['loginPassword'] != 'admin':
            write_log('\n$Invalid Credentials by: '+request.form['loginuser'])
        else:
            write_log('\nUsername: '+request.form['loginuser'])
            verify()
            return redirect("/dashboard")
    return render_template('Login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    pass


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    write_log('\n$Dashboard Page')
    user = 'dummy_user'
    n_app = get_mail_count()
    p_inc = 12
    c_rec = 5
    table_data = json.loads(get_all_details())
    graph_data = json.loads(graph_dashboard())
    write_log('#Graph Loaded')
    return render_template('dashboard.html', graph_data=graph_data, report="", table_data=table_data, user=user, n_app=n_app, p_inc=p_inc, c_rec=c_rec)


@app.route('/results', methods=['GET', 'POST'])
def results():
    user = 'dummy_user'
    n_app = get_mail_count()
    p_inc = 12
    c_rec = 5
    global candidate_id
    table_data = json.loads(get_all_details())
    graph_data = json.loads(graph_dashboard())
    if request.method == 'POST':
        report = json.loads(get_user_details(str(request.form['report'])))
        # sending the preview mail
        # don't send to others
        preview_mail(str(request.form['report']))
        write_log('\nUser load : '+str(request.form['report']))
        write_log('\nPreview Mail Event')
        candidate_id=request.form['report']
    return render_template('dashboard.html', graph_data=graph_data, report=report, table_data=table_data, user=user, n_app=n_app, p_inc=p_inc, c_rec=c_rec)


@app.route('/interview', methods=['GET', 'POST'])
def interview():
    if request.method == 'POST':
        interview_date = request.form['date']
        interview_time = request.form['time']
        comment = request.form['comment']
        interview_mail(str(candidate_id))
    return "<h1>Interview mail sent</h1>"


if __name__ == '__main__':
    global candidate_id
    app.run(host='127.0.0.1', port=8080, debug=True)
