from extra import write_log
from attachments import mail_downloader
from model import model_extract
from data_loader import data_load
from mail import email_content


def verify():                                                   
    write_log('$$ Log Load Started $$')
    mail_downloader()
    model_extract()
    data_load()
    write_log('Log Sent')
    write_log('$$ Log Load Ended $$')
