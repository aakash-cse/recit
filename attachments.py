import os
import shutil
from imbox import Imbox  # pip install imbox
from datetime import date
import datetime
from dashboard import set_mail_load
from extra import write_log,get_password

today = str(date.today())
year = int(today.split('-')[0])
month = int(today.split('-')[1])
day = int(today.split('-')[2])

def mail_downloader():
    write_log('\n'+"#Mail Downloader#")

    host = "imap.gmail.com"
    username = "testrecruitathon"
    download_folder = "pdf_files"
    password=get_password()

    try:
        shutil.rmtree(download_folder, ignore_errors=True)
        write_log("destroyed pdf_files")
    except:
        write_log('unable to destry pdf_files')
        exit()

    if not os.path.isdir(download_folder):
        os.makedirs(download_folder, exist_ok=True)
        write_log("created pdf_files")
    else:
        write_log("unable create pdf_files")

    try:    
        mail = Imbox(host, username=username, password=password,
                    ssl=True, ssl_context=None, starttls=False)
        messages = mail.messages(date__on=datetime.date(
            year, month, day))  # defaults to inbox
        write_log('\nCredentials Accepted')
    except:
        write_log('\nINVALID CREDENTIALS SUPPLIED')
        exit()

    for (uid, message) in (messages):
        mail.mark_seen(uid)

        for idx, attachment in enumerate(message.attachments):
            if attachment['content-type'][-3:] == 'pdf':
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{att_fn}"
                write_log("Mail Downloaded from "+download_path)
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())


    mail.logout()
    write_log("Mail logged out !")

    try:
        set_mail_load()
        write_log("Updated mail count to the database \nExiting mail system")
    except:
        write_log('Unique key constrain \nExiting mail system')

