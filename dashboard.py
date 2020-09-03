import sqlite3
import json
from mail import email_content
import os

DB = "database.sql"


def get_all_details():                    # to fetch all the user details as json format
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    cmd = 'SELECT ID,NAME,SKILLS,YEARS_OF_EXP from CANDIDATES ORDER BY ID DESC'
    rows = db.execute(cmd).fetchall()

    conn.close()

    return json.dumps([dict(ix) for ix in rows])


def get_user_details(usr_id):              # to fetch the user details

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    cmd = 'SELECT * from CANDIDATES where id='+usr_id
    rows = db.execute(cmd).fetchall()

    conn.close()

    return(json.dumps([dict(ix) for ix in rows]))


def graph_dashboard():  # graph dashboard

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    cmd = 'SELECT mail_count,date_load from mail_load'
    rows = db.execute(cmd).fetchall()

    conn.close()

    return(json.dumps([dict(ix) for ix in rows]))


def set_mail_load():                    # to fetch all the user details as json format
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    mail_count = len(os.listdir('pdf_files'))
    cur.execute('INSERT INTO mail_load (MAIL_COUNT,DATE_LOAD) VALUES (' +
                str(mail_count)+',DATE("now"))')
    conn.commit()
    conn.close()
    return 'Insertion Done'


def get_mail_id(usr_id):                   # To fetch the mail id from the user id
    conn = sqlite3.connect(DB)
    db = conn.cursor()
    cmd = 'SELECT EMAIL from CANDIDATES where id='+usr_id
    rows = db.execute(cmd)
    extract_id = rows.fetchmany()[0]
    mail_id = ' '.join(map(str, extract_id))
    conn.close()

    return mail_id


def get_mail_count():                   # To fetch the aggregate of incomming job mail
    conn = sqlite3.connect(DB)
    db = conn.cursor()
    cmd = 'select sum(Mail_Count ) from Mail_load ml'

    rows = db.execute(cmd)
    total_cnt = rows.fetchone()[0]
    conn.close()

    return total_cnt


def setup_interview(usr_name,usr_email,meeting_time):                    # Interview dasboard insert
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cmd='insert into schedule (candidate_name,candidate_email,meeting_time) values(?,?,?)'
    cur.execute(cmd,(usr_name,usr_email,meeting_time))
    conn.commit()
    conn.close()
    
    
def get_interview_schedule():                   # To get interview schedule
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    cmd = 'select * from schedule where meeting_date=date("now");'

    rows =db.execute(cmd).fetchall()
    conn.close()

    return(json.dumps([dict(ix) for ix in rows]))


def preview_mail(usr_id):                               # 1 to trigger the preview mail
    email_content(1, get_mail_id(usr_id))



def interview_mail(usr_id):                             # 2 to trigger the interview mail
    email_content(2, get_mail_id(usr_id))
