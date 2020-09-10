from flask import Flask
from flask import render_template
from flask import request
from flask import request, redirect, render_template, url_for
import json
from dashboard import *
from mail import email_content
import time
from log_load import verify
from extra import write_log
app = Flask(__name__)

p_count=get_project_grp()
emp_cnt=get_emp_cnt()
notif=get_interview_schedule()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    global ln_usr
    if request.method == 'POST':
        ln_usr=request.form['loginuser']
        ln_pass=request.form['loginPassword']
        if get_login_details(ln_usr,ln_pass):
            write_log('\nUsername: '+request.form['loginuser'])
            return redirect("/dashboard")         
        else:
            error='Invalid Credentials'
            write_log('\n$Invalid Credentials by: '+request.form['loginuser'])
            return render_template('new_index.html',error=error)
        
    return render_template('new_index.html',error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('new_index.html',error="Please contact your admin")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect("/")

@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    table_data = json.loads(get_all_details())
    email_content(3,'rexdivakar@hotmail.com')
    return render_template("dash_board.html",table_data=table_data,label=1,p_count=p_count,emp_cnt=emp_cnt,notif=notif)

@app.route('/incoming', methods=['GET', 'POST'])
def incoming():
    graph_data = json.loads(graph_dashboard())
    mail_cnt=get_mail_count()
    tdy_cnt=get_tdy_mail_count()
    return render_template("dash_board.html",graph_data=graph_data,label=2,mail_cnt=mail_cnt,tdy_cnt=tdy_cnt,notif=notif)

def reload():
    verify()
    return redirect("/incoming")

@app.route('/team_manag', methods=['GET', 'POST'])
def team_manag():
    table_data = json.loads(get_emp_details())
    return render_template("dash_board.html",table_data=table_data,label=3,p_count=p_count,emp_cnt=emp_cnt,notif=notif)

@app.route('/hiring', methods=['GET', 'POST'])
def hiring():
    table_data = json.loads(get_all_details())
    return render_template("dash_board.html",report="",table_data=table_data,label=4,notif=notif)


@app.route('/hiring_result', methods=['GET', 'POST'])
def hiring_result():
    table_data = json.loads(get_all_details())
    global candidate_id
    if request.method == 'POST':
        candidate_id=str(request.form['cand_id'])
        report = json.loads(get_user_details(candidate_id))
        preview_mail(candidate_id)
    return render_template("dash_board.html",report=report,table_data=table_data,label=4,notif=notif)

@app.route('/call_interview', methods=['GET', 'POST'])
def call_interview():
    global candidate_id
    table_data = json.loads(get_all_details())
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        content=request.form['cmt']
        try:
            set_interview(candidate_id,date,time,content)
            interview_mail(candidate_id)
        except:
            candidate_id=0
            set_interview(candidate_id,date,time,content)
            interview_mail(candidate_id)
    return render_template("dash_board.html",report='msg',table_data=table_data,label=4,notif=notif)

@app.route('/user_manag', methods=['GET', 'POST'])
def user_manag():
    return render_template("dash_board.html",label=5,msg='',notif=notif)

@app.route('/inside_signup', methods=['GET', 'POST'])
def inside_signup():
    msg=''
    if request.method == 'POST':
        name = str(request.form['s_uname'])
        email = str(request.form['s_email'])
        pwd = str(request.form['s_pwd']) 
        print(name,email,pwd) 
        msg=set_user_signup(name,email,pwd)
        print(msg)
    return render_template('dash_board.html',label=5,msg=msg,notif=notif)

@app.route('/change_pwd', methods=['GET', 'POST'])
def change_pwd():
    msg=''
    if request.method == 'POST':
        uid = str(request.form['u_uid'])
        name = str(request.form['u_name'])
        pwd = str(request.form['u_pwd'])  
        print(uid,name,pwd)
        msg=set_forgot_password(uid,name,pwd)
        print(msg)
    return render_template('dash_board.html',label=5,msg=msg,notif=notif)

@app.route('/about', methods=['GET', 'POST'])
def about():
    data = "About us"
    return render_template("dash_board.html",data=data,label=6,notif=notif)

if __name__ == '__main__':
    global candidate_id
    global ln_usr
    app.run(host='127.0.0.1', port=8080, debug=True)
