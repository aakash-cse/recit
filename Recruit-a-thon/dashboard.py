import sqlite3
import json
from mail import email_content
import os
import hashlib
import binascii
import random
import string

DB = "database.sql"


def get_all_details():                    # to fetch all the user details as json format
    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        cmd = 'SELECT ID,NAME,SKILLS,YEARS_OF_EXP from CANDIDATES ORDER BY ID DESC'
        rows = db.execute(cmd).fetchall()

        return json.dumps([dict(ix) for ix in rows])
    except:
        pass
    finally:
        conn.close()


def get_user_details(usr_id):              # to fetch the user details
    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        cmd = 'SELECT * from CANDIDATES where id='+usr_id
        rows = db.execute(cmd).fetchall()
        return(json.dumps([dict(ix) for ix in rows]))
    except:
        pass
    finally:
        conn.close()


def get_emp_details():
    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        cmd = 'SELECT * from EMPLOYEES'
        rows = db.execute(cmd).fetchall()

        return json.dumps([dict(ix) for ix in rows])
    except:
        pass
    finally:
        conn.close()


def graph_dashboard():  # graph dashboard
    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        cmd = 'SELECT mail_count,date_load from mail_load'
        rows = db.execute(cmd).fetchall()
        return(json.dumps([dict(ix) for ix in rows]))
    except:
        pass
    finally:
        conn.close()


def set_mail_load():                    # to fetch all the user details as json format
    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        mail_count = len(os.listdir('pdf_files'))
        cur.execute('INSERT INTO mail_load (MAIL_COUNT,DATE_LOAD) VALUES (' +
                    str(mail_count)+',DATE("now"))')
        conn.commit()
        return mail_count
    except:
        pass
    finally:
        conn.close()


def get_mail_id(usr_id):                   # To fetch the mail id from the user id
    try:
        conn = sqlite3.connect(DB)
        db = conn.cursor()
        cmd = 'SELECT EMAIL from CANDIDATES where id='+usr_id
        rows = db.execute(cmd)
        extract_id = rows.fetchmany()[0]
        mail_id = ' '.join(map(str, extract_id))
        return mail_id
    except:
        pass
    finally:
        conn.close()


def get_usr_name(usr_id):
    try:
        conn = sqlite3.connect(DB)
        db = conn.cursor()
        cmd = 'SELECT name from CANDIDATES where id='+usr_id
        rows = db.execute(cmd)
        extract_id = rows.fetchmany()[0]
        usr_name = ' '.join(map(str, extract_id))
        return usr_name
    except:
        pass
    finally:
        conn.close()


def get_emp_cnt():
    try:
        conn = sqlite3.connect(DB)
        db = conn.cursor()
        cmd = 'SELECT COUNT(*) from EMPLOYEES'
        rows = db.execute(cmd).fetchone()[0]
        return rows
    except:
        pass
    finally:
        conn.close()


def get_project_grp():
    try:
        conn = sqlite3.connect(DB)
        db = conn.cursor()
        cmd = 'select count(distinct (project_code)) from employees;'

        rows = db.execute(cmd)
        total_cnt = rows.fetchone()[0]
        return total_cnt
    except:
        pass
    finally:
        conn.close()


def get_total_salary():
    try:
        conn = sqlite3.connect(DB)
        db = conn.cursor()
        cmd = 'SELECT sum(salary) from EMPLOYEES '
        rows = db.execute(cmd).fetchone()[0]
        return rows
    except:
        pass
    finally:
        conn.close()


def get_mail_count():                   # To fetch the aggregate of incomming job mail
    try:
        conn = sqlite3.connect(DB)
        db = conn.cursor()
        cmd = 'select sum(Mail_Count ) from Mail_load ml'

        rows = db.execute(cmd)
        total_cnt = rows.fetchone()[0]
        return total_cnt
    except:
        pass
    finally:
        conn.close()


def get_tdy_mail_count():                   # To fetch the aggregate of incomming job mail
    try:
        conn = sqlite3.connect(DB)
        db = conn.cursor()
        cmd = 'select sum(Mail_Count ) from Mail_load ml where date_load=date("now")'
        rows = db.execute(cmd)
        total_cnt = rows.fetchone()[0]
        if total_cnt is None:
            return '0'
        else:
            return total_cnt
    except:
        pass
    finally:
        conn.close()


# Interview dasboard insert
def set_interview(usr_id, meeting_date, meeting_time, content):
    try:
        usr_email = get_mail_id(usr_id)
        usr_name = get_usr_name(usr_id)
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cmd = 'insert into schedule (candidate_name,candidate_email,meeting_date,meeting_time,content) values(?,?,?,?,?)'
        cur.execute(cmd, (usr_name, usr_email,
                          meeting_date, meeting_time, content))
        conn.commit()
        return True
    except:
        pass
    finally:
        conn.close()


def get_interview_schedule():                   # To get interview schedule
    try:
        conn = sqlite3.connect(DB)
        db = conn.cursor()
        cmd = 'select candidate_name,meeting_date,meeting_time from schedule where meeting_date=date("now");'
        rows = db.execute(cmd).fetchall()
        op = []
        for i in rows:
            x = ' '.join(i)
            op.append(x)
        return op
    except:
        pass
    finally:
        conn.close()


def preview_mail(usr_id):                               # 1 to trigger the preview mail
    try:
        email_content(1, get_mail_id(usr_id))
        return True
    except:
        return False


# 2 to trigger the interview mail
def interview_mail(usr_id):
    try:
        email_content(2, get_mail_id(usr_id))
        return 'Success'
    except:
        return 'Failure'



def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(30)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def set_user_signup(usr_name, email, pass_wrd):
    try:
        N = 4
        scrt_id = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(N))
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        pass_wrd = hash_password(pass_wrd)
        cmd = 'insert into login_access(username,email,password,secret_id) values(?,?,?,?)'
        cur.execute(cmd, (usr_name, email, pass_wrd, scrt_id))
        conn.commit()
        return 'Please note down ur secret id: '+str(scrt_id)
    except:
        return 'Unable to generate Id'
    finally:
        conn.close()

# set_user_signup('divakar','p@gmail.com','password')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def get_login_details(usr_name, pass_wrd):
    conn = sqlite3.connect(DB)
    db = conn.cursor()
    try:
        cmd = 'select password from login_access where username=?'
        rows = db.execute(cmd, (usr_name,))
        stor_dat = rows.fetchone()[0]

        status = verify_password(stor_dat, pass_wrd)
        return status
    except:
        return False
    finally:
        conn.close()
        
        
def set_forgot_password(scrt_id,usr_name,usr_pswd):                    
    conn = sqlite3.connect(DB)
    cmd = 'update  login_access set password=? where username=? and secret_id =?'
    try:
        hash_pwd=hash_password(usr_pswd)
        conn.execute(cmd,(hash_pwd,usr_name,scrt_id))
        conn.commit()
        return 'Update Successfull !'
    except:
        return 'Update Failed'
    finally:
        conn.close()
