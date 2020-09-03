from datetime import date
import sqlite3
from extra import write_log

from attachments import mail_downloader
from model import model_extract
from data_loader import data_load
from mail import email_content

today = str(date.today())
DB = 'database.sql'
usr_name = 'root'


def db_change():  # date updater
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cmd = 'update login_access set uid=? where username=?'
    exe = cur.execute(cmd, (today, usr_name))
    conn.commit()
    conn.close()


def verify():                                                   # verify date instance and send mail
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cmd = 'select uid from login_access where username=?'
    db_date = cur.execute(cmd, (usr_name,)).fetchone()[0]
    cur.close()

    if today == db_date:
        pass
    else:
        write_log('$$ Log Load Started $$')
        mail_downloader()
        model_extract()
        data_load()
        db_change()
        write_log('Log Sent')
        write_log('$$ Log Load Ended $$')
